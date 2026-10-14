# Overnight Vague Queue — Continuity (2026-07-29)

**Agent:** Continuity (overnight)  
**Sources:** `CONTINUITY_REPORT.md`, `SESSION_LOOP.md`, `WORLD_DUNGEON_LOOP.md`, `RESONANCE_CANON.md`, `CONTENT_GAPS.md`, `CHARGEN_PROGRESSION.md`  
**Protocol:** Resolve from existing canon only. Escalate true lore contradictions to Director/Owner. Do not commit.

**Snapshot (wave 3, 2026-07-29 overnight):** **P0 = 0** · **P1 = 0** · open **P2** below only.

---

## P0 — Play truth & terminology (resolve first)

| ID | Vague item | Canonical answer | Status |
|----|------------|------------------|--------|
| **VQ-01** | Cosmology XIV gate bosses (Hollow King Lv10, Cindervore Lv30, Vox Prime Lv70) vs live dungeon table | **Director decided (2026-07-29 overnight):** `floor-encounters.json` + `dungeon-mechanics.json` `gateBosses[]` win for play. Cosmology XIV marked `[superseded by Dungeon Guide]` — non-authoritative draft. | **Resolved** |
| **VQ-02** | Oracle pool label — RP vs Revelation Charges | Oracle uses **Revelation Charges (RC)** only; excluded from Weave RP (`spell-utils.js`). Session shows RC column; Builder Weave tab shows Oracle guidance. | **Resolved** (prior pass) |
| **VQ-03** | Weave spellcasting system name | **Director decided (2026-07-29):** player-facing name is **Resonance / Resonance Points (RP)**. "Hybrid-B" = internal doc label only. **"Song of the Weave" rejected** as system name — flavor prose only. | **Resolved** |
| **VQ-04** | "Eighteen classes" rulebook prose vs 17-row Classes Table | **Owner decided (2026-07-29):** book typo; v1 ships **17 base classes** (`canon-classes.js`). Fighter archive-only; Swashbuckler orphan/hidden. | **Resolved** |
| **VQ-05** | Bloodbound prestige base classes | **Owner decided (2026-07-29):** Crimson Agent or Thief (Lv 10+) only — **Gravetouched removed** from Bloodbound requirements. | **Resolved** |

---

## P1 — Data gaps & session stubs (GM can improvise; companion should flag)

| ID | Vague item | Current stance | Next action |
|----|------------|----------------|-------------|
| **VQ-06** | Gravetouched prestige (#10) — no base class definition | Prestige path exists in `prestige-lorebook.json` (Cleric/Warrior/Crimson Agent Lv 10+). Not a Bloodbound prereq. Feat blurbs may stay thin/draft. | **Resolved (wave 2, 2026-07-29)** — closed as false escalation (ASK OWNER #6); prestige-only path, hero-path wiring may proceed. |
| **VQ-07** | `dungeon-mechanics.json` `entryClasses` / `victoryConsequences` | Director draft-filled 2026-07-29 overnight: 17 CANON_CLASSES eligible; tier-themed `byTier` consequences; both `draft: true`. | **Resolved (wave 2, 2026-07-29)** — ASK OWNER #5 closed; re-open only if rulebook Ch XII restricts entry by class. |
| **VQ-08** | Tiers 6–10 POI/haven lists | **Resolved (wave 3, 2026-07-29):** survivor-rumor stubs filled for tiers 6–10 in `src/data/floor-encounters.json` (1 haven + 2 POIs each; `mapped: false`, GM improv flagged). | Author ingest from Floor Encounters deep docs when available; Generators usable now. |
| **VQ-09** | Session HP import formula | **Resolved (wave 4, 2026-07-29):** `estimatePcMaxHp()` uses rulebook Ch3 HD via `class-hit-dice.js` (L1 max die + CON; higher levels avg die + CON per level; all 17 CANON_CLASSES). Stored `hp`/`maxHp` still preferred. | Closed — multiclass HP split not modeled on import. |
| **VQ-10** | Session rest economy (RP/RC refresh) | **Resolved (wave 3, 2026-07-29):** Short/Long rest buttons in `SessionTracker.tsx`; `applyShortRest` / `applyLongRest` in `session-utils.ts` use `shortRestRecovery` / `longRestRecovery` from `resonance-economy.js` (¼ RP retune + Oracle RC +1 short; full RP/RC long; long adds +8h horn). | Closed — re-open only if rest table contradicts rulebook. |
| **VQ-11** | Party RP pool default | **Resolved (wave 3, 2026-07-29):** Director default = sum of living Weave casters' max RP via `sumWeaveCasterMaxRp()` in `session-utils.ts`; auto-sync on character load and long rest in `SessionTracker.tsx`. | Closed — manual Spend/Gain 1 RP buttons remain for table fiat. |
| **VQ-12** | Multiclass RP formula | **Resolved (wave 4, 2026-07-29):** `mergeMulticlassMaxRp()` in `resonance-economy.js` — highest caster-tier pool + ⌈25% secondary⌉ per RESONANCE_CANON §7. `defaultMaxRp` / `resolveMaxRp` accept `secondaryClass` + `secondaryLevel` or `classLevels` on character save. | Closed — formula remains `draft: true`; re-open if Ch6 slot table conflicts. |
| **VQ-13** | CHARGEN `ASK OWNER` table stale rows | Rows 1–3 (eighteen/Fighter/Swashbuckler) still listed as open in `CHARGEN_PROGRESSION.md`. | **Resolved overnight** — table updated to match owner rulings. |
| **VQ-14** | Race IP rename (Drow → **Umbrin**, etc.) | **Umbrin** is current product name (late 2026-07-29). Umbral Elf was interim; companion + bestiary aligned (`races.js`, `builder-races.js`, `bestiary_data_full.json`, migration in `character-storage.js`). Lore: `UMBRIN_LORE.md`. | **Resolved (2026-07-29 PM)** — rulebook docx still says Drow; author re-ingest ticket. |

---

## P2 — Author review & polish (not blocking playtest)

| ID | Vague item | Notes |
|----|------------|-------|
| **VQ-15** | Oracle mysteries/curses (8 of 10 draft) | Playable Aethel trees with `draft: true`; Ancestor + **Shadow** approved; Spiral-Touched rulebook-complete. |
| **VQ-16** | Paladin oaths (8 of 10 draft) | **Grief** approved; **Mercy** remains `draft: true` in companion (rulebook prose exists, not promoted); 8 others pending author review. |
| **VQ-17** | L11–20 class progressions | `class-draft-levels.js` milestones marked Draft; author review vs rulebook tables. |
| **VQ-18** | Cosmology First Song chapters | Single blob; chapter nav IX–XII incomplete — split extract ticket. |
| **VQ-19** | Feats compendium reconciliation | 336 live vs 330-title doc; placeholder descriptions; unwired legacy feat files. |
| **VQ-20** | Global header search | Non-functional input — client index over existing data only. |
| **VQ-21** | Reputation → RP auto-apply | Hybrid-B puts Academic/Religious/Arcane/Nature modifiers in scope; **not yet wired** in companion. |
| **VQ-22** | Session Druid wild-shape tracker | Forms in Builder; Session does not track uses/CR. |
| **VQ-23** | Overcast / Burnout UI | Phase 2 stub in `resonance-economy.js`; no Builder/Session panel yet. |
| **VQ-24** | Horn clock overrun penalty | **1200 h / day 50** PoNR → 10-year trap is narrative; no in-session mechanical penalty table. Lane A design question. |
| **VQ-25** | Level 97 Old God vs tier/floor math | Myth anchor (Binding of the Old God); not an encounter index — **WDL-4** watch only. |
| **VQ-26** | MECHANICS_BIBLE_STUB open TBD rows | Rows #2 (17 classes), #3 (bestiary IP), and #7 (`entryClasses`) were stale — updated wave 2. | **Resolved (wave 2, 2026-07-29)** |
| **VQ-27** | Legacy root companion still says Drow | Pre-Next.js `index.html` + `game-data.js` (unwired per `CONTENT_GAPS.md`) still expose Drow race id/copy. Next.js product path uses **Umbrin** only. | **Resolved (2026-07-29)** — root `index.html` + `game-data.js` scrubbed to **Umbrin** (id `umbrin`, Murkish, Obsidian Highborn, lore aligned to `races.js`). |

---

## Overnight resolutions applied (2026-07-29 PM)

1. **VQ-01 / WDL-1:** Cosmology XIV `draftNote` → `[superseded by Dungeon Guide]`; Cosmology viewer banner updated; CONTINUITY_REPORT ASK OWNER #7 closed (Director decided).
2. **VQ-03:** SessionTracker RP tooltip scrubbed — removed "Hybrid-B canon" from player-facing title.
3. **VQ-05:** Confirmed `prestige-lorebook.json` Bloodbound base class string; glossary + CHARGEN cross-refs aligned.
4. **VQ-13:** CHARGEN_PROGRESSION ASK OWNER table — rows 1–3 marked resolved; Gravetouched row clarified (prestige #10, not Bloodbound prereq).
5. **Glossary:** Added **Revelation Charges (RC)** abbreviation row; Oracle RC separate from RP reaffirmed.
6. **VQ-14:** Race rename complete — **Umbrin** in People picker (Umbral Elf interim, superseded late 2026-07-29); legacy Drow / Umbral Elf saves migrate on load; rulebook docx re-ingest pending.

## Overnight resolutions applied (wave 2, 2026-07-29)

7. **VQ-06:** Gravetouched ASK OWNER #6 closed — false escalation; prestige #10 complete in `prestige-lorebook.json`; not a Bloodbound prereq.
8. **VQ-07:** `entryClasses` / `victoryConsequences` marked resolved — Director draft in `dungeon-mechanics.json`; ASK OWNER #5 closed.
9. **VQ-26:** `MECHANICS_BIBLE_STUB.md` §7 rows #3 and #7 updated to resolved.
10. **Glossary wave 2:** Added **Lumina** row; Umbra vs Umbrin distinction tightened; agent checklist item 8 (no "Umbral Elf" as current).
11. **Oracle RC vs RP UI:** `CharacterBuilder.tsx` spell cost badge — removed "Hybrid-B" from player-facing tooltip (parity with SessionTracker wave 1).
12. **Legacy migration:** `character-storage.js` — added `umbral-elf` / `drow` id aliases → Umbrin on load.
13. **Bloodbound scan:** `prestige-lorebook.json` #4 confirmed Crimson Agent or Thief (Lv 10+) only — no Gravetouched coupling in product data.
14. **Cosmology XIV banner:** Verified — `cosmology-lore.json` `draft: true` + `CosmologyViewer.tsx` superseded banner; no additional conflicts found.
15. **MECHANICS_ROADMAP.md:** Director Status #3 and overnight wave notes updated — **Umbrin** current (Umbral Elf interim only).

## Overnight resolutions applied (wave 3, 2026-07-29 — verified)

16. **VQ-08:** Tiers 6–10 POI/haven arrays no longer empty — survivor-rumor stubs in `src/data/floor-encounters.json` (tiers 6–10: `safeHavens[]`, `pointsOfInterest[]`, boss names wired).
17. **VQ-10:** Rest economy wired — `SessionTracker.tsx` `runShortRest` / `runLongRest` + UI buttons; `session-utils.ts` `applyShortRest` / `applyLongRest`; Oracle RC scaling via `maxRevelationCharges()`.
18. **VQ-11:** Party RP pool default = sum of Weave caster max RP — `session-utils.ts` `sumWeaveCasterMaxRp()` / `sumWeaveCasterCurrentRp()`; `SessionTracker.tsx` sync on load + long rest.

**Still open after verification:** None — VQ-09 and VQ-12 closed wave 4 (2026-07-29).

---

## Overnight resolutions applied (wave 4, 2026-07-29)

19. **VQ-09:** Rulebook HP formula wired — `src/data/class-hit-dice.js` (17 CANON_CLASSES HD from Ch3 table); `estimatePcMaxHp()` in `session-utils.ts` delegates; `SESSION_LOOP.md` updated.
20. **VQ-12:** Multiclass RP merge — `parseMulticlassLevels()`, `mergeMulticlassMaxRp()` in `resonance-economy.js`; `defaultMaxRp` / `resolveMaxRp` multiclass-aware; SessionTracker + CharacterSheet pass character save fields when present.

## Overnight resolutions applied (wave 5, 2026-07-29)

21. **VQ-27:** Legacy root companion Drow scrub — `index.html` (`data-race="umbrin"`) + `game-data.js` (`umbrin` key, Umbrin Magic / Weapon Training, Murkish, Obsidian Highborn, lore blurb aligned to `races.js`).

---

## Escalation (true contradictions only)

| Item | Why escalate | Do not |
|------|--------------|--------|
| Cycle `entryClasses` if rulebook Ch XII restricts classes | Would override Director draft (all 17 eligible) | Re-open without source text |
| Multiclass RP if numbers clash | Could break chargen balance | Ship a merged formula without owner |

---

## Remaining P0–P1 (wave 3 snapshot, 2026-07-29)

**P0:** None — all resolved (VQ-01 through VQ-05).

**P1 (open):** None — all P1 items resolved (VQ-06 through VQ-14; VQ-09/12 closed wave 4).

~~**P1 (open):**~~

| ID | Item | Next action |
|----|------|-------------|
| ~~**VQ-09**~~ | ~~Session HP import stub formula~~ | **Resolved wave 4** — `class-hit-dice.js` |
| ~~**VQ-12**~~ | ~~Multiclass RP formula draft only~~ | **Resolved wave 4** — `mergeMulticlassMaxRp()` |

**P1 resolved (wave 3):** VQ-08 (tier 6–10 rumor stubs), VQ-10 (rest RP/RC wired), VQ-11 (party RP sum default).

---

## Quick reference — play sources of truth

| Topic | Source |
|-------|--------|
| Gate bosses / tiers | `floor-encounters.json`, `dungeon-mechanics.json` |
| 17 classes | `canon-classes.js` |
| Oracle magic | `oracle-mysteries.js`, `oracle-curses.js` — RC not RP |
| Weave magic | `RESONANCE_CANON.md`, `resonance-economy.js` — RP not RC |
| Terms | `CONTINUITY_GLOSSARY.md` |
| Open owner rows | `CONTINUITY_REPORT.md` ASK OWNER |

*Last updated: Continuity wave 5, 2026-07-29 — P0=0 P1=0; VQ-27 resolved (legacy root Umbrin scrub).*
