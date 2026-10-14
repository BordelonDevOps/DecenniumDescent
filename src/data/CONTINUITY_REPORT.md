# Decennium Descent — Continuity Report



**Date:** 2026-07-29 (living document)  

**Scope:** Terminology, class roster, Oracle/Paladin/Druid, prestige↔feats, cosmology↔dungeon, character save shape, content gaps  

**Canon source:** `rulebook_output.txt`, cosmology/dungeon JSON, `canon-classes.js`  
**Source-of-truth hierarchy:** [`docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`](../docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md) (2026-07-30)  

**Glossary:** [`CONTINUITY_GLOSSARY.md`](./CONTINUITY_GLOSSARY.md) — approved terms for all agents  
**Overnight queue:** [`docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md`](../docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md) — P0–P2 vague backlog  

**Strategy:** TTRPG-first · Aethel tone · 17 canon classes · no SWTOR in product path

> **Overnight freeze ~23:30 local — P0/P1 clear; drafts for author morning review.**



---



## Continuity Watchlist



Living checklist — scan these on every content pass. Details in glossary.



| Watch area | Canonical source | Pass criteria |

|------------|------------------|---------------|

| **Terms** | Glossary + `cosmology-lore.json`, `dungeon-mechanics.json`, Oracle/Paladin modules | Spiral, Choir, First Song, Echo Court, Turning Spiral, Hush, Shardspire, Tenfold, Resonance, Weave used consistently; no foreign-deity patrons in Oracle mysteries. |

| **17 classes** | `canon-classes.js` (`CANON_CLASSES`) | Builder/Sheet picker = exactly 17; no "18 classes" product copy; Swashbuckler/Fighter not selectable. |

| **Oracle charges** | Rulebook Oracle ch.; `oracle-curses.js` `ORACLE_REVELATION_CHARGES` | Revelation Charges (3→7), not Weave RP or spell slots; Oracle excluded from `isSpellcasterClass()`; Weave tab shows guidance not slot picker. |

| **Weave / RP** | Rulebook Ch Resonance (~6071+) | Wizard/Mage/Cleric/Druid use **Resonance Points**; L1 defaults Mage/Cleric/Druid **3**, Wizard **4**; "spell slot" OK for Weave casters only. |

| **Prestige ↔ feats** | `prestige-lorebook.json` vs `feats.js` | Every feat name in prestige requirements exists in `feats.js`; Fighter reqs → Warrior alias in `prestige.js`. |

| **Save fields** | `character-storage.js` `normalizeCharacter()` | `class`, `archClass`, `sacredOath`, `druidCircle`, `oracleMystery`, `oracleCurse`, `resonancePoints` (default 3), `reputation` (faction map), spells arrays for Weave casters. |

| **Subclass display** | Builder/Sheet/Session | Store **ids** on save; display **human names** (oath/mystery/curse/circle labels). |

| **Draft flags** | Oracle mysteries/curses, Paladin oaths, `class-draft-levels.js` | `draft: true` content shows "(draft)" in UI; do not promote to canon without author. |

| **Gate bosses** | `dungeon-mechanics.json` ↔ `floor-encounters.json` | 10 tiers, names/zones/floors aligned; tier 10 silence lore ↔ Marquis of Silence. |

| **Druid circles** | `druid-shapeshifting.js`, `class-paths.js` | All 7 circles in UI + arch paths; hero forms keyed by circle id. |

### Wave 90 continuity stamp — 2026-07-30

Eight generic feat records—**Dispel Precision**, **Double Tap**, **Draw Cut**, **Dungeon Cartographer**, **Echo Spell**, **Efficient Caster**, **Empowered Summoning**, and **Energy Sink**—received presentation-only `draft: true` descriptions derived only from their existing prerequisite and effect fields. Their source effect strings and all feat behavior remain unchanged; Builder’s existing Draft badge provides provenance. **Umbrin**, **Resonance**, the **17-class** roster, and Oracle/Paladin author-review boundaries remain unchanged.

### Builder canon surfacing stamp — 2026-07-30 (pm)

**Character Builder UI audit:** Umbrin pinned/selectable (no star/draft race labels); Hybrid-B multiclass merge panel shows **Canon** badge when secondary Weave pool merges; Shadow Mystery + Grief Oath promoted (`draft: false` — no Draft badge); ceiling-cap callouts on **Class**, **Combat**, and **Paths** for Mirrorsage/Oracle/Paladin/Warrior/Dragoon/Tinker; **Advancement** card uses `CANON_XP_THRESHOLDS` with canon label, current-level highlight, XP-to-next, and Session-only draft-award note; feat list hides deprecated `skill_feats1_master_tracker` duplicate (Skill `master_tracker` only). Ethos blank-state, arch-path intent, Sacred Oath / Oracle empty states, and feat Draft badges were already wired (waves 116–121). `npx tsc --noEmit` clean. No commit.

### Gap-fill Worker 5 — T6–T10 draft dungeon seeds (2026-07-30)

**Delivered:** Tiers **6–10** in `floor-encounters.json` gained source-bounded draft seeds — `regionNames`, `hazards`, `gateBossSeed` (encounter title + rumor blurb), and `encounterVibe` — each marked `draft: true`. Tier-level `draft: true` and `mapped: false` preserved. Geography touches are selective: **Quiet Deep** (T6, T10), **Blackglass Reach** (T7), **Veyr-Obsid** (T8), **The Murk** iron-guild slang (T9); Umbrin faction lore is not forced into every tier.

**UI:** `DungeonGuide.tsx` and `EncountersBrowser.tsx` render the new seed sections with Draft badges; search haystacks include seed text. `dungeon-mechanics.json` `gateBosses` T6–T10 carry matching `draft: true` encounter titles/vibes.

**Boundary:** No routes, maps, encounter resolution, rewards, HP, or tactics confirmed. T6–T10 remain **unmapped** — Draft extract / survivor-rumor labeling only. No Oracle/Paladin/Umbrin tone review, commit, or deletion.

**Validation:** `npx tsc --noEmit` passed; no commit created.

### Bestiary Excel-first consolidation stamp — 2026-07-30 (pm)

**`Bestiary.xlsx`** is the **single canonical authoring workbook** (identity, loot, metadata, combat columns). Retired `Bestiary_combat_sandbox.xlsx` merged in; companion JSON is a **build artifact** only. Re-ingest: `python scripts/ingest_bestiary_from_excel.py` or `npm run ingest:bestiary`. **708 JSON entries**, **708 with AC/HP/combat** (698 excel-sandbox drafts + gate guardians from Excel cells). Gate guardians: **Excel combat wins when populated**; companion-authored fallback only when Excel attack cells empty. Sim smoke: Bloom L3 **63.7%**, Vaskor L8 **46.8%**. See [`docs/mechanics/BESTIARY_INGEST.md`](../docs/mechanics/BESTIARY_INGEST.md).

### Bestiary Excel re-ingest stamp — 2026-07-30 (pm)

Owner added **`Bestiary.xlsx`** (newest mtime) as the canonical name list; **`final_bestiary.xlsx`** supplements empty metadata columns (Size, Type, CR, XP, zones, tier drops). Neither workbook includes AC/HP/attack columns yet. Re-ingest: **708 JSON entries**, **698 metadata-only**, **10 gate guardians** with authored AC/HP/`combat` drafts + Excel `lootTable` harvest JSON. Ul'nath hidden. **`rename_value()` IP scrub on read.** See [`docs/mechanics/BESTIARY_INGEST.md`](../docs/mechanics/BESTIARY_INGEST.md). Combat sim re-run: Bloom L3 **63.7%** party HP loss; Vaskor L8 **46.8%**.

### Bestiary Excel re-ingest stamp — 2026-07-30

Owner correction applied: **`final_bestiary.xlsx`** holds **708 real monster rows** (identity, CR, XP, zones, loot tiers 1–6). Prior “708 AC 10 / HP 1 placeholders” was **`extract_full_bestiary.py` hardcoding**, not empty source data. `scripts/ingest_bestiary_from_excel.py` rebuilds `src/bestiary_data_full.json` (**708 unique names**, 698 metadata-only + 10 authored gate guardians with AC/HP/`combat` drafts). Ul'nath remains hidden. See [`docs/mechanics/BESTIARY_INGEST.md`](../docs/mechanics/BESTIARY_INGEST.md). **Umbrin** IP scrub unchanged.

### P0 #3 structured monster combat stamp — 2026-07-30

The Bestiary now has an optional, documented structured combat payload for ten existing **Gate Guardian** records, including Floor Encounter bosses **The Bloom That Hungers** and **Vaskor, the Stone Maw**. All payloads are marked `draft: true` with `source: "companion-authored draft"`; they add no D&D/FR names or lore and do not change the baseline Bestiary identity, zones, CR, XP, or descriptions. The balance harness uses only each payload’s at-will action and retains an explicit CR-proxy fallback with a reason for all other records. No combat estimate is canon until rulebook provenance is supplied. Bloom draft retune (vine-maw count 2→1) brings L3 sim expected loss to **63.7%** party HP (target band 40–70%).

### XP draft + Bloom retune stamp — 2026-07-30

[`XP_ADVANCEMENT_CANON.md`](../docs/mechanics/XP_ADVANCEMENT_CANON.md) now carries a **DRAFT — OWNER APPROVAL REQUIRED** provisional CR→XP table, equal party-split rule, and easy/medium/hard/deadly budget sketch. Confirmed L1–L20 thresholds are unchanged; no Session/Builder/encounter code was wired from the draft. Bloom structured at-will retune verified by `node scripts/combat-balance-sim.mjs`: **62.4 HP / 63.7%** L3 party loss (Vaskor unchanged at 46.8%).

### Hybrid-B Resonance rulebook sync — 2026-07-30

**Status:** Canon. `rulebook_output.txt` and the player rulebook now state the approved multiclass merge: full highest caster-tier Weave pool + ceil(25% of one secondary Weave pool), with Arcane Guilds applied once and no tertiary contribution. Oracle remains Revelation Charges (RC), never RP. **Hybrid-B** remains an internal label only; no Mystery or Oath draft status changed.



---



## ASK OWNER



**Protocol:** If a conflict cannot be resolved from rulebook + this report + glossary, **stop inventing** — add a row here and escalate to Director docs if design scope is affected.



| # | Conflict | Evidence | Blocked action |

|---|----------|----------|----------------|

| ~~1~~ | ~~**Bloodbound base class lists "Gravetouched"**~~ | ~~`prestige-lorebook.json` Bloodbound listed Gravetouched alongside Crimson Agent/Thief; Gravetouched is prestige #10.~~ | **Resolved (owner 2026-07-29):** Bloodbound base classes are **Crimson Agent or Thief (Lv 10+)** only — Gravetouched dropped from requirements. |

| ~~2~~ | ~~**Rulebook "eighteen classes" vs 17-row table**~~ | ~~Prose vs Classes Table.~~ | **Resolved (owner 2026-07-29):** "Eighteen" is a book typo; **v1 ships 17 base classes per Classes Table.** |

| ~~3~~ | ~~**Fighter chapter vs Classes Table**~~ | ~~Full Fighter chapter; not in `CANON_CLASSES`.~~ | **Resolved (owner 2026-07-29):** Fighter stays archive/reference only; Warrior/Soldier cover martial roles; not added to builder for v1. |

| ~~4~~ | ~~**Bestiary D&D name leakage**~~ | ~~e.g. "Drow Priestess of Lolth" in `bestiary_data_full.json`.~~ | **Resolved (owner 2026-07-29):** 54 creature entries renamed to Aethel-neutral labels in `bestiary_data_full.json` + `final_bestiary.xlsx`. See `docs/mechanics/BESTIARY_SCRUB_LOG.md`. |

| ~~5~~ | ~~**Dungeon `entryClasses` placeholders**~~ | ~~`dungeon-mechanics.json` cycle entry bullets unfilled.~~ | **Resolved (Director draft 2026-07-29 overnight):** `entryClasses.eligible` = all 17 `CANON_CLASSES`; `victoryConsequences.byTier` = tier boss/zone themes from `floor-encounters.json`. Both marked `draft: true`. Re-open only if rulebook Ch XII source specifies class restrictions. |

| ~~6~~ | ~~**Gravetouched feat stubs**~~ | ~~Several feats in `feats.js` note "Gravetouched definition not in available canon sources".~~ | **Closed as false escalation (Director + Continuity, 2026-07-29 overnight):** Gravetouched is prestige path **#10** with a full `prestige-lorebook.json` entry (base classes Cleric/Warrior/Crimson Agent, Lv10+) — it was never missing a class definition. The separate Bloodbound question (should Gravetouched count toward Bloodbound eligibility) is already resolved as **no** (see #1). Individual feat blurbs may stay thin/draft pending author polish, but this is no longer an ASK OWNER item — do not re-block Gravetouched hero-path wiring on it. |

| 7 | ~~**Cosmology XIV gate bosses vs dungeon tiers**~~ | ~~`cosmology-lore.json` XIV: Hollow King Lv10, Cindervore Lv30, Vox Prime Lv70. Live `floor-encounters.json` / `gateBosses`: Vaskor T1, Ashthirst T3, Xarog T7, etc.~~ | **Resolved (Director 2026-07-29 overnight):** Play uses **`floor-encounters.json` / Dungeon Guide**. Cosmology XIV marked `[superseded by Dungeon Guide]` — non-authoritative draft. See `docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md` VQ-01. |



---



## Collaborator-ready continuity gates



Invite writers / external collaborators only when **all** gates pass (or known gaps are explicitly accepted).



### Gate A — Terminology & cosmology

- [ ] [`CONTINUITY_GLOSSARY.md`](./CONTINUITY_GLOSSARY.md) read and followed

- [ ] No new patrons/deities outside Aethel cosmology without owner sign-off

- [ ] Oracle copy uses **Revelation Charges**; Weave copy uses **RP** — never swapped



### Gate B — Class roster (17)

- [ ] `CANON_CLASSES.length === 17` and Builder drift guard silent

- [ ] No Swashbuckler/Fighter in any player-facing picker

- [ ] New class content targets an existing canon class or is flagged `draft: true`



### Gate C — Oracle / Paladin / Druid

- [ ] 10 mysteries + 10 curses named; Ancestor + Shadow approved; Spiral-Touched rulebook-complete; 8 mysteries draft

- [ ] 10 Paladin oaths wired; Grief approved; Mercy + 8 others `draft: true` in companion

- [ ] 7 Druid circles in shapeshifting + class-paths

- [ ] No wholesale rewrite of mystery/oath trees in drive-by PRs



### Gate D — Prestige ↔ feats

- [ ] Automated feat-name cross-check: **0 missing** (`prestige-lorebook.json` → `feats.js`)

- [x] Bloodbound eligibility: Crimson Agent or Thief (Lv 10+) only — ASK OWNER #1 resolved 2026-07-29



### Gate E — Character save & UI

- [ ] `normalizeCharacter()` fields stable (see Watchlist)

- [ ] Subclass ids saved, display names resolved in Sheet + Session

- [ ] `resonancePoints` default **3** consistent (storage, Builder, Sheet, Session)

- [ ] Oracle excluded from Weave spell-slot UI paths



### Gate F — Dungeon & encounters

- [ ] 10 gate bosses aligned across dungeon JSON

- [ ] Tier/floor bands match encounter data



### Gate G — Build hygiene

- [ ] `npx tsc --noEmit` clean after TS edits

- [ ] `CONTENT_GAPS.md` / `content-gap-report.json` reflect known intentional drafts



**Current status (Oversight Phase C cleanup, 2026-07-30):** Gates A–G **pass** — continuity **clean pass** (no pass-with-drift items). Gate C docs match code: Mercy **`draft: true`**, Shadow + Grief promoted, Hybrid-B multiclass = **approved canon**. XP Builder uses **`CANON_XP_THRESHOLDS`**. Bloom Spore Burst retuned in Excel (**1d8**, recharge **6**); L3 sim **68.4%** party loss (40–70% band). Vaskor **58.2%** unchanged. Continuity VQ **P0 = 0 · P1 = 0**. Balance **P0 partially advanced**. T6–10 **still unmapped**. **`npx tsc --noEmit` clean**. See [`CONTINUITY_DETAILED_CHECK.md`](../docs/mechanics/CONTINUITY_DETAILED_CHECK.md) Phase C.

**Historical status (Oversight Phase B, 2026-07-30 — superseded by Phase C block above):** Gates A–G **pass** (Gate G green — `npx tsc --noEmit` clean post workers). **Gate C drift resolved:** glossary + checklist match code — Mercy **`draft: true`**, Shadow + Grief promoted. **Hybrid-B multiclass merge = approved canon** (Draft badge only when contributing pool table is draft). Continuity VQ **P0 = 0 · P1 = 0**. Balance **P0 partially advanced** (W3 ceiling caps doc + UI; W4 recharge schema + sim; W1 XP canon wired; W2 bestiary QA in Excel). T6–10 **still unmapped** (`mapped: false`). No unintended draft promotions; no Hybrid-B UI leaks. Bloom sim **93.2%** party loss with recharge (above 40–70% draft band — **retuned in Phase C**). See Phase B section in `CONTINUITY_DETAILED_CHECK.md`.

**Historical status (2026-07-30, wave 63 — superseded by Phase B block above):** Gates A, B, C, D, E, F, G **pass** (green). All ASK OWNER items (#1–#7) **resolved or closed**. **P0 = 0 · P1 = 0** — see `docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md`. Open backlog: **P2 only** (VQ-15–25 author-review drafts). **Depth passes complete:** Oracle revelations (all tiers + L12/18/20); Paladin oaths L3–L20 + `finalOathGift`; class-draft non-ASI thin (**0/0 under 100 chars**, waves 46–47); prestige hallmarks thin (**0 under 80 chars**); prestige capstones thin (**0 under 100 chars**, wave 50a); **all druid form traits thin (base/arch/hero)** — base (**0 remain under 60 chars**, waves 52b–54: **14/14 enriched**); arch (**0 remain under 60 chars**, waves 53–54: **15/15 enriched**); hero (**0 remain under 60 chars**, waves 48b–51: **29/42 enriched**); prestige unlock/entrance blurbs (**18/18 enriched**, waves 55b–57); all still **draft for author tone review**. **Resonance multiclass:** player-facing breakdown + Draft badges in Builder/Sheet/Session (wave 58); formula still **draft** per RESONANCE_CANON §7. **Session UX (waves 59–62):** VQ-22 wild-shape tracker + duration/Primal Recovery + **L15 arch attunement badge** (wave 62); VQ-23 overcast tier + school affinity/spell lookup + **Ethos row picker** (wave 62); **post-cast Burnout concentration hint stub** (Mage L17 draft, wave 61). **Class-draft L11–20 gaps (waves 59–63):** Druid L13/L15/L17 (wave 59); Mirrorsage/Mage/Bard (wave 61); **Cleric/Monk/Ranger/Dragoon/Tinker L13/L15/L17** (wave 63, 14 milestones). **34 ASI placeholders** in `class-draft-levels.js` are intentional. Product-path re-scan post wave 63: **clean** — **Umbrin** only; **Resonance** (Hybrid-B internal-only); **17 classes**; Cosmology XIV **still superseded**. **`npx tsc --noEmit` + `npm run build` green** (wave 63). **Coffee primary:** author tone review Oracle/Paladin/Umbrin; L11–20 author tables; Resonance multiclass still draft.



---



## What was checked



| Area | Files / surfaces | Result |

|------|------------------|--------|

| **Terminology** | `cosmology-lore.json`, `dungeon-mechanics.json`, `floor-encounters.json`, `oracle-mysteries.js`, `oracle-curses.js`, `backgrounds.js`, `class-paths.js` | Spiral, Choir, Echo Court, First Song, Shardspire, Tenfold, Resonance, Revelation Charges used consistently in authored data. No foreign-deity patrons in Oracle mysteries (Aethel cosmology only). |

| **Class roster (17)** | `canon-classes.js`, `CharacterBuilder.tsx`, `class-details.js`, `class-paths.js`, `prestige.js`, `character-storage.js`, `CharacterSheet.tsx`, `SessionTracker.tsx` | 17 selectable classes; picker matches `CANON_CLASSES` with dev-time drift guard. Swashbuckler orphan in `class-details.js` only (commented, not selectable). Fighter mapped to Warrior in `prestige.js` only. No "18 classes" product language. |

| **Oracle** | `oracle-mysteries.js`, `oracle-curses.js`, Builder/Sheet UI, `class-details.js`, `spell-utils.js` | 10 mysteries + 10 curses named per rulebook. Ancestor + Spiral-Touched rulebook canon; Battle–Time + 9 curses Aethel draft (`draft: true`). Save fields `oracleMystery`, `oracleCurse` consistent across storage/Builder/Sheet. |

| **Paladin / Druid** | `paladin-oaths.js`, `druid-shapeshifting.js`, `class-paths.js` | 10 Sacred Oaths wired; signature powers in class-paths match `paladin-oaths.js`. Druid circles (7) in shapeshifting module; hero forms keyed by circle id. |

| **Prestige ↔ feats** | `prestige-lorebook.json` vs `feats.js` | All feat names referenced in prestige requirements exist in `feats.js` (automated check, 0 missing). |

| **Cosmology ↔ dungeon** | `dungeon-mechanics.json` `gateBosses`, `floor-encounters.json` tiers | All 10 gate bosses align by tier, zone, and floor range. Tier 10 Marquis of Silence / Silencebound Void matches Echo Court / Hush lore. |

| **Character save shape** | `character-storage.js`, Builder save/load, Sheet display | `sacredOath`, `druidCircle`, `oracleMystery`, `oracleCurse`, `class`, `archClass`, `resonancePoints` normalized on load. |

| **Content gaps** | `CONTENT_GAPS.md`, `content-gap-report.json` | Updated post-pass; intentional drafts flagged. |



---



## Fixes applied



### Prior pass (2026-07-29 AM)



1. **Oracle — Revelation Charges vs spell slots**

   - `class-details.js`: L1 feature "Spellcasting" → "Revelation Charges (3, max 7)"; combat line updated.

   - `CharacterBuilder.tsx`: weave label "Revelation Caster (charges)"; class blurb aligned with rulebook; Spells tab shows Oracle-specific guidance instead of Weave picker.

   - `spell-utils.js`: Oracle excluded from `isSpellcasterClass()` (Revelation Caster, not Weave slot caster).



2. **Druid — class-paths circle parity**

   - `class-paths.js`: Added arch paths for **Circle of Thorns**, **Circle of Winterfang**, **Circle of the Rotshaper**, **Circle of the Ashen Grove**.



3. **Oracle — stale class-path text**

   - `class-paths.js`: Hero path actives updated — Final Revelations live in `oracle-mysteries.js` (draft flagged).



4. **Session — subclass continuity in notes**

   - `SessionTracker.tsx`: Saved characters added to combat include oath / circle / mystery / curse in notes when set.



5. **Gap docs**

   - `content-gap-report.json`: `ui-class-paths-display` marked resolved; `continuityPass` timestamp added.

   - `CONTENT_GAPS.md`: Continuity pass summary + link to this report.



### Continuity agent pass (2026-07-29 PM)



6. **Glossary & report infrastructure**

   - Added [`CONTINUITY_GLOSSARY.md`](./CONTINUITY_GLOSSARY.md) — approved terms for agents.

   - Added **Continuity Watchlist**, **ASK OWNER**, **Collaborator-ready gates** (this file).



7. **Session — RP default drift**

   - `SessionTracker.tsx`: Saved-character and quick-add ally `resonance` fallback **2 → 3** (matches rulebook L1 Mage/Cleric/Druid and `normalizeCharacter()`).



8. **Session — subclass display names**

   - `SessionTracker.tsx`: Notes resolve oath/mystery/curse/circle **ids → display names** via lookup helpers (parity with CharacterSheet).



9. **Sheet — RP display default**

   - `CharacterSheet.tsx`: RP badge fallback **0 → 3** when field absent post-normalize edge case.



10. **Bestiary — D&D / FR IP scrub (owner ruling #4)**

   - `src/bestiary_data_full.json` + `final_bestiary.xlsx`: 54 creature names renamed (Drow→Umbrin, Mind Flayer→Voidmind, Beholder→Gaze Tyrant, etc.).

   - `scripts/scrub_bestiary_ip.py` + `docs/mechanics/BESTIARY_SCRUB_LOG.md` added.

   - ASK OWNER #4 marked resolved.



### Continuity overnight pass (2026-07-29 PM)



11. **Cosmology XIV gate bosses — Director decided (WDL-1 / ASK OWNER #7)**

   - `cosmology-lore.json` XIV: `draftNote` → `[superseded by Dungeon Guide]`; gate boss subsections remain visible as non-authoritative reference only.

   - `CosmologyViewer.tsx`: draft banner text updated — no longer "ASK OWNER"; points to Dungeon Guide / Encounters for play.

   - **Play source of truth unchanged:** `floor-encounters.json` + `dungeon-mechanics.json` `gateBosses[]`.



12. **Overnight vague queue compiled**

   - Added `docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md` — P0–P2 ranked backlog from continuity sources.



13. **Glossary & product language scrub**

   - `CONTINUITY_GLOSSARY.md`: **Revelation Charges (RC)** abbreviation; Bloodbound eligibility reaffirmed; **Umbrin** race term + Calan'thir / Umbra / First Choir lore (VQ-14 resolved — People picker aligned to bestiary).

   - `SessionTracker.tsx`: RP max tooltip — removed "Hybrid-B canon" from player-facing title.

14. **Player race IP rename — Umbrin (VQ-14, 2026-07-29 PM; Director lore pass)**

   - **Name chosen:** **Umbrin** — one-word demonym clearly of **Umbra** (primordial deity); supersedes interim **Umbral Elf** label. No prior owner coinage found in sibling lore extracts.
   - **Lore:** Calan'thir and the **First Choir** shunned and exiled them, burning flesh to living obsidian; worship a perverse Umbra; hated by most, capable of strange alliances (EverQuest dark-elf tone).
   - **Companion updated:** `races.js` (`umbrin`), `builder-races.js`, `racial-variants.json`, `feats.js` (Nightfang Training prereq), `character-storage.js` (legacy `Drow` / `Umbral Elf` → `Umbrin`; `Noble Drow` / `Noble Umbral Elf` → **Obsidian Highborn** on load).
   - **Bestiary:** 10 Umbral Elf* entries → **Umbrin *** (`bestiary_data_full.json`; see `BESTIARY_SCRUB_LOG.md`).
   - **Avoid in product:** Drow, Dark Elf, Umbral Elf, Lolth, Underdark; Undercommon → Murkish; trait labels Umbrin Magic / Umbrin Weapon Training.
   - **Lore stub:** [`docs/mechanics/UMBRIN_LORE.md`](../../docs/mechanics/UMBRIN_LORE.md) — Obsidian Burn (`draft: true`), Umbra cult vs Choir orthodoxy, strange alliances reputation note.
   - **Author ticket:** Re-ingest `rulebook_output.txt` race chapter when docx updated; promote Obsidian Burn and Murk cult theology.



14. **Stale ASK OWNER cross-refs**

   - `CHARGEN_PROGRESSION.md`: rows 1–3 (seventeen classes / Fighter / Swashbuckler) marked resolved.

   - `MECHANICS_BIBLE_STUB.md` §7: TBD rows #2 (17 classes) and #3 (bestiary IP) marked resolved.



15. **Dungeon cycle entryClasses & victoryConsequences — Director draft (WDL-2 / ASK OWNER #5)**

   - `dungeon-mechanics.json`: `entryClasses` → `{ draft: true, eligible: CANON_CLASSES×17, policy }`; `victoryConsequences` → `{ draft: true, summary, byTier[1–10] }` from `floor-encounters.json` boss/zone themes.

   - `WORLD_DUNGEON_LOOP.md` WDL-2 closed; draft table row updated.

   - **Not mechanical rules** — flavor for GM/Cycle fiction until author confirms rulebook Ch XII source.



### Continuity wave 2 (2026-07-29 overnight)



16. **Glossary — Umbrin/Umbra/Calan'thir pass**

   - `CONTINUITY_GLOSSARY.md`: Added **Lumina** row; tightened Umbra (primordial) vs Umbrin (people) distinction; agent checklist item 8 — never "Umbral Elf" as current copy.
   - Product scan: `races.js`, `builder-races.js`, `racial-variants.json`, `bestiary_data_full.json` — **Umbrin** only; no stale Umbral Elf labels in live data.
   - `character-storage.js`: legacy aliases extended (`umbral-elf`, `drow` ids → Umbrin).

17. **OVERNIGHT_VAGUE_QUEUE re-rank (wave 2)**

   - **VQ-06** (Gravetouched) and **VQ-07** (`entryClasses`/`victoryConsequences`) marked **Resolved**.
   - **VQ-26** (`MECHANICS_BIBLE_STUB` stale rows) marked **Resolved**.
   - Remaining open P1: **VQ-08 through VQ-12** only (see queue snapshot).

18. **Bloodbound vs Gravetouched scan**

   - `prestige-lorebook.json` #4 Bloodbound: **Crimson Agent or Thief (Lv 10+)** — no Gravetouched in requirements string.
   - Gravetouched (#10) is a separate prestige path (Cleric/Warrior/Crimson Agent Lv 10+); class-details milestone lines list them independently.

19. **Oracle RC vs RP UI scrub**

   - `CharacterBuilder.tsx`: spell cost badge tooltip — removed "Hybrid-B" from player-facing text (parity with SessionTracker wave 1).
   - Verified: Oracle Weave tab shows Revelation Charges guidance; Session Pool column uses RC for Oracle, RP for Weave casters.

20. **Cosmology ↔ dungeon banner verification**

   - `cosmology-lore.json` XIV: `draft: true`, `[superseded by Dungeon Guide]` note intact.
   - `CosmologyViewer.tsx`: superseded banner renders for draft world sections; no additional conflict surfaces found.
   - `MECHANICS_BIBLE_STUB.md` §3 Cycle + §7 TBD rows updated to match Director draft resolutions.

21. **Stale doc sync**

   - `MECHANICS_BIBLE_STUB.md` §7 rows #3 and #7 → resolved.
   - `OVERNIGHT_VAGUE_QUEUE.md`: escalation table trimmed; P0–P1 snapshot added.

### Continuity wave 3 (2026-07-29 overnight)

22. **Full product-path scan (wave 3 targets)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Dark elf / Lolth** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, Builder/Sheet/Session UI | **Pass** — **Umbrin** only in live data/UI. Legacy save migration in `character-storage.js` (intentional). No Lolth/Dark Elf product copy. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Dev comment in Builder updated to "Resonance canon". Internal label remains in `resonance-economy.js` file header only. |
   | **Eighteen classes** | `canon-classes.js`, Builder picker, `class-details.js`, components | **Pass** — `CANON_CLASSES.length === 17`; no "18 classes" product copy in `src/`. Prose note in canon file comments only. |
   | **Gravetouched on Bloodbound** | `prestige-lorebook.json`, `class-details.js`, `feats.js`, glossary | **Pass** — Bloodbound #4: **Crimson Agent or Thief (Lv 10+)** only. Gravetouched is prestige #10 (separate path). Milestone lines list them independently, not coupled. |
   | **Oracle spell slots** | `spell-utils.js`, Builder Weave tab, Sheet, Session Pool column | **Pass** — Oracle excluded from `isSpellcasterClass()`; RC guidance in Builder; Pool column RC vs RP split in Session. |

23. **Fix applied (wave 3)**

   - `CharacterBuilder.tsx`: dev comment — "Hybrid-B canon" → "Resonance canon (RESONANCE_CANON.md)" (parity with player-facing scrub).

24. **Legacy root companion scrub (VQ-27)**

   - Root `index.html` + `game-data.js` synced to **Umbrin** (id `umbrin`, Murkish, Obsidian Highborn) — aligned to `races.js`. VQ-27 **resolved**.

25. **OVERNIGHT_VAGUE_QUEUE header refresh**

   - Snapshot: **P0 = 0 · P1 = 0**; VQ-27 resolved wave 5. All prior P0–P1 items remain resolved.

### Continuity wave 4 — overnight freeze (~23:30 local, 2026-07-29)

26. **Full product-path re-scan (freeze targets)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, Builder/Sheet/Session UI, root `index.html` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth. Bestiary: 10 Umbrin* entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header only. |
   | **Eighteen classes** | `canon-classes.js` (17), Builder picker, `src/components/` | **Pass** — `CANON_CLASSES.length === 17`; no "18 classes" product copy in components. Prose note in `canon-classes.js` / `content-gap-report.json` comments only. |
   | **Bloodbound + Gravetouched** | `prestige-lorebook.json`, `class-details.js`, glossary | **Pass** — Bloodbound #4: Crimson Agent or Thief (Lv 10+) only. Gravetouched #10 separate (Cleric/Warrior/Crimson Agent Lv 10+). Milestone lines independent. |
   | **Oracle slots** | `spell-utils.js`, Builder Weave tab, Sheet, Session Pool | **Pass** — Oracle in `REVELATION_CASTERS`; excluded from `isSpellcasterClass()`; RC guidance in Builder; Session RC vs RP split. |

27. **Umbrin alignment check**

   - `races.js` / `builder-races.js`: id `umbrin`, traits Umbrin Magic / Umbrin Weapon Training, Murkish, Obsidian Highborn subrace, Calan'thir / First Choir exile blurb — **aligned**.
   - [`docs/mechanics/UMBRIN_LORE.md`](../docs/mechanics/UMBRIN_LORE.md): Obsidian Burn, Umbra cult, strange alliances — **aligned** (`draft: true` pending author promotion).
   - [`CONTINUITY_GLOSSARY.md`](./CONTINUITY_GLOSSARY.md): Umbrin, Umbra, Lumina, Calan'thir, First Choir, Obsidian Burn, Murkish rows — **aligned**.

28. **Freeze stamp**

   - **Overnight freeze ~23:30 local — P0/P1 clear; drafts for author morning review.** No new blockers. P2 draft backlog unchanged (VQ-15–25).

### Continuity wave 10 — post waves 8–9 check (2026-07-29 PM)

29. **Full product-path re-scan (wave 10 targets — post waves 8/8b/9/9b)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterSheet.tsx` (Umbrin lore card), `GeneratorsPanel.tsx`, `Header.tsx`, `MonstersLibrary.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. 10 Umbrin* bestiary entries. Legacy migration in `character-storage.js` only. Wave 8 scrubbed `game-data.js` Mycelian **Undercommon** → **Mycelian**; removed obsolete Drow race-pool filter in GeneratorsPanel. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **SWTOR / FR deity leakage** | `src/` product path (data + components) | **Pass** — no SWTOR or Forgotten Realms product copy. Generic SRD labels (e.g. Owlbear) remain in bestiary by prior ruling. |
   | **Cosmology XIV superseded** | `cosmology-lore.json` XIV, `CosmologyViewer.tsx` world-section banner | **Pass** — `draft: true`, `draftNote` `[superseded by Dungeon Guide]` intact after wave 9b First Song split. Banner still points to Dungeon Guide / Encounters for gate bosses. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 4. Bloodbound: Crimson Agent or Thief (Lv 10+) only. Oracle in `REVELATION_CASTERS`; excluded from `isSpellcasterClass()`. |
   | **Build hygiene** | `npx tsc --noEmit` post waves 8–9 | **Pass** — exit 0. |

30. **Wave 10 stamp**

   - **Wave 10 check post waves 8–9 — green; P0/P1 clear; no new P2 blockers.** Waves 8–9 added Umbrin sheet lore, prestige feat drafts, header search stub, Cosmology First Song I–XII nav (9b) — none reintroduced forbidden IP or Hybrid-B UI. Existing P2 backlog unchanged (VQ-15–25); VQ-18/19/20 partially improved but not closed.

### Continuity wave 13 — post wave 12 spot-check (2026-07-29 PM)

31. **Full product-path re-scan (wave 13 targets — post wave 12)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterSheet.tsx`, `CharacterBuilder.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. Builder dev comment uses "Resonance canon (RESONANCE_CANON.md)". |
   | **Wave 12 touch surfaces** | `CharacterBuilder.tsx` (ESLint deps disable), `druid-shapeshifting.js` (named export), `SessionTracker.tsx` (initiative Sort/Roll all) | **Pass** — lint/build hygiene only; no forbidden IP or Hybrid-B reintroduced. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 10. |
   | **Build hygiene** | `npx tsc --noEmit` + `npm run build` (wave 12) | **Pass** — exit 0; ESLint warnings cleared. |

32. **Wave 13 stamp**

   - **Wave 13 check post wave 12 — green; P0/P1 clear; no new P2 blockers.** Wave 12 (ESLint fixes, druid-shapeshifting named export, Session initiative Sort/Roll all) did not reintroduce Drow/Hybrid-B UI leaks.

### Continuity wave 16 — post waves 12–15 spot-check (2026-07-29 PM)

33. **Full product-path re-scan (wave 16 targets — post waves 12–15 / 14b / 15b)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `EncountersBrowser.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. Wave 13 Umbrin pin + People search; no forbidden race IP reintroduced. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `EncountersBrowser.tsx`, `MonstersLibrary.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Waves 12–15 touch surfaces** | `SessionTracker.tsx` (Sort/Roll all, crowd filter, idempotent handoffs), `page.tsx` (`goToSession` / `handoffTick`), `session-handoff.ts`, `CharacterSheet.tsx` (print identity strip), `EncountersBrowser.tsx`, `MonstersLibrary.tsx`, `Header.tsx` (`/` shortcut), `oracle-mysteries.js` (14b/15b L1 enrichment) | **Pass** — UX/handoff hygiene only; Oracle L1 drafts retain `draft: true`; no forbidden IP or Hybrid-B UI. Handoff banner still uses lowercase source ids (`encounters`, `generators`). |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 13. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 16 re-check) | **Pass** — exit 0 (~9s). |

34. **Wave 16 stamp**

   - **Wave 16 check post waves 12–15 — green; P0/P1 clear; no new P2 blockers.** Waves 12–15 added Session initiative/crowd UX, export-field parity, `handoffTick`/`goToSession` re-apply, idempotent handoff consume, and Oracle L1 depth (14b/15b) — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 19 — post waves 17–18 spot-check (2026-07-29 PM)

35. **Full product-path re-scan (wave 19 targets — post waves 17–18 / 18b)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `SpellsLibrary.tsx`, `CraftingBuilder.tsx`, `EncountersBrowser.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `SpellsLibrary.tsx`, `CraftingBuilder.tsx`, `EncountersBrowser.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. Builder dev comment uses "Resonance canon (RESONANCE_CANON.md)". |
   | **Waves 17–18 touch surfaces** | `SessionTracker.tsx` (eslint-disable cleanup), `paladin-oaths.js` (Ancients/Chain/Grief/Vengeance/Chains Broken L3 drafts), `SpellsLibrary.tsx` (clear-filters UX), `CraftingBuilder.tsx` (clear-filters + search polish), `oracle-curses.js` (18b — 4 curse boon enrichments) | **Pass** — filter UX + draft oath/curse depth only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 16. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 19 re-check) | **Pass** — exit 0 (~8s). |

36. **Wave 19 stamp**

   - **Wave 19 check post waves 17–18 — green; P0/P1 clear; no new P2 blockers.** Waves 17–18 added Paladin L3 draft enrichment (all 9 draft oaths now L3-complete), Spells/Crafting clear-filters UX, Session eslint cleanup, and Oracle curse boon depth (18b) — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 21 — post waves 19–20 spot-check (2026-07-30)

37. **Full product-path re-scan (wave 21 targets — post waves 19–20 / 20b)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `ItemsLibrary.tsx`, `DungeonGuide.tsx`, `ReputationPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `ItemsLibrary.tsx`, `DungeonGuide.tsx`, `ReputationPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Waves 19–20 touch surfaces** | `oracle-curses.js` (8 boon enrichments — depth pass complete), `ItemsLibrary.tsx` (clear-filters), `class-draft-levels.js` (5 class L11–20 enrichments), `DungeonGuide.tsx` (search/filter + mapped toggle), `ReputationPanel.tsx` (20b — faction search/category filter) | **Pass** — draft depth + library filter UX only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 19. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 21 re-check) | **Pass** — exit 0 (~10s). |

38. **Wave 21 stamp**

   - **Wave 21 check post waves 19–20 — green; P0/P1 clear; no new P2 blockers.** Waves 19–20 finished Oracle curse boon depth (0 thin boons), enriched five class-draft milestones, added Dungeon Guide + ItemsLibrary + ReputationPanel filter UX — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 23 — post wave 22 spot-check (2026-07-30)

39. **Full product-path re-scan (wave 23 targets — post wave 22)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `ReputationPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `ReputationPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. Builder dev comment uses "Resonance canon (RESONANCE_CANON.md)". |
   | **Wave 22 touch surfaces** | `class-draft-levels.js` (Bard/Mage/Soldier/Crimson Agent/Mirrorsage L11–20 enrichments), `SessionTracker.tsx` (combatants empty-state tip: "Add saved character or foe.") | **Pass** — draft milestone depth + UX copy only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 21. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 23 re-check) | **Pass** — exit 0 (~8s). |

40. **Wave 23 stamp**

   - **Wave 23 check post wave 22 — green; P0/P1 clear; no new P2 blockers.** Wave 22 enriched five class-draft milestones (Bard/Mage/Soldier/Crimson Agent/Mirrorsage) and added Session combatants empty-state tip — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 25 — post wave 24 spot-check (2026-07-30)

41. **Full product-path re-scan (wave 25 targets — post wave 24)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx` (Obsidian Burn tip), `CharacterSheet.tsx`, `SessionTracker.tsx`, `page.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. Obsidian Burn tip uses Calan'thir / First Choir / Umbrin — no Drow. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. Builder dev comment uses "Resonance canon (RESONANCE_CANON.md)". |
   | **Wave 24 touch surfaces** | `class-draft-levels.js` (Ranger/Thief/Tinker L12 enrichments), `prestige-lorebook.json` (Giant Killer, Berserker hallmarks), `CharacterBuilder.tsx` (Obsidian Burn draft tip + `onOpenLore` Lore link), `page.tsx` (`onOpenLore` → my-content / Cosmology) | **Pass** — draft milestone + prestige hallmark depth + Umbrin lore UX only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 23. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 25 re-check) | **Pass** — exit 0 (~8s). |

42. **Wave 25 stamp**

   - **Wave 25 check post wave 24 — green; P0/P1 clear; no new P2 blockers.** Wave 24 enriched Ranger/Thief/Tinker L12 drafts, Giant Killer/Berserker prestige hallmarks, and added Umbrin Obsidian Burn lore tip with Cosmology handoff — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 27 — post wave 26 spot-check (2026-07-30)

43. **Full product-path re-scan (wave 27 targets — post wave 26)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 26–27 touch surfaces** | `class-draft-levels.js` (Dragoon L11, Mage L7/L11/L13/L15 slot enrichments), `prestige-lorebook.json` (Hexblade, Blademaster, Warlock hallmarks) | **Pass** — draft milestone + prestige hallmark depth only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 25. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 27 re-check) | **Pass** — exit 0 (~9s). |

44. **Wave 27 stamp**

   - **Wave 27 check post wave 26 — green; P0/P1 clear; no new P2 blockers.** Wave 27 enriched Dragoon L11 and Mage L7/L11/L13/L15 slot drafts plus Hexblade/Blademaster/Warlock prestige hallmarks — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 29 — post wave 28 spot-check (2026-07-30)

45. **Full product-path re-scan (wave 29 targets — post wave 28)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 28–29 touch surfaces** | `class-draft-levels.js` (Soldier L11/L16, Mirrorsage L11, Shaman L16, Tinker L15 enrichments), `prestige-lorebook.json` (Forge Master, Sapper hallmarks) | **Pass** — draft milestone + prestige hallmark depth only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 27. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 29 re-check) | **Pass** — exit 0. |

46. **Wave 29 stamp**

   - **Wave 29 check post wave 28 — green; P0/P1 clear; no new P2 blockers.** Wave 29 enriched Soldier L11/L16, Mirrorsage L11, Shaman L16, and Tinker L15 class drafts plus Forge Master/Sapper prestige hallmarks — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 30 — post wave 29b spot-check (2026-07-30)

47. **Full product-path re-scan (wave 30 targets — post wave 29b)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. People spark uses Umbrin pool + lore tags only. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 29b touch surfaces** | `GeneratorsPanel.tsx` (`lastSpark`, copy/clear spark toolbar) | **Pass** — UX polish only; Umbrin lore tags unchanged; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 29. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 30 re-check) | **Pass** — exit 0 (~12s). |

48. **Wave 30 stamp**

   - **Wave 30 check post wave 29b — green; P0/P1 clear; no new P2 blockers.** Wave 29b added GeneratorsPanel last-spark tracking, copy/clear spark toolbar — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 32 — post wave 31 spot-check (2026-07-30)

49. **Full product-path re-scan (wave 32 targets — post wave 31)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 31 touch surfaces** | `class-draft-levels.js` (Tinker L11, Soldier L13/L17, Dragoon L18, Monk L18 enrichments), `prestige-lorebook.json` (Berserker Reckless Charge, Chronomancer Acceleration Field, Mooncursed Lunar Tides hallmarks) | **Pass** — draft milestone + prestige hallmark depth only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 30. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 32 re-check) | **Pass** — exit 0 (~9s). |

50. **Wave 32 stamp**

   - **Wave 32 check post wave 31 — green; P0/P1 clear; no new P2 blockers.** Wave 31 enriched Tinker L11, Soldier L13/L17, Dragoon L18, Monk L18 class drafts plus Berserker/Chronomancer/Mooncursed prestige hallmarks — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 34 — post wave 33b spot-check (2026-07-30)

51. **Full product-path re-scan (wave 34 targets — post wave 33b)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 33a/33b + 34 touch surfaces** | `prestige-lorebook.json` (33a/33b hallmark depth complete), `oracle-mysteries.js` (34: Bones/Shadow/Stars Tier I), overnight docs | **Pass** — draft depth + doc refresh only; all mysteries retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 32. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npm run build` (wave 34 re-check) | **Pass** — exit 0. |

52. **Wave 34 stamp**

   - **Wave 34 check post wave 33b — green; P0/P1 clear; no new P2 blockers.** Thin-depth pass complete (class drafts 0, prestige hallmarks 0); Oracle Tier I enrichments (Marrow Drain, Shadow Step, Guiding Bolt) + coffee list refresh — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion.

### Continuity wave 35 — post wave 34b spot-check (2026-07-30)

53. **Full product-path re-scan (wave 35 targets — post wave 34b)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 34b touch surfaces** | `paladin-oaths.js` (34b: Ancients/Flame/Grief/Martyr King L5 revelation depth), overnight docs | **Pass** — draft oath L5 enrichment only; all four oaths retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 34. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count remains **0**. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 35 re-check) | **Pass** — exit 0 (~9s). |

54. **Wave 35 stamp**

   - **Wave 35 check post wave 34b — green; P0/P1 clear; no new P2 blockers.** Paladin L5 oath revelation enrichments (Ancients Primal Ward, Flame Zealot's Flame, Grief Last Rites, Martyr King Royal Decree) — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** in `class-draft-levels.js` confirmed intentional (ability score increases), not thin-content backlog.

### Continuity wave 36 — post wave 35c spot-check (2026-07-30)

55. **Full product-path re-scan (wave 36 targets — post wave 35c)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 35c touch surfaces** | `oracle-mysteries.js` (35c: Battle/Cataclysm/Life/Stars/Time Tier I), `paladin-oaths.js` (35c: Grief/Dominion/Ancients L9 revelation depth), overnight docs | **Pass** — draft mystery/oath enrichment only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 35. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count remains **0**. |
   | **Build hygiene** | `npm run build` (wave 36 re-check) | **Pass** — exit 0 (~71s). |

56. **Wave 36 stamp**

   - **Wave 36 check post wave 35c — green; P0/P1 clear; no new P2 blockers.** Oracle Tier I enrichments (Vanguard's Step, Gale of Unmaking, Thorned Shelter, Fate's Glimpse, Clarity, Moment's Pause) + Paladin L9 oath enrichments (Grief Memorial Flame, Dominion Law's Weight, Ancients Echo of Ages) — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional; thin-depth pass still **0/0** non-ASI.

### Continuity wave 37 — post wave 36 spot-check (2026-07-30)

57. **Full product-path re-scan (wave 37 targets — post wave 36)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 36 touch surfaces** | `oracle-mysteries.js` (36: Dream/Flame/Time/Shadow/Battle/Cataclysm/Life Tier I — 9 enrichments), overnight docs | **Pass** — draft mystery Tier I enrichment only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. Paladin L9: 0 oaths below Mercy depth — no oath edits. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 36. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count remains **0**. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 37 re-check) | **Pass** — exit 0 (~9s). |

58. **Wave 37 stamp**

   - **Wave 37 check post wave 36 — green; P0/P1 clear; no new P2 blockers.** Oracle Tier I mid-tier batch (Borrowed Beat, Mark of the Doomed, Ashen Shroud, Fault Line, Mirage, Bone Whisper, False Memory, Passion's Rush, Wrathful Brand) — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional; thin-depth pass still **0/0** non-ASI; **27/27** Tier I options enriched — depth pass **complete**; Tier II/III remain author-draft review.

### Continuity wave 38 — post wave 37 spot-check (2026-07-30)

59. **Full product-path re-scan (wave 38 targets — post wave 37)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 37 touch surfaces** | `oracle-mysteries.js` (37: Time/Battle/Bones×2/Cataclysm/Dream×2/Flame×2 Tier I — 9 mid-tier enrichments), overnight docs | **Pass** — draft mystery Tier I enrichment only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. **27/27** Tier I depth pass complete; Tier II/III trees remain author-draft review. Paladin L9: 0 oaths below Mercy depth — no oath edits. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 37. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count remains **0**. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 38 re-check) | **Pass** — exit 0 (~9s). |

60. **Wave 38 stamp**

   - **Wave 38 check post wave 37 — green; P0/P1 clear; no new P2 blockers.** Oracle Tier I depth pass **27/27 complete** (waves 34–37); Tier II/III revelation trees remain author-draft review — none reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional; thin-depth pass still **0/0** non-ASI; **0** Tier I options remain at ≤126 chars or mid-tier (133–168 chars).

### Continuity wave 39 — post wave 38 spot-check (2026-07-30)

61. **Full product-path re-scan (wave 39 targets — post wave 38)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 39 touch surfaces** | `oracle-mysteries.js` (39: Battle/Bones/Dream/Shadow/Stars Tier II — 5 thin enrichments; Stars/Life/Shadow/Dream/Flame Tier III — 5 shortest enrichments), `tools/oracle_tier3_lengths.py` | **Pass** — draft mystery Tier II/III enrichment only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. **14/27** Tier II options enriched; **0 thin remain** (≤130 chars). **5/9** Tier III options enriched; **0 thin remain** (≤130 chars). |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 38. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count remains **0**. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 39 re-check) | **Pass** — exit 0 (~19s). |

62. **Wave 39 stamp**

   - **Wave 39 check post wave 38 — green; P0/P1 clear; no new P2 blockers.** Oracle Tier II depth pass **complete for thin debt** (14/27 enriched — waves 38–39); **0 thin remain** at ≤130 chars. Oracle Tier III depth pass **started** (5/9 enriched — wave 39); **0 thin remain** at ≤130 chars; **4** Tier III options remain for author tone pass. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional; thin-depth pass still **0/0** non-ASI; Tier I depth pass **27/27 complete**.

### Continuity wave 40 — post wave 39 spot-check (2026-07-30)

63. **Full product-path re-scan (wave 40 targets — post wave 39)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 40 touch surfaces** | `oracle-mysteries.js` (40: Flame/Bones/Life/Cataclysm/Time Tier II — 5 mid-tier enrichments; Battle/Bones/Time/Cataclysm Tier III — 4 remaining capstones) | **Pass** — draft mystery Tier II/III enrichment only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. **19/27** Tier II options enriched; **0 thin remain** (≤130 chars); **8** mid-tier remain (139–160 chars). **9/9** Tier III options enriched; **0 thin remain** (≤130 chars). |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 39. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count remains **0**. |
   | **Build hygiene** | `npm run build` (wave 40 re-check) | **Pass** — exit 0 (~40s). |

64. **Wave 40 stamp**

   - **Wave 40 check post wave 39 — green; P0/P1 clear; no new P2 blockers.** Oracle Tier III depth pass **complete** (9/9 enriched — waves 39–40); **0 thin remain** at ≤130 chars. Oracle Tier II mid-tier batch (5 options — wave 40); **19/27** enriched cumulative; **0 thin remain** at ≤130 chars; **8** mid-tier options remain (139–160 chars). None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional; thin-depth pass still **0/0** non-ASI; Tier I depth pass **27/27 complete**.

### Continuity wave 41 — post wave 40 spot-check (2026-07-30)

65. **Full product-path re-scan (wave 41 targets — post wave 40)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 41 touch surfaces** | `oracle-mysteries.js` (41: Battle/Cataclysm/Dream/Flame/Life/Shadow/Stars/Time Tier II — 8 mid-tier enrichments) | **Pass** — draft mystery Tier II enrichment only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. **27/27** Tier II options enriched; **0 thin remain** (≤130 chars); **0 mid-tier remain**. **9/9** Tier III options enriched; **0 thin remain** (≤130 chars). |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 40. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count remains **0**. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 41 re-check) | **Pass** — exit 0 (~9s). |

66. **Wave 41 stamp**

   - **Wave 41 check post wave 40 — green; P0/P1 clear; no new P2 blockers.** Oracle Tier II depth pass **complete** (27/27 enriched — waves 38–41); **0 thin remain** at ≤130 chars; **0 mid-tier remain**. Oracle Tier III depth pass **complete** (9/9 enriched — waves 39–40); **0 thin remain** at ≤130 chars. Oracle revelation depth passes (Tier I/II/III) **complete** — author tone review still pending. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional; thin-depth pass still **0/0** non-ASI.

### Continuity wave 42 — post wave 41 spot-check (2026-07-30)

67. **Full product-path re-scan (wave 42 targets — post wave 41)**

   | Target | Result |
   |--------|--------|
   | **Wave 42 touch surfaces** | `paladin-oaths.js` (42: Silence/Flame/Grief/Chains Broken/Ancients/Dominion L13/L17 — 8 revelation enrichments; Chains Broken/Martyr King `finalOathGift`) | **Pass** — draft oath enrichment only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. Paladin L13/L17 pass **ongoing** — 8 thinnest enriched this wave. |
   | **Umbrin / no Drow-Lolth IP** | product path | **Pass** — clean; legacy migration in `character-storage.js` only. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 41. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count remains **0**. |
   | **Build hygiene** | `npm run build` (wave 42b re-check) | **Pass** — exit 0 (~54s). |

68. **Wave 42 stamp**

   - **Wave 42 check post wave 41 — green; P0/P1 clear; no new P2 blockers.** Paladin L13/L17 revelation pass **ongoing** (8 thinnest enriched — wave 42); 2 thinnest `finalOathGift` enriched (Chains Broken, Martyr King). Oracle revelation depth passes (Tier I/II/III) **complete** — author tone review still pending. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional; thin-depth pass still **0/0** non-ASI.

### Continuity wave 43 — post wave 42 spot-check (2026-07-30)

69. **Full product-path re-scan (wave 43 targets — post wave 42)**

   | Target | Result |
   |--------|--------|
   | **Umbrin / no Drow-Lolth IP** | **Pass** — `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, Builder/Sheet/Session UI, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | **Pass** — no Hybrid-B in `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, or other player surfaces. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 42 surfaces (unchanged)** | **Pass** — Paladin 8 L13/L17 revelation enrichments + 2 `finalOathGift` from wave 42; all retain `draft: true`. No new content edits this wave. |
   | **17 classes / Bloodbound / Oracle RC** | **Pass** — unchanged from wave 42. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | **Pass (intentional)** — 34 × "Ability Score Improvement" rows (L14/L19 per class); **not** thin-content debt. Non-ASI stub count remains **0**. |

70. **Wave 43 stamp**

   - **Wave 43 check — green; P0/P1 clear; no new P2 blockers.** Paladin L13/L17 revelation pass **complete** (6 remaining thin enriched — Vengeance, Chain, Dominion L17, Martyr King L13); **finalOathGift depth pass complete** (7 gifts enriched — Chain, Mercy, Ancients, Dominion, Silence, Grief, Vengeance). `UMBRIN_LORE.md` light clarity polish (no cosmology contradictions). Oracle revelation depth passes (Tier I/II/III) **complete** — author tone review still pending. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional; thin-depth pass still **0/0** non-ASI.

71. **Wave 44 stamp**

   - **Wave 44 check — green; P0/P1 clear; no new P2 blockers.** Oracle L12/L18 depth pass: **9 enrichments** (8× `propheticSurge` + Bones `finalRevelation`) vs Ancestor baseline; **0** thin `propheticSurge`, **0** thin `mysticInsight`; **1** remaining thin `finalRevelation` (Battle Avatar of the War Chorus, 193 chars). Paladin + Oracle Tier I/II/III depth passes remain **complete** — author tone review primary. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

72. **Wave 45 stamp**

   - **Wave 45 check — green; P0/P1 clear; no new P2 blockers.** Oracle L20 depth pass **complete**: Battle `finalRevelation` (Avatar of the War Chorus) enriched to Echo Crowned parity (388 chars); **0/9 thin** across `mysticInsight`, `propheticSurge`, and `finalRevelation`. Oracle depth debt **cleared**. PLAYTEST_SMOKE Path A Paths tip polished (L1 block, Tier I charge costs, L3 unlock hint). Paladin + Oracle Tier I/II/III + L12/L18/L20 depth passes remain **complete** — author tone review primary. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

73. **Wave 46 stamp**

   - **Wave 46 check — green; P0/P1 clear; no new P2 blockers.** Class-draft L11–20 thin pass: **5 enrichments** (Thief L18 Uncanny Dodge, Mage L20 Archmage Reservoir, Ranger L16 Favored Terrain, Oracle L16 Prophecy Trigger, Ranger L20 Legendary Hunter) — thinnest non-ASI under 100 chars brought to parity; **5 remain** (Shaman/Dragoon/Mirrorsage/Thief/Soldier L19–20 capstones, 75–83 chars). Oracle + Paladin depth passes **complete** (draft for author). **Coffee primary:** author tone review Oracle/Paladin/Umbrin; **secondary:** L11–20 author tables. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

74. **Wave 47 stamp**

   - **Wave 47 check — green; P0/P1 clear; no new P2 blockers.** Class-draft L11–20 thin pass **complete**: **5 final enrichments** (Shaman L20 Primal Convergence, Dragoon L20 Sky Sovereign, Mirrorsage L20 Infinite Reflection, Thief L20 Master of Shadows, Soldier L20 Immovable Line) — **0 non-ASI under 100 chars** remain (ASI placeholders OK). Running total **10/10** enriched across waves 46–47. Oracle + Paladin depth passes **complete** (draft for author). **Coffee primary:** author tone review Oracle/Paladin/Umbrin; **secondary:** L11–20 author tables. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

### Continuity wave 47 — post wave 46 spot-check (2026-07-30)

74. **Full product-path re-scan (wave 47 targets — post wave 46)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `GeneratorsPanel.tsx`, root `index.html`, `game-data.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. No Lolth/Underdark/Undercommon product copy. 10 Umbrin* bestiary entries. |
   | **Hybrid-B in player UI** | `CharacterBuilder.tsx`, `SessionTracker.tsx`, `CharacterSheet.tsx`, `Header.tsx`, `GeneratorsPanel.tsx`, `MonstersLibrary.tsx`, `CosmologyViewer.tsx` | **Pass** — no Hybrid-B in titles, labels, or tooltips. Internal label in `resonance-economy.js` file header + continuity docs only. Builder dev comment uses "Resonance canon (RESONANCE_CANON.md)". |
   | **Wave 47 touch surfaces** | `class-draft-levels.js` (5 L20 capstone enrichments — Shaman/Dragoon/Mirrorsage/Thief/Soldier) | **Pass** — draft milestone depth only; all retain `draft: true`; no forbidden IP or Hybrid-B UI. **10/10** non-ASI under 100 chars enriched across waves 46–47; **0 remain**. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json` #4 Bloodbound, `spell-utils.js` | **Pass** — unchanged from wave 46. Oracle uses Revelation Charges, not RP. |
   | **ASI placeholders (`class-draft-levels.js`)** | 34 × "Ability Score Improvement" rows (L14/L19 per class) | **Pass (intentional)** — standard D&D-style ASI milestones; **not** thin-content debt or enrichment targets. Non-ASI stub count under 100 chars remains **0**. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 47 re-check) | **Pass** — exit 0 (~7s). |

75. **Wave 47 stamp (spot-check)**

   - **Wave 47 check post wave 46 — green; P0/P1 clear; no new P2 blockers.** Class-draft L11–20 thin pass **complete** (**10/10 enriched** across waves 46–47; **0 remain** under 100 chars non-ASI). Oracle + Paladin depth passes **complete** (draft for author). **Coffee primary:** author tone review Oracle/Paladin/Umbrin; **secondary:** L11–20 author tables. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

76. **Wave 48 stamp**

   - **Wave 48 check — green; P0/P1 clear; no new P2 blockers.** Full production build **`npm run build` pass** (~48s). **Depth passes complete:** Oracle revelations (all tiers + L12/18/20); Paladin oaths L3–L20; class-draft non-ASI thin; prestige hallmarks thin — all 0 thin; content still **draft for author tone review**. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0** · **build green**. Handoff opening + coffee section refreshed; midnight checkpoint waves 1–48. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

### Continuity wave 48 — post wave 47 spot-check (2026-07-30)

77. **Full product-path re-scan (wave 48 targets — post wave 47)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, Builder/Sheet/Session UI, `GeneratorsPanel.tsx` | **Pass** — **Umbrin** only in live data/UI. Legacy migration in `character-storage.js` only. |
   | **Hybrid-B in player UI** | Builder, Session, Sheet, Header, Generators, Cosmology | **Pass** — no Hybrid-B in player surfaces. Internal label in `resonance-economy.js` + continuity docs only. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Depth pass debt** | `oracle-mysteries.js`, `paladin-oaths.js`, `class-draft-levels.js`, `prestige-lorebook.json` | **Pass** — Oracle revelations (Tier I/II/III + L12/18/20), Paladin L3–L20, class-draft non-ASI, prestige hallmarks all **0 thin**; still `draft: true` for author. |
   | **Build hygiene** | `npm run build` (wave 48 re-check) | **Pass** — exit 0 (~48s). |

78. **Wave 48 stamp (spot-check)**

   - **Wave 48 check post wave 47 — green; P0/P1 clear; no new P2 blockers.** **`npm run build` green.** Depth passes complete (Oracle revelations all tiers + L12/18/20; Paladin oaths L3–L20; class-draft non-ASI thin; prestige hallmarks thin). Content still draft for author tone review. **Coffee primary:** author tone review Oracle/Paladin/Umbrin; **secondary:** L11–20 author tables. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

79. **Wave 49 stamp**

   - **Wave 49 check post wave 48 — green; P0/P1 clear; no new P2 blockers.** **`npx tsc --noEmit` green** (~7s). Enriched **5** druid hero-form traits (Snow Leopard Glacier Claw, Frost Wyrmling Rime Scales, Insect Broodmother Brood Chitin, Charbear Ember Claw, Blight Elk Blight Antlers) and **3** prestige capstones (Berserker, Chronomancer, Storm Lord). **2** prestige capstones remain under 100 chars (Blademaster, Beastmaster). **18** druid hero traits remain under 60 chars. Depth passes still **complete** for prior targets; content still **draft for author tone review**. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

80. **Wave 51 stamp**

   - **Wave 51 check post wave 50a — green; P0/P1 clear; no new P2 blockers.** **`npx tsc --noEmit` green** (~7s); **`npm run build` green** (~41s). Enriched final **12** druid hero-form traits under 60 chars (Blazewood Stag Flaming Trail + Conflagration, Charbear Flame Aura + Smoke Cloud, Frost Wyrmling Breath Weapon, Carrion Rat King Poison Bite, Land + Thorns Blight Elk Aura of Decay, Land Tanglemaw Root Network, Moon Beastlord Chimera Cub + Alpha Dire Wolf, Mooncursed Lycanthropic Resilience). **0** druid hero traits remain under 60 chars (**29/42 enriched**, waves 48b–51). Prestige capstones **0 remain** under 100 chars (wave 50a). Depth passes still **complete** for prior targets; content still **draft for author tone review**. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

81. **Wave 52 stamp**

   - **Wave 52 check post wave 51 — green; P0/P1 clear; no new P2 blockers.** **`npm run build` green** (~53s). Handoff opening + coffee list refreshed for waves 1–51: depth passes complete (Oracle revelations all tiers + L12/18/20; Paladin oaths L3–L20; class-draft non-ASI thin; prestige hallmarks thin; prestige capstones thin; druid hero traits thin — all 0 thin); content still **draft for author tone review**. **Coffee primary:** author tone review Oracle/Paladin/Umbrin; L11–20 author tables; Resonance multiclass still draft. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

82. **Wave 53 stamp**

   - **Wave 53 check post wave 52b — green; P0/P1 clear; no new P2 blockers.** **`npx tsc --noEmit` green** (~8s). Enriched **2** druid base-form traits under 40 chars (Boar Gristle Hide, Bear Rootbark Hide) and **3** arch-form stubs (Dire Wolf Alpha Bite, Earth Warden Stoneheart Buffer, Ironhorn Ram Hornplate Hide). **6** druid base traits remain under 60 chars (**7/14 enriched**, waves 52b–53). **6** druid arch traits remain under 60 chars (**3/15 enriched**, wave 53). Druid hero-form **0 remain** under 60 chars (**29/42 enriched**, waves 48b–51). Depth passes still **complete** for prior targets; content still **draft for author tone review**. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

82. **Wave 53 stamp (quick continuity — Drow/Hybrid-B re-scan post wave 52b)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | `races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`, Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. Legacy migration keys in `character-storage.js` only (intentional). No Lolth/Underdark/Undercommon product copy. |
   | **Hybrid-B in player UI** | Builder, Session, Sheet, Header, Generators, Cosmology | **Pass** — no Hybrid-B in player surfaces. Internal label in `resonance-economy.js` file header + continuity docs only. |
   | **Wave 52b touch surface** | `druid-shapeshifting.js` (5 base-form trait enrichments) | **Pass** — draft depth only; no forbidden IP or Hybrid-B UI. |

   - **Wave 53 check post wave 52b — green; P0/P1 clear; no new P2 blockers.** Quick Drow/Hybrid-B product-path re-scan after wave 52b druid base-form enrichments. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional. **HANDOFF opening untouched** (per owner request).

83. **Wave 54 stamp**

   - **Wave 54 check post wave 53 — green; P0/P1 clear; no new P2 blockers.** **`npx tsc --noEmit` + `npm run build` green** (~47s). Enriched **6** remaining druid base-form traits under 60 chars (Wolf Keen Senses/Bite, Bear Claw, Hawk Keen Sight/Dive Attack, Panther Pounce) and **6** remaining arch-form traits (Dire Wolf Pack Tactics/Howl, Sky Serpent Lightning Bite/Glide Reflexes, Ironhorn Ram Ironhorn Stance, Shadow Lynx Shadow-Touched Strikes). Druid base-form **0 remain** under 60 chars (**14/14 enriched**, waves 52b–54). Druid arch-form **0 remain** under 60 chars (**15/15 enriched**, waves 53–54). Druid hero-form **0 remain** under 60 chars (**29/42 enriched**, waves 48b–51). **All druid trait tiers cleared** for 60-char depth pass; content still **draft for author tone review**. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional.

84. **Wave 55 stamp (handoff refresh + build)**

   - **Wave 55 check post wave 54 — green; P0/P1 clear; no new P2 blockers.** **`npm run build` green** (~45s). Refreshed **OVERNIGHT_HANDOFF** opening + coffee for waves 1–54: depth line now reflects **all druid form traits thin pass complete** (base/arch/hero, all 0 under 60 chars). **Coffee primary unchanged:** author tone review Oracle/Paladin/Umbrin; L11–20 author tables; Resonance multiclass still draft. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. No code/data edits this wave — docs + continuity stamp only.

85. **Wave 56 stamp (prestige unlock/entrance + CharacterSheet draft badges)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Wave 56 touch surfaces** | `prestige-lorebook.json` (5 unlock/entrance enrichments), `CharacterSheet.tsx` (Oracle/Paladin Draft badges) | **Pass** — prestige unlock depth + sheet draft UX only; Oracle/Paladin draft content still flagged; no forbidden IP or Hybrid-B UI. |
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. |
   | **Hybrid-B in player UI** | `CharacterSheet.tsx`, Builder, Session, Header | **Pass** — no Hybrid-B in player surfaces. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npx tsc --noEmit` (wave 56) | **Pass** — exit 0 (~10s). |

   - **Wave 56 check post wave 55 — green; P0/P1 clear; no new P2 blockers.** Enriched **5** prestige unlock/entrance blurbs (Hexblade, Battlemage, Beastmaster, Chronomancer, Storm Lord). **8/18** unlock/entrance blurbs enriched (waves 55b+56); **10 remain** (next shortest: Sapper #13 at 91 chars). **CharacterSheet** — visible amber **Draft** badges on Oracle/Paladin sections (missing-selection callouts + draft oath/mystery/curse/L20 gift). **`npx tsc --noEmit` green.** **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional. **HANDOFF opening untouched** (append only).

86. **Wave 57 stamp (prestige unlock/entrance completion)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Wave 57 touch surfaces** | `prestige-lorebook.json` (10 unlock/entrance enrichments) | **Pass** — all 18 prestige paths now have Aethel-toned unlock/entrance blurbs; no forbidden IP or Hybrid-B UI. |
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. |
   | **Hybrid-B in player UI** | `CharacterSheet.tsx`, Builder, Session, Header | **Pass** — no Hybrid-B in player surfaces. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npx tsc --noEmit` + `npm run build` (wave 57) | **Pass** — exit 0 (~51s combined). |

   - **Wave 57 check post wave 56 — green; P0/P1 clear; no new P2 blockers.** Enriched **10** remaining prestige unlock/entrance blurbs (Bloodbound, Echomancer, Forge Master, Giant Killer, Gravetouched, Mooncursed, Sapper, Soulrender, Verdant Animist, Warlock). **18/18** unlock/entrance blurbs enriched (waves 55b–57); **0 remain** under 120 chars. **`npx tsc --noEmit` + `npm run build` green.** **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional. **HANDOFF opening untouched** (append only).

87. **Wave 58 stamp (Resonance multiclass player-facing clarity)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Wave 58 touch surfaces** | `resonance-economy.js` (`multiclassRpBreakdown`, `formatMaxRpTooltip`, enriched `mergeMulticlassMaxRp` metadata), `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`, `CONTINUITY_GLOSSARY.md`, `PLAYTEST_SMOKE.md` | **Pass** — multiclass RP merge shows Draft badge + line breakdown in Builder/Sheet; Session max-RP tooltip shows merge summary; no new math beyond documented §7 draft formula; no Hybrid-B in UI. |
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. |
   | **Hybrid-B in player UI** | `CharacterSheet.tsx`, Builder, Session, Header | **Pass** — no Hybrid-B in player surfaces. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npx tsc --noEmit` + `npm run build` (wave 58) | **Pass** — exit 0. |

   - **Wave 58 check post wave 57 — green; P0/P1 clear; no new P2 blockers.** Shipped Resonance multiclass player-facing clarity: `multiclassRpBreakdown()` + `formatMaxRpTooltip()` helpers; Builder multiclass panel with Draft badge + line math; Sheet merge callout; Session max-RP tooltip; glossary + smoke stretch updated. Formula remains **draft** per RESONANCE_CANON §7 — no new canon math invented.

88. **Wave 59 stamp (Session wild-shape stub + overcast tier wiring + Druid draft L13–17)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Wave 59 touch surfaces** | `druid-shapeshifting.js` (uses/CR/form helpers), `SessionTracker.tsx` (VQ-22 wild-shape panel, VQ-23 spell-tier overcast), `class-draft-levels.js` (Druid L13/L15/L17), `LevelFeatureList.tsx` (draft count legend) | **Pass** — Session UX stubs only; no forbidden IP or Hybrid-B UI. |
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. |
   | **Hybrid-B in player UI** | `CharacterSheet.tsx`, Builder, Session, Header | **Pass** — no Hybrid-B in player surfaces. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npx tsc --noEmit` + `npm run build` (wave 59) | **Pass** — exit 0 (~54s combined). |

   - **Wave 59 check post wave 58 — green; P0/P1 clear; no new P2 blockers.** Shipped VQ-22 wild-shape tracker stub (`shapeshiftUsesAtLevel`, `wildShapeCrCap`, `shapeshiftFormsForDruid`; Session uses/CR/form picker + long-rest restore). Shipped VQ-23 overcast tier wiring (`castSpellTier` → `spellCost()` base + surcharge total; **Apply cast spend**). Added Druid L13/L15/L17 draft milestones. LevelFeatureList draft count legend polish. **`npx tsc --noEmit` + `npm run build` green.** **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional. **HANDOFF opening untouched** (append only).

89. **Wave 60 stamp (Session overcast affinity + wild-shape depth + smoke stretch)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Wave 60 touch surfaces** | `spell-utils.js` (`searchSpellsByName`), `druid-shapeshifting.js` (duration/Primal Recovery helpers), `SessionTracker.tsx` (school affinity + spell lookup, duration timer, Primal Recovery), `PLAYTEST_SMOKE.md` | **Pass** — Session UX stubs only; affinity uses existing `schoolAffinityMods`/`spellCost`; no forbidden IP or Hybrid-B UI. |
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. |
   | **Hybrid-B in player UI** | `CharacterSheet.tsx`, Builder, Session, Header | **Pass** — no Hybrid-B in player surfaces. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npx tsc --noEmit` + `npm run build` (wave 60) | **Pass** — exit 0 (~54s combined). |

   - **Wave 60 check post wave 59 — green; P0/P1 clear; no new P2 blockers.** Shipped overcast school affinity depth (spell lookup + school pills → `schoolAffinityMods` in base cost). Shipped wild-shape depth (10 min duration stub, Primal Recovery L13 draft, short-rest reset). PLAYTEST_SMOKE stretch steps for overcast + wild-shape. **`npx tsc --noEmit` + `npm run build` green.** **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional. **HANDOFF opening untouched** (append only).

90. **Wave 61 stamp (class-draft L11–20 gaps + Overcast Burnout hint stub)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Wave 61 touch surfaces** | `class-draft-levels.js` (Mirrorsage L13/L15/L17, Mage L16, Bard L13/L15/L17), `resonance-economy.js` (`overcastBurnoutHintAfterCast`), `SessionTracker.tsx` (post-cast hint line + `burnoutCastHint` persist) | **Pass** — draft milestones + Session UX stub only; no forbidden IP or Hybrid-B UI. |
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. |
   | **Hybrid-B in player UI** | `CharacterSheet.tsx`, Builder, Session, Header | **Pass** — no Hybrid-B in player surfaces. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npx tsc --noEmit` + `npm run build` (wave 61) | **Pass** — exit 0 (~51s combined). |

   - **Wave 61 check post wave 60 — green; P0/P1 clear; no new P2 blockers.** Shipped class-draft L11–20 gap fill (Mirrorsage L13/L15/L17, Mage L16, Bard L13/L15/L17). Shipped post-cast Overcast Burnout concentration hint stub (`overcastBurnoutHintAfterCast` → Session **Overcast check** line after **Apply cast spend**). **`npx tsc --noEmit` + `npm run build` green.** **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional. **HANDOFF opening untouched** (append only).

91. **Wave 62 stamp (Session Ethos picker + Druid L15 arch attunement badge)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Wave 62 touch surfaces** | `resonance-economy.js` (`PLAYER_ALIGNMENTS`), `druid-shapeshifting.js` (`hasArchFormAttunement`, `isFreeArchAttunementSwap`), `SessionTracker.tsx` (Ethos row picker, arch attunement badge + Shift+click attune, free swap tracking) | **Pass** — Session UX stubs only; affinity uses existing `schoolAffinityMods`; no forbidden IP or Hybrid-B UI. |
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. |
   | **Hybrid-B in player UI** | `CharacterSheet.tsx`, Builder, Session, Header | **Pass** — no Hybrid-B in player surfaces. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npx tsc --noEmit` + `npm run build` (wave 62) | **Pass** — exit 0 (~56s combined). |

   - **Wave 62 check post wave 61 — green; P0/P1 clear; no new P2 blockers.** Shipped Session **Ethos row picker** (9-alignment compact pills → overcast affinity smoke without Builder re-add). Shipped Druid **L15 arch attunement** Session badge (2 attuned arch forms via Shift+click; free swap once/encounter between attuned forms; short/long rest reset). **`npx tsc --noEmit` + `npm run build` green.** **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional. **HANDOFF opening untouched** (append only).

92. **Wave 63 stamp (PLAYTEST_SMOKE Burnout stretch + class-draft L13/L15/L17 gaps)**

   | Target | Surfaces scanned | Result |
   |--------|------------------|--------|
   | **Wave 63 touch surfaces** | `class-draft-levels.js` (Cleric/Monk/Ranger/Dragoon/Tinker L13/L15/L17 — 14 milestones), `PLAYTEST_SMOKE.md` (Burnout hint + Ethos + arch attunement stretch rows) | **Pass** — draft milestones + smoke doc only; no forbidden IP or Hybrid-B UI. |
   | **Drow / Umbral Elf / Lolth / Underdark / Undercommon** | Builder/Sheet/Session/Generators UI, `character-storage.js` | **Pass** — **Umbrin** only in live data/UI. |
   | **Hybrid-B in player UI** | `CharacterSheet.tsx`, Builder, Session, Header | **Pass** — no Hybrid-B in player surfaces. |
   | **17 classes / Bloodbound / Oracle RC** | `canon-classes.js` (17), `prestige-lorebook.json`, `spell-utils.js` | **Pass** — unchanged. Oracle uses Revelation Charges, not RP. |
   | **Build hygiene** | `npx tsc --noEmit` + `npm run build` (wave 63) | **Pass** — exit 0 (~48s combined). |

   - **Wave 63 check post wave 62 — green; P0/P1 clear; no new P2 blockers.** Shipped PLAYTEST_SMOKE stretch for **Overcast Burnout hint** (Mage L17+ tier 8+ post-cast RP &lt; 25%), **Ethos row**, and **Druid arch attunement** one-liners. Shipped class-draft L11–20 gap fill: **Cleric/Monk/Ranger/Dragoon L13/L15/L17**, **Tinker L13/L17** (14 draft milestones, Aethel tone). **`npx tsc --noEmit` + `npm run build` green.** **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0**. None reintroduced Drow/Hybrid-B UI leaks or Oracle RP confusion. **34 ASI placeholders** remain intentional. **HANDOFF opening untouched** (append only).



---



## Already in good shape (no change needed)



- **17-class roster** — Monk, Dragoon, Paladin present; Swashbuckler hidden; Fighter archive-only.

- **Paladin oaths** — 10 oaths; **Grief** approved; Mercy + eight others draft revelation lists.

- **Oracle patrons** — Echo Court, War Chorus, Turning Spiral, Hush Beneath the Song, etc.; no Forgotten Realms deities.

- **Prestige feat names** — All requirements resolve to `feats.js` entries.

- **Gate bosses** — Wired and consistent across dungeon JSON.

- **Character save fields** — Builder, Sheet, and `normalizeCharacter()` aligned.



---



## Remaining tensions (author review — do not force-fit)



| Tension | Detail | Recommendation |

|---------|--------|----------------|

| **Oracle draft content** | 9 mysteries (Battle–Time) + 9 curses have full playable Aethel trees marked `draft: true`. Only Ancestor + Spiral-Touched are rulebook-complete. | Author promotes or revises draft tiers; UI already shows "(draft)". |

| **Paladin draft oaths** | 9 of 10 oaths have draft revelation spell lists. | Ingest from `Paladin_Oaths_*.docx` when ready. |

| **Rulebook prose "eighteen"** | **Resolved:** book typo; v1 ships 17 base classes per Classes Table. | Product uses 17 (`canon-classes.js`). |

| **Fighter chapter** | **Resolved:** archive/reference for v1; Warrior/Soldier cover martial roles. | Do not add Fighter to builder. |

| **Swashbuckler orphan** | **Resolved:** orphan in `class-details.js` only; not selectable for v1. | Never expose in picker. |

| **Dungeon cycle entryClasses / victoryConsequences** | **Resolved (Director draft 2026-07-29 overnight):** `dungeon-mechanics.json` — 17 CANON_CLASSES eligible; tier-themed consequences; `draft: true`. | Re-open if rulebook Ch XII restricts entry by class. |

| **Bestiary D&D leakage** | See ~~ASK OWNER #4~~ — **resolved 2026-07-29** (`BESTIARY_SCRUB_LOG.md`). Generic SRD labels (Owlbear, etc.) may remain; no FR deity/setting names in live bestiary. | |

| **Generic spell slot language** | Feats, spells, prestige capstones, Mage hero paths still use "spell slot" for arcane classes. | Correct for Wizard/Mage/Cleric; only Oracle was wrong in product UI. |

| **class-draft-levels.js** | L11–20 milestones for many classes still `draft: true`. | Author review against rulebook tables. |

| **Cosmology First Song** | Single concatenated blob; chapter nav incomplete (IX–XII). | Split extract per existing gap ticket. |

| **Session wild-shape tracker** | Druid forms in Builder; Session does not track uses/CR. | Wire when Session scope expands. |

| **Bloodbound eligibility** | **Resolved (owner 2026-07-29):** Crimson Agent or Thief (Lv 10+) only; Gravetouched removed from requirements. | `prestige-lorebook.json` updated. |



---



## Validation



- `npx tsc --noEmit` — run after TS edits.

- Prestige feat cross-check script: **0 missing feat names** across 18 prestige paths.



---



## Files touched (continuity agent pass)



- `src/data/CONTINUITY_GLOSSARY.md` (new)

- `src/data/CONTINUITY_REPORT.md` (this file)

- `src/components/SessionTracker.tsx`

- `src/components/CharacterSheet.tsx`

- `src/bestiary_data_full.json`

- `final_bestiary.xlsx`

- `scripts/scrub_bestiary_ip.py`

- `docs/mechanics/BESTIARY_SCRUB_LOG.md`



## Files touched (continuity overnight pass, 2026-07-29 PM)



- `docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md` (new)

- `src/data/cosmology-lore.json`

- `src/components/CosmologyViewer.tsx`

- `src/components/SessionTracker.tsx`

- `src/data/CONTINUITY_GLOSSARY.md`

- `src/data/CONTINUITY_REPORT.md`

- `docs/mechanics/WORLD_DUNGEON_LOOP.md`

- `docs/mechanics/CHARGEN_PROGRESSION.md`

- `docs/MECHANICS_BIBLE_STUB.md`

- `docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md` (wave 2 re-rank)

- `docs/MECHANICS_BIBLE_STUB.md`

- `src/components/CharacterBuilder.tsx`

- `src/lib/character-storage.js`

- `src/data/CONTINUITY_GLOSSARY.md`

- `src/data/CONTINUITY_REPORT.md` (this file)



## Files touched (continuity wave 3, 2026-07-29 overnight)



- `src/components/CharacterBuilder.tsx` (dev comment Resonance canon scrub)

- `src/data/CONTINUITY_REPORT.md` (this file — wave 3 scan + green status)

- `docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md` (P0=0 P1=0 header; VQ-27 P2)

---

## Wave 64 continuity stamp — Session Shaman totem tracker (2026-07-30)

**Status:** Green. `SessionTracker` now records Shaman totem placement at L6+, keeps the L13 second-slot behavior explicitly draft-facing, and clears placed totems on long rest. It does not automate effects, damage, duration, or target selection: those still resolve from the selected path and GM ruling.

**L11–20 scan:** Paladin L13/L15/L17, Wizard L13/L15/L17, and Warrior L13/L15/L17 already exist as rulebook/canon entries in `class-details.js`; no overlapping draft milestones added.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0.

---

## Wave 68 continuity stamp — Recovery smoke coverage + Ashen Grove draft labels (2026-07-30)

**Status:** Green. `PLAYTEST_SMOKE.md` now gives the three library recovery states a repeatable zero-result path and checks every transient `burnoutCastHint` recovery exit: Short Rest, Long Rest, and direct **Full** restore. The smoke instructions preserve learned/favorite spell selections and distinguish the transient hint from the calculated Burnout threshold badge.

**Draft content:** The two Circle of the Ashen Grove hero forms now carry an explicit **Draft** badge in the shared class-path display. Their six existing trait blurbs received descriptive context only; no values, ranges, action economy, effects, or form availability changed. Oracle, Paladin, Umbrin, totem automation, and resonance rules remain untouched.

**Validation:** `npx tsc --noEmit` and `npm run build` pending.

### Wave 68 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build completed in ~49s).

---

## Wave 65 continuity stamp — Shaman smoke coverage + hero-form depth (2026-07-30)

**Status:** Green. `PLAYTEST_SMOKE.md` now covers the persisted Shaman tracker end-to-end: one L6 placement/recall, two distinct L13 draft placements with slot enforcement, and long-rest clearing. The check explicitly preserves the GM-resolved boundary for every totem effect.

**Hero-form depth:** Enriched the remaining 13 concise hero-form trait descriptions across Moon, Storm, Thorns, Winterfang, and Rotshaper circles. Existing numbers, ranges, action economy, and effects remain unchanged; this is descriptive depth only.

**Validation:** `npx tsc --noEmit` exit 0.

---

## Wave 66 continuity stamp — Burnout recovery + Items empty state (2026-07-30)

**Status:** Green. Session now clears the transient post-cast `burnoutCastHint` on Short Rest, Long Rest, direct **Full** Resonance restore, and the existing Overcast **Clear** action. The Burnout badge itself continues to reflect the calculated RP threshold; this change does not add consequences or alter Burnout math.

**Items Library:** A zero-result search/filter now renders an explicit, tab-aware empty state with an in-place **Clear all filters** action. Item filtering and selected-item behavior remain unchanged.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0.

---

## Wave 67 continuity stamp — Session fields + library recovery parity (2026-07-30)

**Status:** Green. `CONTINUITY_GLOSSARY.md` now distinguishes persisted Session-only state from Character Builder saves: Shaman `activeTotemIds` remains presence-only and GM-resolved; Druid `attunedArchFormIds` keeps its two-id L15 draft cap; `archAttunementSwapUsed` resets on either rest; Ethos uses the existing nine `PLAYER_ALIGNMENTS`; and `burnoutCastHint` remains a transient reminder with its four documented clear exits.

**Library recovery:** Spells and Bestiary now match Items Library’s actionable zero-results behavior. Spells clears discovery inputs plus the temporary Learned/Favorites view but preserves those stored selections; Bestiary includes search in active-filter state and clears it with dropdown filters. No lore, class, Oracle, Paladin, Umbrin, Totem effect, or Burnout math changes were made.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0.

---

## Wave 69 continuity stamp — Encounters recovery parity (2026-07-30)

**Status:** Green. `EncountersBrowser` now treats its search as active filter state: a result row reports matching tiers and offers **Clear filters**, a global no-match card restores the full encounter view, and query-emptied haven/POI columns expose the same recovery action. The selected-tier handoff and all underlying encounter data are unchanged.

**Scope:** Generators has no filter-driven result set, so no artificial empty state was added. The already-completed Druid hero-form context pass was not duplicated; Oracle, Paladin, Umbrin, totem automation, and gameplay values remain untouched.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~48s).

---

## Wave 77 continuity stamp — prestige smoke + draft provenance (2026-07-30)

**Status:** Green. The smoke guide now verifies World VIII’s existing **Draft** marker and Builder → Sheet persistence for the three previously enriched prestige hallmark badges.

**Prestige draft boundary:** Sapper **Demolition Pack** (index 1) and **Saboteur’s Toolkit** (index 3), plus Soulrender **Echo of Death** (index 3), are explicitly flagged with `draftHallmarkIndices`. The shared Builder and Character Sheet rendering exposes badges only for those entries. No prerequisite, eligibility, numerical effect, capstone, or other prestige mechanic changed.

**Scope:** No Oracle/Paladin/Umbrin review, totem automation, Dungeon Guide empty-state work, source promotion, or 3D work. Commit: none.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~45s).

---

## Wave 70 continuity stamp — Encounter smoke + cosmology draft flavor (2026-07-30)

**Status:** Green. `PLAYTEST_SMOKE.md` now gives Floor Encounters two repeatable recovery checks: `zzzz-wave-70` verifies the global zero-tier card, and T1 `Crystalfront` verifies the POI-only local empty state. Each reset clears only the search, retains the selected tier, and leaves encounter handoff behavior unchanged.

**Draft content:** World sections X (Economy & Trade) and XI (Magic Systems) in `cosmology-lore.json` now visibly carry their existing draft presentation marker. Six short extract labels received flavor-only context while keeping their existing goods, locations, named schools, and all game mechanics unchanged. No rules, spell access, costs, restrictions, Oracle, Paladin, Umbrin, or totem behavior changed.

**Validation:** `npx tsc --noEmit` exit 0; `npm run build` pending.

### Wave 70 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build ~41s). Eight concise labels are enriched under the X/XI draft markers; source facts and rules are unchanged.

---

## Wave 71 continuity stamp — Ashen Grove draft propagation + trade flavor (2026-07-30)

**Status:** Green. Existing `draft: true` metadata on Ashen Grove hero forms now survives each character-facing view: Builder marks the circle and forms, Character Sheet repeats the selected-circle/form status, and Session marks both selectable and active hero forms. The helper exposes source metadata only; it changes no form availability, numbers, traits, action economy, or tracker behavior.

**Draft content:** World X’s already-marked Economy & Trade extract expands only its pre-existing **Divine Essence** and **Shard Markets** labels with presentation flavor. Trade goods, locations, Naegul’s market protection, no-theft rule, and every game rule remain unchanged. Oracle, Paladin, Umbrin, totem automation, and 3D scope remain untouched.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~50s). Commit: none.

---

## Wave 72 continuity stamp — Ashen Grove smoke + legends draft flavor (2026-07-30)

**Status:** Green pending validation. `PLAYTEST_SMOKE.md` now specifies one persisted-Ashen-Grove journey from Builder through refresh, Sheet, and Session. It verifies each existing draft marker remains visible on the selected circle, both hero forms, Session picker, and active-form line, while a non-Ashen circle shows no leaked Ashen/draft marker.

**Draft content:** World section XIII (Legends & Songs) now explicitly carries a draft extract marker. Its three existing source titles remain unchanged; three sub-100-character “Draft color” blurbs add presentation only. No history, character facts, mechanics, class behavior, Oracle, Paladin, Umbrin, or totem work changed.

**Validation:** `npx tsc --noEmit` and `npm run build` pending. Commit: none.

### Wave 72 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build ~43s).

---

## Wave 73 continuity stamp — Appendix draft flavor + Dungeon Guide recovery (2026-07-30)

**Status:** Green. World XV is visibly draft and retains its four source labels exactly; each gets one presentation-only color line. No chronology, divine-lineage, dungeon-reference, calendar, or gameplay fact changed.

**UX recovery:** Dungeon Guide Tier Details now honors the active filter set: when no tier matches, it replaces the stale-detail fallback with a dedicated empty state and **Clear filters** action. Tier selection, filter semantics, and all encounter data remain unchanged.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~47s). Commit: none.

---

## Wave 74 continuity stamp — Dungeon Guide overview recovery smoke (2026-07-30)

**Status:** Green pending validation. When a tier query or mapped-only combination yields no Overview cards, the app now renders an explicit **Clear filters** recovery action rather than passive no-results copy. The reset affects only filter state; selected tier and floor-encounter data remain unchanged.

**Smoke coverage:** `PLAYTEST_SMOKE.md` adds the deterministic `zzzz-wave-74` Overview path and verifies all ten tier cards return while the selected tier is preserved.

**Scope:** No source facts, lore, mechanics, Oracle/Paladin/Umbrin review, totem automation, or 3D work changed. Commit: none.

**Validation update:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~48s).

---

## Wave 75 continuity stamp — Dungeon Guide paired recovery (2026-07-30)

**Status:** Green pending validation. The Dungeon Guide’s existing Tier Details and Overview recovery paths now share a deterministic smoke case: `zzzz-wave-75` combined with **Mapped tiers only** must yield each local empty state, and reset clears only filter state while keeping the selected tier intact.

**Mechanics search:** An impossible query no longer leaves the existing Victory Consequences heading above an unexplained blank list. Its explicit no-match state offers **Clear filters** and restores the same ten source-backed rows. Dungeon data, tier selection, filter matching, and all game mechanics remain unchanged.

**Scope:** No source facts, lore expansion, Oracle/Paladin/Umbrin review, prestige prose, totem automation, or 3D work changed. Commit: none.

**Validation:** `npx tsc --noEmit` and `npm run build` pending.

### Wave 75 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build ~46s).

---

## Wave 76 continuity stamp — Races draft color + prestige hallmark provenance (2026-07-30)

**Status:** Green. World VIII is explicitly a draft extract; its five existing race labels remain intact, with presentation-only color notes that add no ancestry, origin, location, ability, or gameplay facts.

**Prestige draft boundary:** Bloodbound **Bloodletting Strikes**, Forge Master **Ember Pulse**, and Hexblade **Doom Sigil** are individually flagged through `draftHallmarkIndices`. Builder and Character Sheet render the badge only for those entries. Existing mechanics, requirements, eligibility, and capstones remain unchanged.

**Scope:** No Oracle/Paladin/Umbrin review, totem automation, or 3D work. Commit: none.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~48s).

---

## Wave 78 continuity stamp — prestige thin batch + Myth & History draft flavor (2026-07-30)

**Status:** Green pending validation. Hexblade **Blade Hunger** (index 3), Storm Lord **Eye of the Tempest** (index 3), Verdant Animist **Living Terrain** (index 1), and Warlock **Pact Sigils** (index 1) are explicitly marked in `draftHallmarkIndices`. The shared Builder and Character Sheet rendering exposes badges only for those entries. No prerequisite, eligibility, numerical effect, capstone, or other prestige mechanic changed.

**Draft content:** World VII **Myth & History** is now an explicitly draft extract. Its five source labels remain intact and gain presentation-only color lines; chronology, people, places, dungeon facts, and all rules remain source-derived.

**Scope:** No Oracle/Paladin/Umbrin review, totem automation, Dungeon Guide empty-state work, source promotion, or 3D work. Commit: none.

**Validation:** pending.

### Wave 88 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~44s). The exact generic-placeholder scan reports **96** remaining. No commit created.

### Wave 87 validation update

`npx tsc --noEmit` passed (~8s) and `npm run build` passed (~41s). The exact generic-placeholder scan reports **104** remaining. No commit created.

---

## Wave 87 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Battlefield Commander, Battlefield Tactician, Beast Whisperer, Berserker Rage, Bleeding Edge, Blood Magic, Brace for Impact, and Break Line now carry bounded presentation-only descriptions and `draft: true`. The existing Builder feat card branch provides the compact **Draft** badge, and `PLAYTEST_SMOKE.md` records a type-filtered pass for all eight entries.

**Queue:** The exact generic-placeholder scan reports **104** remaining `General feat from the Decennium Descent compendium.` descriptions.

**Boundary:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** pending.

### Wave 86 scan correction

The completed exact-placeholder scan reports **112** remaining descriptions, superseding the earlier provisional **84** figure.

### Wave 86 validation update

`npx tsc --noEmit` passed (~7s) and `npm run build` passed (~47s). No commit created.

---

## Wave 86 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Arcane Recall, Arcane Transfusion, Armor Crusher, and Battle Awareness now carry bounded presentation-only descriptions and `draft: true`. The existing Builder feat card branch provides the compact **Draft** badge, and `PLAYTEST_SMOKE.md` records a type-filtered pass for all four entries.

**Queue:** The exact generic-placeholder scan reports **84** remaining `General feat from the Decennium Descent compendium.` descriptions. The short-effect scan reports **8** draft feats under 80 effect characters; effects remain source fields and are not a prose-enrichment target.

**Boundary:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** pending.

### Wave 85 validation update

`npx tsc --noEmit` passed (~10s) and `npm run build` passed (~43s). No commit created.

### Wave 84 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build ~50s). No commit created.

### Wave 84 hallmark completion update

All **18/18** prestige paths have hallmark records, with none under 80 characters. The two draft entries below the 100-character presentation threshold—Sapper **Saboteur’s Toolkit** and Soulrender **Echo of Death**—now carry longer presentation-only copy; their existing draft indices and all mechanics remain unchanged. Final validation pending.

### Wave 84 final validation

`npx tsc --noEmit` and `npm run build` exit 0 (build ~47s). Final scan: all **18/18** paths contain hallmarks, with **0** below 80 or 100 characters; all **18/18** capstones remain draft-badged. No commit created.

### Wave 83 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build ~47s). The data scan confirms all **18/18** paths have `draftCapstone: true`; **0** remain undrafted. No commit created.

---

## Wave 83 continuity stamp — final prestige capstone draft batch (2026-07-30)

**Status:** Green pending validation. Beastmaster and Chronomancer are explicitly marked `draftCapstone: true`. Builder and Character Sheet use their existing shared badge branch, and `PLAYTEST_SMOKE.md` names the Builder → Sheet provenance path for both. The complete 18-path scan finds **0** prestige capstones without `draftCapstone`.

**Boundary:** The revised text is draft presentation only. No capstone resolution, timing, costs, prerequisites, eligibility, feat behavior, source promotion, or other prestige mechanics changed. No Oracle/Paladin/Umbrin review, totem automation, cosmology/dungeon factual work, or 3D work occurred. Commit: none.

**Validation:** pending.

### Wave 81 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build ~43s). Commit: none.

### Wave 78 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build ~46s).

---

## Wave 79 continuity stamp — prestige capstone draft provenance (2026-07-30)

**Status:** Green. The four shortest prestige capstone candidates — Battlemage, Gravetouched, Hexblade, and Warlock — are explicitly marked `draftCapstone: true`. Builder and Character Sheet render the same compact draft badge only beside those capstone lines; the existing hallmark-index behavior remains unchanged.

**Boundary:** The prose is presentation-only. Capstone resolution, timing, costs, eligibility, requirements, and all source facts remain unchanged. No Oracle/Paladin/Umbrin review, totem automation, cosmology, dungeon, or 3D work occurred. Commit: none.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~41s).

---

## Wave 80 continuity stamp — second prestige capstone draft batch (2026-07-30)

**Status:** Green. The next four shortest undrafted capstones — Sapper, Forge Master, Bloodbound, and Echomancer — are explicitly marked `draftCapstone: true`. Builder and Character Sheet use their shared existing badge branch, so precisely those capstone lines show the compact draft marker; `PLAYTEST_SMOKE.md` names the corresponding Builder → Sheet provenance check.

**Boundary:** The revised text is draft presentation only. No capstone resolution, timing, costs, prerequisites, eligibility, feat behavior, source promotion, or other prestige mechanics changed. No Oracle/Paladin/Umbrin review, totem automation, cosmology/dungeon factual work, or 3D work occurred. Commit: none.

**Queue:** 8/18 capstones are draft-badged; 10 remain undrafted. The next bounded candidates are Wyrmslayer, Verdant Animist, Mooncursed, and Giant Killer.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~47s).

---

## Wave 88 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Bull Rush, Channeled Flow, Cleaving Momentum, Climb Anywhere, Close Quarters Combat, Cold Reader, Combat Intuition, and Combat Slide now carry bounded presentation-only descriptions and `draft: true`. The existing Builder feat-card branch provides the compact **Draft** badge, and `PLAYTEST_SMOKE.md` records a type-filtered pass for all eight entries.

**Queue:** The exact generic-placeholder scan reports **96** remaining `General feat from the Decennium Descent compendium.` descriptions.

**Boundary:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** pending.

---

## Wave 85 continuity stamp — unmapped-depth visibility + feat draft batch (2026-07-30)

**Status:** Green pending validation. Dungeon Guide now displays the existing T6–T10 `draftNote` records in Tier Details with a **Draft extract** badge and warning panel; the note is searchable. `PLAYTEST_SMOKE.md` names a deterministic pass through all five unmapped tiers, requiring their provisional status and scope boundary to remain visible.

**Feat provenance:** Acrobatic Mastery, Arcane Armor, Arcane Flexibility, and Arcane Pulse have presentation-only descriptions derived from their existing prerequisite/effect records, with `draft: true`. Builder displays a compact **Draft** badge for exactly those records.

**Boundary:** T6–T10 remain unmapped; no route, hazard, map, reward, procedure, or encounter-resolution content was added. No feat prerequisite, effect, or automation changed. No Oracle/Paladin/Umbrin review, totem automation, source promotion, 3D work, deletion, or commit occurred.

**Validation:** pending.

---

## Wave 84 continuity stamp — prestige scheduling + unmapped-depth draft extract (2026-07-30)

**Status:** Green pending validation. The completed Wave 83 prestige presentation pass is recorded for morning author scheduling: all **18/18** paths use `draftCapstone`, and **0** capstones remain undrafted. This does not promote, resolve, or otherwise alter capstone mechanics.

**Dungeon boundary:** T6–T10 remain `mapped: false`. Their new `draftNote` records and presentation-only copy restate only the existing tier, haven, POI, gate, and boss labels within survivor-rumor framing. `EncountersBrowser` visibly labels the records **Draft extract** and exposes the scope note; maps, routes, hazards, encounter resolution, rewards, and factual source promotion remain open.

**Scope:** No Oracle/Paladin/Umbrin review, feat/item mechanics, totem automation, or 3D work. Commit: none.

**Validation:** pending.

---

## Wave 81 continuity stamp — third prestige capstone draft batch (2026-07-30)

**Status:** Green pending validation. The next four shortest undrafted prestige capstones—Wyrmslayer, Verdant Animist, Mooncursed, and Giant Killer—are explicitly marked `draftCapstone: true`. Builder and Character Sheet use their shared existing badge branch, so precisely those capstone lines show the compact draft marker; `PLAYTEST_SMOKE.md` names the corresponding Builder → Sheet provenance check.

---

## Wave 82 continuity stamp — fourth prestige capstone draft batch (2026-07-30)

**Status:** Green pending validation. Soulrender, Blademaster, Berserker, and Storm Lord are explicitly marked `draftCapstone: true`. Builder and Character Sheet use their shared existing badge branch, so precisely those capstone lines show the compact draft marker; `PLAYTEST_SMOKE.md` names the corresponding Builder → Sheet provenance check. The remaining undrafted capstones are Beastmaster and Chronomancer. No prerequisite, eligibility, numerical effect, capstone resolution, or other prestige mechanic changed.

### Wave 82 validation update

`npx tsc --noEmit` and `npm run build` exit 0 (build ~42s). Commit: none.

**Boundary:** The revised text is draft presentation only. No capstone resolution, timing, costs, prerequisites, eligibility, feat behavior, source promotion, or other prestige mechanics changed. No Oracle/Paladin/Umbrin review, totem automation, cosmology/dungeon factual work, or 3D work occurred. Commit: none.

**Queue:** 12/18 capstones are draft-badged; 6 remain undrafted. Rescan those six before Wave 82 selects its next bounded batch.

**Validation:** pending.

---

## Wave 83 final continuity append — prestige capstone completion (2026-07-30)

**Status:** Green. Beastmaster and Chronomancer are explicitly marked `draftCapstone: true`; their existing shared Builder and Character Sheet branch presents the compact **draft** badge. The full 18-path data scan reports **0** capstones without `draftCapstone`.

**Boundary:** Presentation-only prose. No capstone resolution, timing, costs, prerequisites, eligibility, feat behavior, source promotion, Oracle/Paladin/Umbrin review, totem automation, cosmology/dungeon factual work, or 3D work changed. No commit created.

**Validation:** `npx tsc --noEmit` and `npm run build` exit 0 (build ~47s).

---

## Wave 88 final continuity append — generic feat draft batch (2026-07-30)

**Status:** Green. Bull Rush, Channeled Flow, Cleaving Momentum, Climb Anywhere, Close Quarters Combat, Cold Reader, Combat Intuition, and Combat Slide are explicitly `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan reports **96** remaining `General feat from the Decennium Descent compendium.` descriptions.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~44s).

---

## Wave 89 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Concentrated Will, Counterspell Adept, Crippling Strike, Cultural Expert, Danger Sense, Diligent Researcher, Disarming Blow, and Disguise Expert now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan reports **88** remaining `General feat from the Decennium Descent compendium.` descriptions.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 89 typecheck and build.

### Wave 89 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **88** remaining. No commit created.

---

## Wave 91 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Ether Anchor, Exploit Weakness, Field Medic, Field Surgeon, Flash Cast, Fleet of Foot, Forensic Investigator, and Foresight Surge now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan reports **72** remaining `General feat from the Decennium Descent compendium.` descriptions.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 91 typecheck and build.

### Wave 91 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **72** remaining. No commit created.

---

## Wave 92 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Herbalist, Illusionist’s Trick, Inspiring Presence, Intuitive Reflex, Jack of All Trades, Librarian's Eye, Lingering Magic, and Lock Savant now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan reports **64** remaining `General feat from the Decennium Descent compendium.` descriptions.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 92 typecheck and build.

### Wave 92 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~44s). The exact generic-placeholder scan reports **64** remaining. No commit created.

---

## Wave 93 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Lunge, Magical Fortitude, Mana Burn, Mental Buffer, Mental Fortress, Merchant’s Guile, Mirror Cast, and Mystic Focus now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan reports **56** remaining `General feat from the Decennium Descent compendium.` descriptions.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 93 typecheck and build.

### Wave 93 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **56** remaining. No commit created.

---

## Wave 95 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Precision Throw, Protective Casting, Punishing Blow, Quick Learner, Quick Recovery, Quick Ritualist, Reckless Swing, and Resilient Mind now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan reports **40** remaining `General feat from the Decennium Descent compendium.` descriptions.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 95 typecheck and build.

### Wave 95 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~42s). The exact generic-placeholder scan reports **40** remaining. No commit created.

---

## Wave 96 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Ritual Channeler, Rogue’s Escape, Runic Scholar, Runic Shield, Savage Momentum, Shattering Smash, Shield Bash, and Shield Expert now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan is expected to report **32** remaining `General feat from the Decennium Descent compendium.` descriptions after validation.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 96 typecheck and build.

### Wave 96 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). The exact generic-placeholder scan reports **32** remaining. No commit created.

---

## Wave 97 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Silent Casting, Silent Movement, Silver Tongue, Skill feats1. Master Tracker, Spell Deflection, Spell Reservoir, Spell Scribe, and Spellweave now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan is expected to report **24** remaining `General feat from the Decennium Descent compendium.` descriptions after validation.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 97 typecheck and build.

### Wave 97 validation update

`npx tsc --noEmit` passed. `npm run build` passed (build ~41s). The exact generic-placeholder scan reports **24** remaining. No commit created.

---

## Wave 98 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Steady Hands, Still Casting, Stubborn Resolve, Sure Shot, Tactical Flanker, Tactical Insight, Target Mark, and Temporal Flux now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge. The malformed Wave 97 display label **Skill feats1. Master Tracker** is normalized to the clearly matching source title **Master Tracker** only.

**Queue:** The exact generic-placeholder scan is expected to report **16** remaining `General feat from the Decennium Descent compendium.` descriptions after validation.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 98 typecheck and build.

### Wave 98 validation update

`npx tsc --noEmit` passed (~7s) and `npm run build` passed (~41s). The exact generic-placeholder scan reports **16** remaining. No commit created.

---

## Wave 99 continuity stamp — generic feat draft batch (2026-07-30)

**Status:** Green pending validation. Tenacity, Tinker Adept, Tough as Nails, Trap Sense, Twin Cast, Unshakeable, Unstoppable Force, and Versatile Artisan now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The canonical exact generic-placeholder scan reports **8** remaining feat records. The raw literal search retains a pre-existing duplicate `master_tracker` description, excluded because wave 98 normalized the matching visible Master Tracker record.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 99 typecheck and build.

### Wave 99 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The canonical exact generic-placeholder scan reports **8** remaining; the raw literal search returns **9** due to the pre-existing duplicate `master_tracker` record. No commit created.

---

## Wave 100 continuity stamp — final generic feat presentation pass (2026-07-30)

**Status:** Green pending validation. Versatile Grip, Volley, Weapon Finesse, Weapon Mastery, Whip Control, Whirlwind Striker, Wilderness Chef, and Wilderness Walker now carry bounded presentation-only descriptions and `draft: true`; the existing Builder feat-card branch presents each compact **Draft** badge.

**Queue:** The exact generic-placeholder scan reports **0** remaining `General feat from the Decennium Descent compendium.` descriptions. The raw literal exception was confirmed as a duplicate: `master_tracker` and `skill_feats1_master_tracker` share name, prerequisite, and effect but have different IDs/types. The still-placeholder `master_tracker` presentation is now drafted; retain both records until the author decides the canonical identity/type.

**Boundary:** Presentation-only copy derived only from existing prerequisite and effect text. No prerequisite, effect, type, selection behavior, or feat automation changed; no Oracle/Paladin/Umbrin review, totem automation, mapped T6–T10 content, source promotion, 3D work, deletion, or commit occurred.

**Validation:** Pending Wave 100 typecheck and build.

**Suggested wave 101:** obtain the Master Tracker canonical-record decision, then take a bounded source-backed encounter, dungeon, or generator playtest pass.

### Wave 100 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **0** remaining. No commit created.

---

## Wave 101 continuity stamp — Session rest feedback (2026-07-30)

**Status:** The Session horn-clock action that only advances time now reads **Advance +8h**. Short and Long Rest provide an accessible status summary after applying their existing character-track changes; no recovery formula or rest outcome changed.

**ASK OWNER (morning):** `master_tracker` and `skill_feats1_master_tracker` remain a duplicate pair with matching visible name/prerequisite/effect but different IDs/types. Both records must remain until the owner chooses the canonical record/type; do not infer or apply a resolution.

**Boundary:** No Oracle/Paladin/Umbrin author-tone review, content-table invention, mapped T6–T10 dungeon work, deletion, or commit occurred.

**Validation:** Pending Wave 101 typecheck and build.

### Wave 101 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). No commit created.

---

## Wave 102 continuity stamp — Floor Encounter handoff choice (2026-07-30)

**Status:** Floor Encounters can now stage an existing specific Point of Interest or Safe Haven in Session. The selected entry replaces only its corresponding `Site` or `Fallback haven` line; tier, floors, gate boss, draft-depth warning, and the other default line remain intact. The tier-level action now makes its default-entry behavior explicit.

**Smoke:** The appended smoke path checks non-default POI and haven handoffs plus the distinction between a time-only **Advance +8h** and the outcome feedback from Short/Long Rest.

**ASK OWNER (morning):** `master_tracker` and `skill_feats1_master_tracker` remain untouched until the owner decides the canonical record/type.

**Boundary:** No Oracle/Paladin/Umbrin author-tone review, encounter-table invention, mapped T6–T10 dungeon work, recovery-rule change, deletion, or commit occurred.

**Validation:** Pending Wave 102 typecheck and build.

### Wave 102 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~47s). No commit created.

---

## Wave 103 continuity stamp — Generator pack handoff guardrails (2026-07-30)

**Status:** Generators now requires a visible, previously built pack before enabling its Session handoff. It sends that exact pack; switching tiers clears the old output and disables the action until the new tier is built, eliminating stale-tier handoff ambiguity.

**Smoke:** `PLAYTEST_SMOKE.md` adds deterministic pack-first, tier-change freshness, Session banner, and clipboard-feedback checks. Browser execution remains pending because the IDE browser was unavailable during this run.

**Boundary:** No content tables, encounter generation, mapped T6–T10 dungeon work, Oracle/Paladin/Umbrin author-tone review, deletion, source promotion, 3D work, or commit occurred. The duplicate `master_tracker` / `skill_feats1_master_tracker` records remain untouched pending owner direction.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~47s).

---

## Wave 104 continuity stamp — Bestiary foe handoff (2026-07-30)

**Status:** Bestiary detail now offers **Add foe in Session**. It stages the selected source creature’s name, listed HP, CR, and zone, opens Session, and adds exactly one editable foe with a confirmation banner. Initiative, combat state, conditions, and all encounter resolution remain table-facing.

**Smoke:** `PLAYTEST_SMOKE.md` appends a deterministic Bestiary-to-Session check alongside the still-pending Wave 102 selected-entry and Wave 103 Generator checks.

**Boundary:** No monster or encounter tables, mapped T6–T10 content, Oracle/Paladin/Umbrin author-tone review, deletion, source promotion, 3D work, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending the owner’s canonical-record decision.

**Validation:** Pending Wave 104 typecheck and build.

### Wave 104 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). The existing `SessionTracker` exhaustive-deps warnings remain non-fatal; no commit created.

---

## Wave 105 continuity stamp — Session saved-character refresh discoverability (2026-07-30)

**Status:** Session now labels its existing browser-local saved-character source, shows each addable hero’s class and level, and reports the refreshed count after **Refresh saved list**. Adding a hero still creates an editable encounter copy; later character edits remain in Characters.

**Boundary:** The empty state gives the real recovery path—**CHARACTERS → SAVE → SESSION → Refresh saved list**—and explicitly says Session has no JSON-import action. No character storage shape, payload semantics, automated inventory, encounter resolution, content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin review, deletion, or commit changed.

**Smoke:** `PLAYTEST_SMOKE.md` appends saved-list return, refresh-feedback, and import-boundary checks. Browser execution remains pending alongside the Bestiary selected-foe and Generator pack handoffs because browser attachment is unavailable.

**Validation:** Pending Wave 105 typecheck and build.

**Suggested wave 106:** Browser-smoke the saved-list path plus pending Bestiary, selected POI/haven, and Generator paths; then take one source-bounded Session usability gap only if demonstrated.

### Wave 105 validation update

`npm run build` passed (~44s) with the two existing non-fatal `SessionTracker` exhaustive-deps warnings. `npx tsc --noEmit` then passed (~9s); its initial concurrent run raced Next’s `.next` generation and was rerun after the build. No commit created.

---

## Wave 106 continuity stamp — Spell cast-preview handoff (2026-07-30)

**Status:** The Spell Library can now stage a selected spell’s existing name, school, tier, casting time, range, and duration in Session. The Session preview points players back to the existing caster spell lookup and Overcast controls; it does not select a caster, spend RP, add combatants, resolve a cast, or alter saved-character data.

**Boundary:** This is reference handoff only. Oracle remains a Revelation Charge class, not a Weave caster; the existing Oracle spell-list reference warning remains unchanged. No character storage schema, automated inventory, content table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit changed.

**Smoke:** `PLAYTEST_SMOKE.md` adds deterministic spell-preview arrival and manual-resolution boundary checks. Browser execution remains non-blocking while attachment is unreliable.

**Validation:** Pending Wave 106 typecheck and build.

**Suggested wave 107:** Browser-smoke the saved-character refresh and spell-preview paths with the still-pending Bestiary, POI/haven, and Generator handoffs when attachment is available; otherwise take one narrow Session usability gap using existing sources only.

### Wave 106 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~54s). The two existing non-fatal `SessionTracker` exhaustive-deps warnings remain. No commit created.

---

## Wave 107 continuity stamp — Items reference-preview handoff (2026-07-30)

**Status:** Green pending build. The Items Library can stage an existing selected item’s name, rarity, tier, category, source type, and description in Session. The Session banner is reference-only: it leaves Scene notes, inventory, saved characters, resources, combatants, acquisition, crafting, and use under manual GM/table control.

**Smoke:** `PLAYTEST_SMOKE.md` adds deterministic dropped/crafted preview arrival and no-auto-inventory/manual-resolution checks. Browser execution remains non-blocking while attachment is unreliable.

**Boundary:** No item, loot, crafting, encounter, or dungeon source tables changed. No inventory/RP automation, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending owner direction.

**Validation:** `npx tsc --noEmit` passed. `npm run build` pending.

### Wave 107 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). The existing two non-fatal `SessionTracker` exhaustive-deps warnings remain; no behavior-changing warning refactor was made. No commit created.

---

## Wave 108 continuity stamp — Session filter clarity + handoff suite (2026-07-30)

**Status:** Session now exposes the visible-versus-total combatant count whenever its existing crowded-table filter or collapsed-foes view hides rows. This is presentation-only: combatant state, initiative order, turn state, and all table resolution remain unchanged.

**Smoke:** `PLAYTEST_SMOKE.md` consolidates the saved-character, spell, item, Bestiary foe, selected POI/haven, and Generator Session arrivals into one repeatable handoff-suite pass. Each existing boundary remains explicit: no character-save mutation, automated inventory, RP spend, cast resolution, or encounter resolution.

**Hook assessment:** ESLint still reports two `applyPendingHandoffs` exhaustive-deps warnings. A one-line dependency addition is not safe because the local function is recreated on render and could reapply handoffs; no suppression or behavior-changing refactor was made.

**Boundary:** No source tables, storage schema, automated inventory, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (~48s). The production build repeats only the two documented non-fatal `SessionTracker` exhaustive-deps warnings.

---

## Wave 109 continuity stamp — hidden active-turn recovery (2026-07-30)

**Status:** When a Combatants filter or crowded-foes collapse hides the active combatant, the existing warning now provides **Show active turn**. It switches to that combatant's side filter and opens foes when required so the existing highlighted row is visible again.

**Smoke:** `PLAYTEST_SMOKE.md` appends filtered-ally and collapsed-foe checks. The action is presentation-only: it does not mutate combatants, initiative, turn/round state, or table resolution.

**Boundary:** No source tables, character storage, inventory automation, RP/cast automation, encounter resolution, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two existing `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 109 typecheck and build.

**Suggested wave 110:** Browser-smoke the consolidated handoff suite and active-turn recovery if available; otherwise take only another narrow state-preserving Session friction pass.

### Wave 109 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). Production build repeats only the two intentional non-fatal `SessionTracker` exhaustive-deps warnings; no commit created.

---

## Wave 110 continuity stamp — Session notice and empty-table recovery (2026-07-30)

**Status:** Session now offers **Dismiss all notices** only when multiple arrival banners are open, closing those local notices without mutating handoff payload outcomes, Scene notes, combatants, tier, horn time, resources, or initiative state. Its empty Combatants state now gives the existing entry routes and makes that preservation boundary visible before the table starts.

**Smoke:** `PLAYTEST_SMOKE.md` appends stacked-arrival dismissal and empty-table orientation checks. Browser execution remains non-blocking.

**Boundary:** No source tables, character storage, inventory automation, RP/cast automation, encounter resolution, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two existing `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 110 typecheck and build.

**Suggested wave 111:** Smoke Waves 109–110 in-browser when available. Otherwise pursue only one additional narrow state-preserving Session or Builder clarity gap.

### Wave 110 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentional non-fatal `SessionTracker` exhaustive-deps warnings; no commit created.

---

## Wave 111 continuity stamp — Character Sheet printable draft-badge parity (2026-07-30)

**Status:** Prestige hallmark and capstone markers now use the existing shared Sheet **Draft** badge, so their draft provenance persists in print preview just like the Sheet’s other draft callouts.

**Smoke:** `PLAYTEST_SMOKE.md` appends an existing-prestige onscreen-to-print-preview verification. Wave 110’s stacked-notice dismissal and empty-table orientation rows remain pending browser execution; that browser work is non-blocking.

**Boundary:** No prestige source data, prerequisite, capstone, character storage, Session state, inventory automation, RP/cast automation, encounter resolution, content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 111 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 112 continuity stamp — Session dismissal confirmation (2026-07-30)

**Status:** Stacked arrival-notice dismissal now leaves accessible feedback that states how many local notices closed and names the unaffected Session state: Scene notes, combatants, tier, horn time, turn, round, and resources. A later existing handoff clears that stale feedback so the active arrival notice remains authoritative.

**Smoke:** `PLAYTEST_SMOKE.md` adds dismissal-confirmation and fresh-arrival-reset checks. Browser execution remains non-blocking while attachment is unavailable.

**Boundary:** This is presentation feedback only; it does not alter handoff payload outcomes, stored table state, character storage, inventory, RP/cast resolution, encounter resolution, source tables, or content. No T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 112 typecheck and build.

**Suggested wave 113:** Browser-smoke Waves 109–112 when attachment is available; otherwise take only another narrow existing-state Session or Builder clarity improvement.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 123 continuity stamp — Hero-path reference clarity (2026-07-30)

**Status:** Builder and printable Sheet now show a bounded explanation when the existing class reference contains no hero-path entries, replacing a blank display area without inferring a hero path or a progression outcome. Existing arch-path cards remain visible.

**Smoke:** `PLAYTEST_SMOKE.md` appends the Builder → save → Sheet/print path-reference check and a compact Wave 122 Cosmology draft-notice confirmation. Browser execution remains non-blocking.

**Boundary:** No hero-path/class source data, progression, save, Resonance, Cosmology, dungeon, Session, inventory/RP/cast automation, encounter, or content rule changed. No content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Suggested wave 124:** Browser-smoke the Wave 123 rows when available; otherwise preserve the narrow existing-state Builder/Sheet clarity lane and leave author review, Session hooks, inventory automation, and dungeon design closed.

### Validation update

`npx tsc --noEmit` passed; `npm run build` passed in ~41s. Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 122 continuity stamp — Cosmology draft-extract visibility (2026-07-30)

**Status:** Existing `draft` / `draftNote` records in Cosmology’s World of Aethel and First Song collections now have a tab-level **Draft extract** notice before selection, in addition to their existing † picker marker and per-section provenance panel. This is presentation only; no lore text, rule, source record, or authority boundary changed.

**Smoke:** `PLAYTEST_SMOKE.md` provides a deterministic World → First Song visibility check and retains Wave 121 feat-filter recovery plus saved/blank People & traits Sheet-print coverage. Browser execution remains non-blocking.

**Boundary:** No cosmology/dungeon content table, T6–T10 mapped material, feat/people/trait/class/Resonance/storage rule, Session behavior, inventory/RP/cast automation, encounter resolution, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** `npx tsc --noEmit` passed; `npm run build` passed in ~42s with only the two intentionally deferred `SessionTracker` exhaustive-deps warnings. No commit created.

---

## Wave 121 final continuity stamp — Hero-state clarity (2026-07-30)

**Status:** Builder feat filtering now recovers from an explicit no-match name/type combination. Sheet trait display is sourced solely from the existing saved people record and existing data; no traits are inferred.

**Boundary:** No people, feat, prerequisite, effect, storage, class, Resonance, Session, automation, source-table, cosmology, dungeon, or content rule changed. No author-tone review, mapped T6–T10 work, deletion, or commit occurred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (~51s); only the two intentionally deferred `SessionTracker` hook warnings remain.

---

## Wave 121 continuity stamp — People traits and feat-filter recovery (2026-07-30)

**Status:** The Builder’s Feats view now makes a zero-match search/type combination recoverable without selecting or changing a feat. The printable Character Sheet derives a compact people/lineage trait summary only from the existing saved record and race source data, and names blank or unresolved state rather than inferring traits.

**Smoke:** `PLAYTEST_SMOKE.md` appends no-match filter and Builder → save → Sheet/print checks. Browser execution remains non-blocking while attachment is unavailable.

**Boundary:** No people, trait, feat, prerequisite, effect, class, Resonance, character-storage, Session, inventory/RP/cast automation, encounter, cosmology, dungeon, or source-table rule changed. No content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 121 typecheck and production build.

**Suggested wave 122:** Browser-smoke the Wave 121 rows when available. Otherwise, make one small draft-marker consistency pass across existing Cosmology/Dungeon surfaces only, leaving owner decisions, author tone, Session hooks, and automation closed.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 120 continuity stamp — Oracle Mystery and Curse recorded-state parity (2026-07-30)

**Status:** Existing blank `oracleMystery` and `oracleCurse` state now has an explicit Builder and printable Character Sheet boundary: **No Oracle Mystery recorded** / **No Oracle's Curse recorded**. The presentation preserves existing L1 timing, required markers, **Draft** badges, and Character Builder recovery; it does not infer a Mystery or Curse or grant a feature.

**Smoke:** `PLAYTEST_SMOKE.md` appends blank-both and one-recorded-selection Builder → save → Sheet/print checks. Browser execution remains non-blocking while attachment is unavailable.

**Boundary:** No Mystery or Curse source data, Oracle rule, revelation, boon, class feature, storage, progression, Session, inventory/RP/cast, or encounter rule changed. No content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 120 typecheck and production build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~49s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

**Suggested wave 121:** Browser-smoke Waves 118–120 recorded-state rows when available; otherwise defer further Oracle presentation work until author review rather than extending this lane.

---

## Wave 119 continuity stamp — Sacred Oath recorded-state parity (2026-07-30)

**Status:** Existing blank `sacredOath` state now has an explicit Builder and printable Character Sheet boundary: **No Sacred Oath recorded**. The presentation preserves the existing L3 timing, required marker, and Character Builder recovery route; it does not infer an oath or grant a feature.

**Smoke:** `PLAYTEST_SMOKE.md` appends L1 blank and L3 required Builder → save → Sheet/print checks. Browser execution remains non-blocking while attachment is unavailable.

**Boundary:** No oath source data, oath rule, class feature, storage, progression, Session, inventory/RP/cast, or encounter rule changed. No content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 119 typecheck and production build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~55s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

**Suggested wave 120:** Browser-smoke Wave 118 Ethos and Wave 119 Sacred Oath recorded-state rows when available; otherwise retain one narrow existing-state Builder clarity lane, preferably Oracle empty-state presentation parity without rules or content changes.

---

## Wave 118 continuity stamp — Ethos recorded-state parity (2026-07-30)

**Status:** Existing `alignment` save state now has an explicit blank-state presentation boundary in Builder and on the printable Character Sheet. Builder identifies its existing save/spell-cost-preview use; Sheet prints **Ethos not recorded** until the saved value exists. No new ethos data or mechanical interpretation was introduced.

**Smoke:** `PLAYTEST_SMOKE.md` now provides blank-state and selected-state Builder → save → Sheet/print checks. Browser execution remains non-blocking while attachment is unavailable.

**Boundary:** No ethos option/source table, spell-cost calculation, character-storage shape, class, feature, Resonance, Session, inventory/RP/cast, or encounter rule changed. No content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 118 typecheck and production build.

**Suggested wave 119:** Browser-smoke Waves 116–118 when available; otherwise retain the narrow source-bounded Builder clarity lane.

### Validation update

`npx tsc --noEmit` passed. `npm run build` passed in ~42s; production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 117 continuity validation update (2026-07-30)

`npx tsc --noEmit` passed. `npm run build` passed in ~41s; it reports only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 116 continuity stamp — Prestige-path intent clarity (2026-07-30)

**Status:** Builder’s Class-tab Arch-path selection now distinguishes recorded player intent from granted progression. Its existing Paths-tab requirements and draft provenance remain authoritative; no prerequisite, feature, or progression behavior was changed.

**Smoke:** `PLAYTEST_SMOKE.md` adds a Class → Paths verification that confirms the intent boundary and the existing requirements/badges. Browser execution remains non-blocking while attachment is unavailable.

**Boundary:** No prestige source data, class, Resonance, character-storage, Session, inventory/RP/cast, or encounter rule changed. No content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~49s); production build repeats only the two existing `SessionTracker` exhaustive-deps warnings.

**Suggested wave 117:** Browser-smoke Waves 114–116 when available; otherwise retain the narrow source-bounded Builder clarity lane.

---

## Wave 115 continuity stamp — Sheet print provenance (2026-07-30)

**Status:** Printable Character Sheets now retain three existing-state clarity signals: the complete draft multiclass RP-merge breakdown, an explicit no-second-Weave-pool note for recorded secondary classes, and legible draft-milestone legend/per-feature badges.

**Smoke:** `PLAYTEST_SMOKE.md` appends print-preview checks for eligible Weave merges, non-Weave secondaries, and draft level features. These remain presentation checks only.

**Boundary:** No class, feature, multiclass, Resonance, or save-data rule changed. No Session behavior, inventory/RP/cast automation, encounter resolution, content table, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 115 typecheck and production build.

**Suggested wave 116:** Browser-smoke Wave 114–115’s Builder → Sheet → print continuity when possible; otherwise, take only another documented narrow Builder clarity gap using existing state.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 113 continuity stamp — Session filtered-table recovery (2026-07-30)

**Status:** A populated Session table now recovers from an empty Allies/Foes display filter with an explicit no-match explanation and **Show all combatants**. Recovery resets only display state and expands the existing foes view; stored/table-facing state remains unchanged.

**Smoke:** `PLAYTEST_SMOKE.md` adds empty-Foes-view and state-preservation checks. Browser execution remains non-blocking while attachment is unavailable.

**Boundary:** This is presentation-only. It does not alter handoff outcomes, combatants, initiative, turn/round, scene context, character storage, inventory, RP/cast resolution, encounter resolution, source tables, or content. No T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The two `SessionTracker` hook warnings remain intentionally deferred.

**Validation:** Pending Wave 113 typecheck and build.

**Suggested wave 114:** Browser-smoke Waves 109–113 when attachment is available; otherwise take only another confirmed narrow state-preserving presentation improvement.

---

## Wave 117 continuity stamp — Sheet prestige-path intent parity (2026-07-30)

**Status:** The existing saved `archClass` presentation now carries the same intent-only boundary in Builder and on the printable Character Sheet. Existing prestige requirements and draft provenance remain present; no progression is inferred or granted.

**Smoke:** `PLAYTEST_SMOKE.md` now gives one Builder → Sheet → print check for the selected path, the intent note, and existing requirements/draft badges. Browser execution remains non-blocking while attachment is unavailable.

**Boundary:** No prestige source data, prerequisite, feature, class, Resonance, character-storage, Session, inventory/RP/cast, or encounter rule changed. No content tables, mapped T6–T10 material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. Existing `SessionTracker` hook warnings remain deferred.

**Validation:** Pending Wave 117 typecheck and production build.

**Suggested wave 118:** Browser-smoke Wave 117 when available; otherwise retain the narrow, source-bounded existing-state Builder clarity lane.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook continuity stamp — Umbrin migration (2026-07-30)

**Status:** `rulebook_output.txt` is confirmed as the living rulebook extract. Its race chapter, ability summary, and language list now use **Umbrin** throughout (38 legacy Drow-era references migrated). The new chapter aligns to the approved product terms **The Murk**, **Murkish**, **Umbrin Magic**, and **Obsidian Highborn**.

**Provisional canon:** The Calan'thir / First Choir exile and **Obsidian Burn** remain explicitly author-reviewed lore, not a new racial mechanic. Companion `draft: true` status remains unchanged.

**Migration boundary:** Active companion data contains no Drow-era product copy; `character-storage.js` intentionally retains Drow/Umbral Elf aliases solely to migrate old saves to Umbrin.

**Suggested next rulebook wave:** Reconcile this extract against the full rulebook source, then author-review one bounded Oracle mystery or Paladin oath before promoting its draft status.

---

## Rulebook continuity stamp — Oath of Grief tone pass (2026-07-30)

**Source status:** `rulebook_output.txt` is the editable living extract. The full `decennium descent player rulebook.docx` is present but was not edited in this wave; its Peoples wording still requires a deliberate document-sync pass.

**Delivered:** The draft **Oath of Grief** received a bounded prose pass: its theme, summary labels, and conduct clauses now use solemn rulebook language for remembrance and passage. The existing rules text, numbers, prerequisites, and revelation list are unchanged; `draft: true` remains in force.

**Author queue:** Review the Oath of Grief's mechanics and revelation wording for final promotion; decide the Obsidian Burn motive/theology, Umbrin naming examples, and Murk-cult terminology; then sync approved Umbrin Peoples copy to the docx.

---

## Rulebook continuity stamp — docx assessment + Oath of the Chain (2026-07-30)

**Docx boundary:** The player-rulebook docx is present and `python-docx` is installed, but no binary edit occurred: the available safe edit path cannot provide the required paragraph-scoped backup and post-save comparison. The document remains unchanged. `rulebook_output.txt` is still the sole living Umbrin source, so the Peoples sync remains explicitly outstanding.

**Draft continuity:** The **Oath of the Chain** gained rulebook-voice presentation only: its theme and three conduct clauses describe a freely borne vigil, steadfast wards, and sacrifice without coercion. Smite, aura, signature power, revelation spells, oathbreaker text, final gift, numeric values, and `draft: true` remain unchanged.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

**Next:** Treat the docx sync as an isolated backup → verified Peoples paragraph replacement → new text extract → Umbrin chapter diff task before accepting any document save.

---

## Rulebook continuity stamp — guarded Umbrin docx sync (2026-07-30)

**Status:** The full player-rulebook docx now matches the approved Umbrin migration in its Peoples copy and related rulebook references. A beside-source pre-sync backup exists as `decennium descent player rulebook.pre-umbrin-backup.docx`; no commit was created.

**Scope:** The sync replaced the Drow-era race heading, prose, traits, variants, magic label, language, ability-summary, language-list, and scattered NPC reference copy with **Umbrin**, **The Murk**, **Murkish**, **Umbrin Magic**, and **Obsidian Highborn**. It also inserts the existing extract's explicitly provisional Obsidian Burn author-review note and removes the legacy external name lists.

**Verification:** The edited docx reopened with `python-docx`; all approved Umbrin markers are present and no whole-word `Drow` reference remains. The unrelated word “drowsy” remains untouched. No mechanics or companion data changed.

**Suggested next:** Author-review the provisional Obsidian Burn theology and supply Umbrin naming examples before any further Peoples expansion; keep any Oracle mystery tone pass `draft: true`.

---

## Rulebook continuity stamp — Cataclysm mystery tone pass (2026-07-30)

**Delivered:** The draft **Cataclysm** mystery now frames its existing destructive role and **The Unbound Wound** capstone in bounded rulebook voice: destruction as a perilous path through what cannot endure. Its charges, range, duration, damage, immunity, Exhaustion, patron, and every other Revelation mechanic are unchanged.

**Draft boundary:** Cataclysm continues to receive `draft: true` through `draftMysteryRevelations`; this is presentation-only and is not a promotion to canon.

**Author queue:** Review Cataclysm's full draft tree before promotion; separately decide Obsidian Burn theology and provide Umbrin naming examples. No new theology, name list, or Umbrin lore was invented here.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Player class balance audit stamp (2026-07-30)

**Audit only:** Added `docs/mechanics/BALANCE_PLAYER_CLASSES.md`, a player-facing 17-class balance review grounded in the rulebook extract and companion data. It keeps Fighter archived and Swashbuckler non-selectable, uses Aethel terminology, treats Hybrid-B multiclassing as approved canon, and marks unverified mechanics as draft or missing.

**Continuity risks surfaced:** Companion and rulebook armor/proficiency entries conflict for Crimson Agent, Dragoon, Mirrorsage, Oracle, and Tinker. Several high-impact class systems—Mirrorsage copying, Oracle RC triggers, Paladin Oaths, Warrior mutations, and Tinker deployables—lack enough final numeric/action constraints for balance claims; no class mechanics were changed or promoted.

---

## Owner-ruling continuity stamp — Umbrin canon decisions (2026-07-30)

**Locked:** Umbrin continuity flows from the **Obsidian Burn** through **The Murk**, **Blackglass Reach**, **Veyr-Obsid**, and the **Quiet Deep**. Alliances remain transactional; the dark-glass underworld is not a foreign dark-elf setting.

**Resolved:** `master_tracker` is the only selectable **Master Tracker** (Skill; Survival 4+, Wisdom 13+; track +10); its General clone is retained as deprecated data for historical saves. The Hybrid-B Resonance multiclass merge is approved canon. **Mystery of Shadow** and **Oath of Grief** are the sole owner-approved Mystery/Oath promotions; all remaining Mysteries, Oaths, and Curses retain their existing draft state, including the complete **Spiral-Touched** curse benchmark.

**Names:** Canon examples are Vaerith, Sythra, Korven, Zelka, Dravik, Nyssara, Kethren, and Vorskai; Houses Veyr, Ashketh, Rhal-Voss, and Obis-Keth establish the Veyr-Obsid dark-glass register.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~74s). The build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Continuity stamp — locked Umbrin geography (2026-07-30)

**Canon:** **The Murk** (region/approach), **Blackglass Reach** (surface and near-Murk marches), **Veyr-Obsid** (primary Umbrin city), and **the Quiet Deep** (deeper underworld) are locked as Proposal 1. Obsidian Burn theology is canon.

**Alliance posture:** Surface distrust rooted in betrayal and cult association remains the default; any Umbrin alliance is tentative, transactional, and self-serving rather than redemption by default.

**Guardrails preserved:** No Umbrin personal-name list was added. No Mystery, Oath, or Curse changed draft state; Master Tracker and Resonance remain unresolved. The rulebook extract and editable docx were synchronized from this lock, with a pre-geography docx backup. No companion data changed, so typecheck/build were not required.

---

## Midnight continuity stamp — author decision pack (2026-07-30)

**Status:** Added [`AUTHOR_REVIEW_QUEUE.md`](../../docs/mechanics/AUTHOR_REVIEW_QUEUE.md) as the authoritative coffee-prep decision surface. It records the existing provisional Obsidian Burn material without expanding theology, asks the owner for Umbrin naming examples without inventing a list, and points to Resonance multiclass §7.

**Draft continuity:** `feats.js` contains two retained Master Tracker records: `master_tracker` (`Skill`, selectable) and `skill_feats1_master_tracker` (`General`, `deprecated: true`). **Grief** is the sole promoted Sacred Oath (`draft: false`); **Mercy** remains `draft: true` in companion despite rulebook prose.

**Validation:** Documentation-only append; build intentionally skipped. No commit or mass deletion occurred.

---

## Rulebook continuity stamp — Oracle curse tone pass (2026-07-30)

**Draft continuity:** All nine draft Oracle curse profiles now use bounded rulebook voice in their profile blurbs and limitations. Their IDs, names, effects, boon trees, values, costs, ranges, durations, damage, unlock levels, and explicit `draft: true` status remain unchanged. **Spiral-Touched** remains the sole rulebook-complete curse tree.

**Queue:** The independent curse tone-pass queue is **0 remaining**. The current content state is one complete example plus **9** unpromoted draft curse trees.

**Author handoff:** Resolve Obsidian Burn theology, Umbrin naming examples, the Master Tracker duplicate, and the Resonance multiclass draft before promotion work. Review each completed draft individually before moving it from `draft` to approved.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`; no commit or deletion occurred.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook continuity stamp — final five-profile tone pass (2026-07-30)

**Draft continuity:** **Battle** now frames command and fury as a charge carried for the company, while **Bones** treats death as an unfinished account owed care rather than a possession. **Oath of Dominion**, **Oath of Flame**, and **Oath of the Ancients** now state their existing themes and conduct clauses in bounded rulebook voice: authority is accountable, cleansing fire is restrained, and ancient covenants are guarded with humility.

**Rules preserved:** Battle and Bones changed only theme, combat role, and reputation; their shared `draft: true` provenance, patrons, full Revelation trees, costs, ranges, durations, damage, values, and progression remain unchanged. The three Oaths changed only theme, conduct clauses, and author-review source wording; smites, auras, signature powers, revelation spells, oathbreaker entries, final gifts, values, selection timing, and explicit `draft: true` remain unchanged.

**Queue complete:** The remaining tone-pass queue is **0**. No Obsidian Burn theology or Umbrin names were invented, and no profile was promoted.

**Author handoff:** Resolve Umbrin lore author blockers, then undertake the separate curse-tone review. For the next overnight pass, use the coffee checklist to confirm each draft remains clearly labeled and no author-only lore has entered player-facing text.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook continuity stamp — Oath of Chains Broken tone pass (2026-07-30)

**Draft continuity:** The **Oath of Chains Broken** now has presentation-only, rulebook-voice wording for its existing theme and conduct clauses. It treats liberation as both the breaking of unjust bonds and the continuing protection of those released. Smite, aura, signature power, revelation spells, oathbreaker text, final gift, numeric values, and `draft: true` are unchanged.

**Source boundary:** Direct Cataclysm comparison against the workspace's `rulebook_output.txt` is pending. No contradictory reading, rule adjustment, or draft promotion has been inferred.

**Author queue:** **14** untouched `draft: true` Oracle Mystery / Sacred Oath profiles remain. Oath of Silence is the next smallest Paladin pass; separately, Obsidian Burn theology and Umbrin naming examples remain author decisions. No new theology or name list was invented here.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`; no commit or deletion occurred.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

**Cataclysm spot-check update:** `rulebook_output.txt` confirms the source-level Cataclysm theme, battlefield-control/area-damage role, and feared/suspect reputation. It presents a full Revelation tree only for Ancestor, so the Cataclysm tree retains `draft: true`; no contradiction was found.

---

## Rulebook continuity stamp — Martyr King oath + Flame mystery tone pass (2026-07-30)

**Draft continuity:** The **Oath of the Martyr King** now frames its existing theme and conduct clauses as accountable stewardship: leadership is a burden freely taken, never an excuse to spend others for glory. Smite, aura, signature power, revelation spells, oathbreaker text, final gift, numbers, and explicit `draft: true` remain unchanged.

**Thin follow-up:** The **Flame** mystery now gives its existing theme, battlefield role, and reputation bounded rulebook voice about conviction, costly mercy, and decisive fire. Patron, full Revelation tree, charge costs, ranges, durations, damage, and shared `draft: true` provenance remain unchanged.

**Author queue:** **10** untouched draft Mystery/Oath profiles remain. Review both completed profiles before any promotion; do not invent Obsidian Burn theology or Umbrin names without author direction.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook continuity stamp — Shadow + Time Oracle mystery tone pass (2026-07-30)

**Draft continuity (historical — Shadow promoted 2026-07-30):** **Shadow** now describes disciplined silence, concealment, and fear used to seize a controlled opening. **Time** now describes measured delay and reversal that gives the party one meaningful chance to act. These were presentation-only profile passes. **Shadow** was subsequently owner-promoted (`draft: false`); **Time** remains draft. Patron trees, costs, ranges, durations, damage, numbers, and progression were unchanged by the tone pass.

**Queue reconciliation:** The Life + Stars audit established a verified seven-profile queue. Shadow and Time reduce it to **5** untouched profiles: **Battle**, **Bones**, **Oath of Dominion**, **Oath of Flame**, and **Oath of the Ancients**.

**Author boundary:** No Obsidian Burn theology or Umbrin names were invented; neither mystery was promoted. Take **Bones** next, preserve `draft: true`, and author-review each completed tree before promotion.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## DM XP / encounter audit stamp (2026-07-30)

Added [`BALANCE_DM_XP.md`](../../docs/mechanics/BALANCE_DM_XP.md). The available rulebook extract has no XP/CR/encounter-budget chapter; current XP/CR values, CR-tier filtering, and gate-boss HP are companion behavior only. Session has no XP award ledger, calculator, or write-back, and T6–T10 remain unmapped.

---

## Combat simulation stamp (2026-07-30)

Added [`BALANCE_COMBAT_SIM.md`](../../docs/mechanics/BALANCE_COMBAT_SIM.md) and runnable `scripts/combat-balance-sim.mjs`. Source-stat simulations flag the L3 Bloom guardian as too hot under an explicit provisional CR damage proxy and the L8 Vaskor guardian as hard but survivable; final damage and XP balance remain unknown because monster attacks and an XP-award formula are absent. No encounter rules, Umbrin/Aethel lore, or Hybrid-B mechanics were invented.

---

## XP advancement provenance stamp (2026-07-30)

Added [`XP_ADVANCEMENT_CANON.md`](../../docs/mechanics/XP_ADVANCEMENT_CANON.md). The editable player-rulebook docx and its text mirror confirm XP-based L1–L20 advancement thresholds and total-character-level multiclass progression. XP awards, sharing, Bestiary XP provenance, CR-to-XP, encounter budgets, party adjustments, gate-boss rewards, and the combat simulation's CR damage proxy remain unverified or blocked. The Builder's conflicting threshold table remains legacy-unverified; no data or behavior was wired, promoted, or silently treated as canon.

---

## XP advancement gap-fill — Worker 1 / 5 (2026-07-30)

**Confirmed wiring:** Character Builder Advancement now reads `CANON_XP_THRESHOLDS` from `src/lib/xp-economy.js` (rulebook L1–L20 cumulative XP). Legacy inline thresholds (500 / 1,500 / … / 256,000) removed.

**Draft wiring:** `xp-economy.js` exports `draftXpForCr`, `splitPartyXp`, `draftEncounterBudget`, and related helpers — all marked `draft: true` / DRAFT OWNER per `XP_ADVANCEMENT_CANON.md`. Session exposes **Award draft XP** on defeated foes (0 HP): appends a labeled Scene-notes line and increments per-ally `draftXpSession`; does **not** upsert character saves or promote Bestiary `xp`.

**Not wired:** Encounters difficulty calculator, automated level-up, Bestiary XP canon, character-save XP write-back.

**Validation:** `npx tsc --noEmit` — run at handoff. No commit.

---

## Oversight Phase A — detailed continuity check (2026-07-30)

**Agent:** Oversight (1) of 6 (5 workers + oversight).  
**Deliverable:** [`docs/mechanics/CONTINUITY_DETAILED_CHECK.md`](../docs/mechanics/CONTINUITY_DETAILED_CHECK.md)

**Gate snapshot:** A–G **pass with noted drift** — Gate C checklist stale on Mercy (data still `draft: true` vs glossary “canon”) and Shadow/Grief promotions; Gate G conditional on `MonstersLibrary.tsx` tsc. T6–10 remain draft/unmapped.

**Queue snapshot:** Continuity VQ **P0 = 0 · P1 = 0 · P2 open** (VQ-15–25). Balance **P0 open** (provenance labels, executable combat schema, class caps, test harness). XP Worker 1 partial land: canon thresholds in Builder + draft Session awards; docs still lag on Builder conflict paragraph.

**Contradictions flagged:** Mercy oath draft vs canon label; stale multiclass “still draft” wave-63 line; Shadow tone-pass stamp predates owner promotion; midnight “all oaths draft” vs Grief promoted.

**Worker watchlist:** XP write-back boundaries, bestiary re-ingest + tsc, class caps/recharges, T6–T10 draft guardrails — re-verify in Oversight Phase B after workers land. No commit.

---

## Monster recharge gap-fill — Worker 4 / 5 (2026-07-30)

**Scope:** Expand combat beyond at-will for gate guardians + CR-band samples; Excel-first.

| Deliverable | Status |
|-------------|--------|
| `Bestiary.xlsx` recharge columns | **Done** — 8 columns after Combat Provenance |
| Draft recharge rows | **26 creatures** (10 gate guardians + 16 CR-band samples; 1 duplicate Xarog Excel name skipped) |
| `ingest_bestiary_from_excel.py` | Maps recharge columns → `combat.attacks[]` with `usage: recharge` |
| `src/lib/monster-combat.mjs` | `expectedRechargeDpr()`, `totalExpectedMonsterDpr()`, documented assumptions |
| `scripts/combat-balance-sim.mjs` | Includes recharge expected DPR when authored |
| `docs/mechanics/BALANCE_COMBAT_SIM.md` | Worker 4 rerun + impact table |
| `docs/mechanics/MONSTER_COMBAT_SCHEMA.md` | Recharge sim assumptions documented |

**Sim impact (draft):** Bloom **63.7% → 93.2%** party loss with Spore Burst recharge; Vaskor **46.8% → 58.2%** (still in 40–70% band). All results remain `draft: true`. No commit.

---

## Oversight Phase B — worker re-check complete (2026-07-30)

**Agent:** Oversight (1) · **Verdict:** **Pass with drift**

**Workers verified:** W1 XP (canon Builder thresholds + session-local draft awards) · W2 Bestiary (430 Excel QA rows, 708 JSON stable) · W3 class ceiling caps (doc + `class-ceiling-caps.js` + Builder/Sheet callouts) · W4 combat recharge (26 payloads; sim Bloom **93.2%**, Vaskor **58.2%**) · W5 T6–T10 draft seeds (`mapped: false` preserved).

**Gate C Mercy fix:** Glossary, Gate C checklist, and VQ-16 updated — **Mercy `draft: true`** in companion (not promoted); **Shadow + Grief** remain sole Mystery/Oath promotions. Hybrid-B multiclass = **approved canon** (historical wave-63 “still draft” superseded).

**Validation:** `npx tsc --noEmit` clean; `node scripts/combat-balance-sim.mjs` smoke pass. **Balance P0:** partially advanced (W3/W4); award canon + full effect enforcement still open.

**Deliverable:** [`docs/mechanics/CONTINUITY_DETAILED_CHECK.md`](../docs/mechanics/CONTINUITY_DETAILED_CHECK.md) Phase B section. No commit.

---

## Oversight Phase C — continuity cleanup complete (2026-07-30)

**Agent:** Oversight (1) · **Verdict:** **Clean pass**

**Drift cleared:** Mercy canon labels (docs only — data stays `draft: true`); Shadow/Grief promotion counts; Resonance multiclass “still draft” in current handoff; XP Builder legacy threshold claims; Shadow tone-pass stamp superseded by promotion.

**Bloom retune (Excel-first):** Spore Burst **1d8 poison** (DC 14), recharge **6** only — was **4d6 / 5-6** (93.2% L3 sim). Post-ingest sim: Bloom **68.4%**, Vaskor **58.2%** (both in 40–70% band).

**Validation:** `npx tsc --noEmit` clean; combat sim smoke pass; **708** bestiary rows stable. **No** mass oath/mystery promotion; **no** Mercy promotion.

**Deliverable:** [`docs/mechanics/CONTINUITY_DETAILED_CHECK.md`](../docs/mechanics/CONTINUITY_DETAILED_CHECK.md) Phase C section. No commit.

---

## T4 expedition continuity watch — EXP-T4-01 post-sim (2026-07-30)

**Agent:** Continuity Watcher (playtest subdivision) · **Verdict:** **Pass with drift**

**Sim:** **Complete** (`EXP-IER-T4-01`) — play report + issues log (50 items). **Architect charter not executed:** sim used **fallback roster** (Sunward Lance / Prism Watch / Dawn's Anvil) because scenario/roster missing at sim time; architect files now present (Dawn Concord / Mirror Guild / Choir Covenant, 17/17 classes).

**Pass:** T4 zone/POIs, good/neutral ethos, Umbrin **Sunlight Sensitivity** + sun-shield supply, Gor Vekk **200 HP manifestation** + retreat (not CR 29 kill), draft XP labeling, horn 106/120 h, class ceiling caps exercised (Paladin/Warrior/Mirrorsage/Oracle).

**Drift:** Fallback vs architect roster (**14/17** classes; **Aasimar/Halfling/Warforged** non-companion races); Glassbite persona/name carryover (Vesper, Kael, Mira, Greta, …); shortened goals (**no Radiance Gate F40** install); different encounter ladder; RP/slots confusion; sandbox *Aberrant Lash* on Deva; alignment affinity not applied; playtest ID mismatch.

**Sim validity:** Partial — T4 mechanics + zone stress test only; **re-run on architect roster** before sign-off.

**Deliverable:** [`docs/playtest/T4_WATCH_CONTINUITY.md`](../docs/playtest/T4_WATCH_CONTINUITY.md). No commit.

---

## Decennial opening window — owner lock (2026-07-30)

**Agent:** Continuity · **Verdict:** **Drift cleared in docs**

**Locked:** Decennial opening duration = **100 days / 2400 hours** when the Shardspire activates and the Great Descent accepts entry. **Distinct from** the **120-hour horn** (in-run underground clock in `dungeon-mechanics.json` / Session UI).

**Drift source:** `The Decennium Descent and the Matrix of Oblivion.docx` § "The 240-Hour Descent" — **240 h treated as typo** (missing zero). Extract corrected; `.docx` on disk **unchanged**.

**Companion gap:** No `openingDuration` field in JSON; horn math **unchanged** at 120 h. Nesting of horn inside 100-day window **pending owner clarification**.

**Deliverable:** [`docs/mechanics/DESCENT_WINDOW_CANON.md`](../docs/mechanics/DESCENT_WINDOW_CANON.md). No commit.

---

## Silent Ones / Pact — owner lore lock (2026-07-30)

**Agent:** Continuity · **Verdict:** **GM-secret stratum added**

**Locked (owner 2026-07-30):**

1. **Silent Ones** — unknown to world and typical PCs.
2. Silent Ones built the dungeon **with loot** to **attract** people → **discover** → **release** them.
3. **The PACT** — keep Silent Ones **silent**; **entice war as dissonance**; **Matrix of Oblivion centralized** here (maps to Divine Pact in Matrix extract unless owner renames).
4. World **peace** → **Old Ones awaken** → **silence the universe again**.

**Reconciliation:** Calan'thir / Asmodeus / Crucible / Divine Pact citations **retained** as **public myth layer**; owner lock is **secret truth stratum**. **Open:** Silent Ones vs Old Ones identity; public vs secret builders; loot-bait vs Pact resonance engine.

**Guardrail:** Silent Ones **not** in player-facing newcomer guides.

**Deliverables:** [`docs/mechanics/SILENT_ONES_CANON.md`](../docs/mechanics/SILENT_ONES_CANON.md) · Owner lock § in [`docs/playtest/DUNGEON_CREATION_PURPOSE.md`](../docs/playtest/DUNGEON_CREATION_PURPOSE.md) · continuity note on [`docs/playtest/MATRIX_OF_OBLIVION_EXTRACT.md`](../docs/playtest/MATRIX_OF_OBLIVION_EXTRACT.md). No commit.

---

## Owner cosmology locks — round 2 (2026-07-30, same date)

**Agent:** Continuity (owner lock) · **Verdict:** **Round-1 open questions resolved; one (Level 97 Old God) explicitly left open**

Same-day follow-up: the owner directly answered the open questions raised by the two locks immediately above.

| Q | Ruling | Effect |
|---|--------|--------|
| **Q1** | "Silent Ones ARE the Old Ones (same)." | Resolves round-1 open question — **same entity**, no subset/warden split. |
| **Q2** | "'The Pact' is shorthand for the Divine Pact — the agreement between heavens and hell manifested to keep the Old Ones hidden." | Confirms identity, **no rename**. |
| **Q3** | Public: Calan'thir & Asmodeus built the dungeon (Crucible/Calan'thir's Trial), joint Order+Hell monument, virtually everyone accepts joint creation. Secret: Silent Ones/Old Ones built the actual machinery (**Heartcell** — 100-floor resonance, ten Gate divisions, opening cycle, reward architecture); Calan'thir & Asmodeus discovered/claimed/modified/activated/bound themselves to it, did not invent it. Treasure is bait; expeditions serve the machine. Formulation: "The Silent Ones built the prison. Calan'thir and Asmodeus taught the world to call it a dungeon." Player knowledge: public myth is the complete explanation at start; truth is discoverable via floor contradictions, never commonly known. | Resolves authorship split cleanly — **two true layers, not competing myths.** New term locked: **Heartcell**. |
| **Q4** | Opening = 2400h/100 days. Horn = **1200h / day 50 = point of no return**. Soft quit Floor 50 Canticle ≠ Horn. | **Aligned** in [`DESCENT_WINDOW_CANON.md`](../docs/mechanics/DESCENT_WINDOW_CANON.md). Session `HORN_AT = 1200` and `hornRule` purged 2026-07-31 ([`OPENING_CLOCK_PURGE_2026-07-31.md`](../docs/mechanics/OPENING_CLOCK_PURGE_2026-07-31.md)). |
| **Q5** | Appendix B (`rulebook_output.txt`, "The Lore of Aethel") kept as **mortal folk religion, not objective canon** — do not reconcile literally into Spiral/Choir/Old Ones. Rename toward "Faiths and Cosmologies of Aethel" with disclaimer. Fifteenfold Pantheon = worship masks; First Choir stays exactly 7; Lumina/Umbra = theological abstractions; Great Wheel = mortal diagram; Blood War rewritten per owner's sequence; locked 7-rung hierarchy (Spiral → Old Ones/Ul'nak → Heartcell → Calan'thir & Asmodeus → First Choir(7) → Fifteenfold Pantheon → Cultural gods/ascended). | New deliverable: [`docs/mechanics/APPENDIX_B_FOLK_RELIGION.md`](../docs/mechanics/APPENDIX_B_FOLK_RELIGION.md). **Rulebook text itself not patched — logged as TODO**, not silently rewritten. |
| **Q6** | Level 97 Old God. | **RESOLVED 2026-07-31.** Owner: **Floor 97 = regular zone with hidden chamber (Old Ones sleep); true conquest L100 boss → focusing crystal → weaken Old God; else L30 mind-control near wipe.** Do not equate with Interstice; do not invent further mechanics. |
| **Q7** | Use bestiary names for gate guardians (live roster); formally retire older Velkyrion/Zeharra/Kharix-style cosmology names where they conflict. | Formalizes `WORLD_DUNGEON_LOOP.md` WDL-1's existing practice; Cosmology XIV gate-boss list (Hollow King/Cindervore/Vox Prime) retirement is now **final**, not just a draft flag. |

**Files touched (docs only):** [`docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md`](../docs/mechanics/OWNER_COSMOLOGY_LOCKS_2026-07-30.md) (new) · [`docs/mechanics/SILENT_ONES_CANON.md`](../docs/mechanics/SILENT_ONES_CANON.md) · [`docs/mechanics/DESCENT_WINDOW_CANON.md`](../docs/mechanics/DESCENT_WINDOW_CANON.md) · [`docs/playtest/DUNGEON_CREATION_PURPOSE.md`](../docs/playtest/DUNGEON_CREATION_PURPOSE.md) · [`docs/mechanics/APPENDIX_B_FOLK_RELIGION.md`](../docs/mechanics/APPENDIX_B_FOLK_RELIGION.md) (new) · [`docs/playtest/A_TO_Z_MASTERY_DIGEST.md`](../docs/playtest/A_TO_Z_MASTERY_DIGEST.md) · [`docs/playtest/READY_TO_CONTINUE.md`](../docs/playtest/READY_TO_CONTINUE.md) · [`docs/mechanics/CONTINUITY_DETAILED_CHECK.md`](../docs/mechanics/CONTINUITY_DETAILED_CHECK.md) · annotation-only pointers added to `WORLD_DUNGEON_LOOP.md`, `NEWCOMER_GM_GUIDE.md`, `HIDDEN_DUNGEON_EQUATION.md`, `SESSION_LOOP.md`, `COMBAT_SYSTEM_COMPARE.md`.

**Code/data:** **Purged 2026-07-31.** `HORN_AT = 1200`; `hornRule` teaches day-50 PoNR. Historical playtest sim logs (SIM_02/04, T4_* series) that reference 120h remain dated archives of sessions run under the pre-purge UI.

No commit/push per brief.

---

## Expedition structure — owner re-assertion (2026-07-30)

**Agent:** Continuity (owner lock) · **Verdict:** **RAW confirmed and locked**

| Topic | Resolution |
|-------|------------|
| **Source** | `rulebook_output.txt` § **Expeditions in Aethel** lines **3801–3926** (mirror: `feat_compendium_output.txt` **3802–3926**); original `decennium descent player rulebook.docx` |
| **RAW cap** | **Up to 12 characters per Expedition** — total organizational roster, **not** combat party size |
| **Teams** | Combat **4–6** · Reconnaissance **1–3** · Research **1–3** · Resource **2–4** · Support **1–3** |
| **Day structure** | **Morning / afternoon / evening** periods; per-period assignment; multi-period activities |
| **Also in RAW** | Skill checks, activity results, three examples, base camps, advancement, parallel resolution (Quick / Scene / Parallel / Between-session), organizational-structure conclusion |
| **Companion JSON** | `dungeon-mechanics.json` → `expedition` — **aligned subset** (maxSize, teams, timePeriods); prose-only elements not in JSON |
| **UI** | `DungeonGuide.tsx` displays JSON; **Session UI has no team/period assignment** — product gap, not built |
| **Playtest drift** | T4 **24 PC (3×8)** = director/playtest coalition exception, **not RAW**; campaign sims **7–8 PC** = valid under cap; recommend multi-expedition coordination for larger forces |

**Deliverable:** [`docs/mechanics/EXPEDITION_STRUCTURE_CANON.md`](../docs/mechanics/EXPEDITION_STRUCTURE_CANON.md) · cross-links in `DESCENT_WINDOW_CANON.md`, `WORLD_DUNGEON_LOOP.md`, `A_TO_Z_MASTERY_DIGEST.md`, `READY_TO_CONTINUE.md` (lock **K**), `NEWCOMER_GM_GUIDE.md`, `SIM_CAMPAIGN_PLAN.md`, `SESSION_LOOP.md` · stamps in `CONTINUITY_DETAILED_CHECK.md`. **No** `src/` code changes. No commit/push per brief.

---

## Rulebook source-of-truth process (2026-07-30)

**Agent:** Continuity (process lock) · **Verdict:** **Hierarchy locked; override questions open**

| Item | Detail |
|------|--------|
| **Deliverable** | [`docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md`](../docs/mechanics/CONTINUITY_SOURCE_OF_TRUTH.md) |
| **Cursor rule** | `.cursor/rules/continuity-rulebooks.mdc` (`alwaysApply: true`) |
| **Priority** | Owner lock → Player Rulebook / DM Manual (published) → companion → playtest sims |
| **Player Rulebook** | `decennium descent player rulebook.docx` · `rulebook_output.txt` (UTF-16LE) · `feat_compendium_output.txt` · `tools/oracle_rulebook_extract.txt` |
| **DM Manual layer** | **No file named "DM Manual"** — Matrix, Cosmology, World of Aethel, Floor Encounters docx + extracts |
| **Override gate** | STOP + owner question **(a) rulebook text (b) proposed change (c) options** before editing published sources |
| **ASK OWNER (override)** | Q-OV-1 Horn **resolved** (2400/1200) · Q-OV-2 expedition **resolved** (**12 max**; T4 24-PC = playtest only) · Q-OV-3 Appendix B **patched** · Q-OV-4 Silent Ones **resolved** (DM-01 Ch 8) · Q6 Level 97 **resolved** (regular zone + hidden chamber; L100→crystal→weaken Old God; else L30 wipe — **not** whole-floor “hidden zone”). Drift: **ReviewBible always wins**. SoT split still **OPEN** — full text in CONTINUITY_SOURCE_OF_TRUTH §5 |

No rulebook/DM `.docx` or extract edits this pass. No commit/push per brief.