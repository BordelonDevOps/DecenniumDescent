# Morning brief — waves 1–54 complete (~7am read)

**For:** Owner · **From:** Director + overnight workers · **Date:** 2026-07-30  
**Waves:** **1–54 done** · build pass green · no commits · no mass deletions  
**Depth:** Oracle revelations (all tiers + L12/18/20) · Paladin oaths L3–L20 · class-draft non-ASI thin · prestige hallmarks thin · prestige capstones thin · **all druid form traits thin (base/arch/hero)** — **all cleared**; content still draft for author tone review  
**Canon locks:** **Umbrin** · **Resonance** (not Hybrid-B in UI) · **17 classes** · **P0/P1 = 0** · **build green**  
**Deep logs:** [`OVERNIGHT_BRIEFING.md`](./OVERNIGHT_BRIEFING.md) · [`OVERNIGHT_PROGRESS.md`](./OVERNIGHT_PROGRESS.md)

---

## Status (one glance)

| | |
|---|---|
| **P0 / P1** | **0 / 0** — vague queue clear |
| **Build** | **Green** — `npm run build` pass (wave 55) |
| **ASK OWNER** | **0 open blockers** — all 7 `CONTINUITY_REPORT` rows closed |
| **Playtest** | Chargen → Session → Encounters/Generators → Dungeon Guide — **ready** |

**Verdict:** Companion is playtest-ready. Draft content is flagged in data/UI; nothing blocks a morning run.

**Waves 1–54:** library filters, Session Clear foes / filters, Generators copy spark; **depth passes cleared** — Oracle revelations (all tiers + L12/18/20), Paladin oaths L3–L20, class-draft non-ASI thin, prestige hallmarks thin, prestige capstones thin, **all druid form traits thin (base/arch/hero, all 0 under 60 chars)**; content still draft for author tone review. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0** · **build green**. **Coffee primary:** author tone review Oracle/Paladin/Umbrin; L11–20 author tables. **Resonance multiclass merge = approved canon** (Hybrid-B internal label only).

---

## Naming locks (do not revert)

| Term | Rule |
|---|---|
| **Umbrin** | Product demonym. **Not** Drow, **not** Umbral Elf (interim only; legacy saves migrate on load). Traits: Umbrin Magic / Umbrin Weapon Training · language **Murkish** · noble subrace **Obsidian Highborn**. |
| **Resonance** | Player-facing spell economy — **Resonance Points (RP)**. Oracle uses **Revelation Charges**, not RP. |
| **Hybrid-B** | Internal ruling label only (`resonance-economy.js` header, continuity docs). **Never** in UI, sheets, or tooltips. |

---

## Start here — five paths

| Doc | Why open it |
|---|---|
| [`UMBRIN_LORE.md`](./UMBRIN_LORE.md) | Draft lore stub — Calan'thir exile, Obsidian Burn, Umbra cult; pending rulebook promote |
| [`RESONANCE_CANON.md`](./RESONANCE_CANON.md) | Shipped vs draft Resonance wiring; multiclass RP formula (**approved canon** — Hybrid-B internal label only) |
| [`PLAYTEST_SMOKE.md`](./PLAYTEST_SMOKE.md) | 15-min smoke — Umbrin Oracle + Mage; 8/8 code-trace pass (wave 8b) |
| [`COLLABORATOR_DAY1.md`](./COLLABORATOR_DAY1.md) | Onboard a helper — same read order + report-back template |
| [`CONTINUITY_REPORT.md`](../../src/data/CONTINUITY_REPORT.md) | Glossary-aligned watchlist; ASK OWNER table all struck through |

---

## Coffee review — top 10 draft files (nothing blocking)

Skim these over coffee; all show `(draft)` in UI where applicable. **Refreshed post Phase C cleanup (2026-07-30).** **Depth passes cleared:** Oracle revelations (all tiers + L12/18/20) · Paladin oaths L3–L20 · class-draft non-ASI thin · prestige hallmarks thin · prestige capstones thin · **all druid form traits thin (base/arch/hero)** — all 0 under 60 chars; content still draft for author tone review. **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0** · **build green**. **Continuity clean pass** — P0/P1 clear. **Coffee primary:** author tone review Oracle/Paladin/Umbrin; L11–20 author tables. **Resonance multiclass merge = approved canon.**

| # | File | Why skim |
|---|------|----------|
| 1 | [`oracle-mysteries.js`](../../src/data/oracle-mysteries.js) | 8/10 mysteries draft (Battle–Time); Ancestor + **Shadow** approved; Spiral-Touched rulebook-complete; **revelations depth cleared** (Tier I/II/III + L12/18/20) — author tone review pending |
| 2 | [`paladin-oaths.js`](../../src/data/paladin-oaths.js) | 8/10 oaths draft; **Grief** approved; **L3–L20 oaths depth cleared** (waves 17–43); Mercy + others remain `draft: true`; **author tone review elevated** |
| 3 | [`class-draft-levels.js`](../../src/data/class-draft-levels.js) | ~117 draft L7–20 milestones, all 17 classes; **non-ASI thin cleared** (waves 46–47: 0 under 100 chars) — **L11–20 author tables elevated** for tone/balance before promote |
| 4 | [`UMBRIN_LORE.md`](./UMBRIN_LORE.md) | Obsidian Burn / Umbra cult stub; clarity polish wave 43; CharacterBuilder lore tip + Cosmology link (wave 24); rulebook docx still says Drow — **promote on re-ingest elevated** |
| 5 | [`resonance-economy.js`](../../src/lib/resonance-economy.js) | `DRAFT_POOL_TABLES` flagged draft when either class uses draft pool table; **multiclass RP merge = approved canon** (`mergeMulticlassMaxRp`); Hybrid-B internal label only |
| 6 | [`oracle-curses.js`](../../src/data/oracle-curses.js) | 9/9 curses draft — **boon depth complete** (wave 19; 0 thin boons); author tone pass only |
| 7 | [`prestige-lorebook.json`](../../src/data/prestige-lorebook.json) | 18 prestige paths; **hallmark + capstone thin cleared** (waves 33a/33b + 50a: 0 under 80/100 chars) — author tone pass only |
| 8 | [`dungeon-mechanics.json`](../../src/data/dungeon-mechanics.json) | Director draft `entryClasses` + `victoryConsequences`; Dungeon Guide search UX landed wave 20 |
| 9 | [`cosmology-lore.json`](../../src/data/cosmology-lore.json) | XIV superseded by Dungeon Guide; First Song IX–XII nav partial (VQ-18) |
| 10 | [`reputation.js`](../../src/data/reputation.js) | 9 draft factions; ReputationPanel filter/search UX wave 20b — rep→RP auto-apply still unwired (VQ-21) |

Lower urgency (balance / wiring): prestige feats reconcile vs docx (`feats.js` — 53/53 enriched, 0 thin), Session wild-shape tracker (VQ-22), overcast panel (VQ-23), header search stub discoverability done (wave 21 `/` + Esc tooltip; VQ-20 partial).

---

## What landed (waves 1–11, compressed)

**Core systems**
- Resonance/RP wired end-to-end — reputation modifiers, Short/Long rest recovery, overcast/Burnout stub in Session
- Session tracker — party RP from computed max, Oracle RC, multiclass badges, gate-boss labels, loot handoff banner
- Multiclass Builder UI + Sheet/Session secondary-class display

**Content polish**
- Umbrin rename shipped across chargen, bestiary (10 entries), generators, sheet lore card + print CSS
- L11–20 full coverage; Paladin L20 gifts + Oracle charge/curse passes; Druid 7-circle Paths; prestige paths display
- Cosmology — First Song I–XII nav (9b); World of Aethel I–VI extract stub + VII–XV † markers

**UX / handoffs**
- Encounters, Generators, Items → Session (`onLoadSession` tab switch fixed wave 2)
- Header tab search stub; bestiary Umbrin name/tag search; crafting filter edges

---

## Safety check

- Renames, `draft: true` fills, and doc updates only — no mass deletion
- 17 canon classes unchanged; no Fighter/Swashbuckler in builder; no 3D/SWTOR work
- `CHARGEN_PROGRESSION.md` has 5 author-priority rows — not contradictions, not blockers

---

## Queued (not urgent)

1. Overcast panel → tie to real spell base cost (manual entry today)
2. Multiclass RP formula — documented in canon, not fully implemented in `defaultMaxRp()`
3. Roadmap snapshot: `docs/MECHANICS_ROADMAP.md` → Director Status / Overnight wave section

---

*Living document — append wave sections below; do not overwrite this brief without a new overnight pass.*

---

## Wave 2 — Playtest readiness (2026-07-29 PM)

**Worker:** Playtest smoke pass  
**Commit:** none (per owner request)

### Delivered

| Item | Result |
|------|--------|
| **`docs/mechanics/PLAYTEST_SMOKE.md`** | 15-minute smoke path: Umbrin Oracle + Mage chargen, subclass paths, RC/RP checks, Session rests, Encounters + Generators handoff, Dungeon Guide **Mechanics** (Cycle) tab |
| **Import / build health** | No broken imports found. `npx tsc --noEmit` **clean**. `npm run build` **clean** (pre-fix baseline). |
| **Encounters / Generators → Session** | Handoff via `session-handoff.ts` verified; **fix:** `Load in Session` now calls `onLoadSession()` so SESSION tab mounts and `consumeEncounterHandoff()` runs (previously required manual tab switch while handoff sat in localStorage). |
| **Typecheck after fix** | `npx tsc --noEmit` **clean** |

### Code touch (Wave 2)

- `src/app/page.tsx` — pass `onLoadSession={() => setActiveTab("session")}` to Encounters + Generators
- `src/components/EncountersBrowser.tsx` — optional `onLoadSession` prop after `pushEncounterHandoff`
- `src/components/GeneratorsPanel.tsx` — same

### Smoke summary (quick run)

1. **CHARACTERS:** Umbrin → Oracle or Mage → Paths picks → SAVE  
2. **SESSION:** Add saved PC → RC (Oracle) or RP (Mage) → Short / Long rest  
3. **ENCOUNTERS** or **GENERATORS:** Load in Session → tier + scene brief land on SESSION  
4. **DUNGEON GUIDE → Mechanics:** Cycle & Shardspire, entry classes, victory consequences  

### Still non-blocking

Same draft items as morning handoff; smoke doc lists explicit non-fail criteria (HP stub, no spell picker in session, placeholder search).

---

## Wave 3 — Collaborator-ready content (2026-07-29 PM)

**Worker:** Chargen + generators + cosmology + onboarding  
**Commit:** none (per owner request)

### Delivered

| Item | Result |
|------|--------|
| **Multiclass Builder UI** | Origin → Class: optional secondary class + level (17 canon); saves `secondaryClass` / `secondaryLevel`; Weave max RP uses §7 merge |
| **CHARGEN_PROGRESSION** | Multiclass table + manual JSON (`classLevels` alt shape) |
| **Generators People spark** | Random race from `builder-races.js` — **Umbrin** in pool; Drow excluded from generator filter |
| **Cosmology Key terms** | Calan'thir, First Choir, Umbra, Lumina, Umbrin panel in viewer sidebar |
| **`COLLABORATOR_DAY1.md`** | Day-1 read → smoke → Umbrin lore + Resonance canon → report-back template |
| **Typecheck** | `npx tsc --noEmit` — see progress log |

### Code touch (Wave 3)

- `src/components/CharacterBuilder.tsx` — multiclass state, save/load, RP label
- `src/lib/character-storage.js` — normalize secondary fields
- `src/components/GeneratorsPanel.tsx` — `genPeople()` + People spark button
- `src/components/CosmologyViewer.tsx` — `GLOSSARY_TERMS` card

### Suggested first task for a new collaborator

Follow [`docs/mechanics/COLLABORATOR_DAY1.md`](./COLLABORATOR_DAY1.md) — onboarding read, 15-min smoke, skim `UMBRIN_LORE.md` + `RESONANCE_CANON.md`.

---

## Wave 5 — oath L20 + oracle spot-check + session multiclass (2026-07-29 PM)

**Worker:** Chargen + Session overnight pass  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **Paladin L20 gifts** | All 10 oaths have `finalOathGift`; Mercy only (draft gift, canon oath untouched) |
| **Oracle charge spot-check** | Bones–Stars + Ancestor tier III prefix fix; Battle/Time/Shadow unchanged |
| **Session multiclass** | Combatant row badge when `secondaryClass` set |
| **Handoff refresh** | Top morning snapshot table (this section) |
| **Typecheck** | `npx tsc --noEmit` — see progress log |

---

## Wave 6 — deeper content (2026-07-29 PM)

**Worker:** Oracle curses + Druid paths + crafting filter pass  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **Oracle curses** | 9/9 draft trees complete (Boons I–V + 3 limitations); 4 thin boons enriched |
| **Druid Paths** | Circle-filtered arch + hero display; Thorns forms + Shadow Lynx fixed |
| **Crafting filters** | ItemsLibrary crafted tab: skill categories, ingredient search, tab reset |
| **WORLD_DUNGEON_LOOP** | GM note — no crafting→Session handoff |
| **Typecheck** | `npx tsc --noEmit` exit 0 |

---

## Wave 7 — items→Session + Umbrin generator tags (2026-07-29 PM)

**Worker:** Session loop + generator polish  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **Items → Session** | **Log loot in Session** on crafted/dropped detail; `pushLootHandoff` append to scene notes; tab switch via `onLoadSession` |
| **Session mount fix** | Handoffs no longer skipped when `dd_session_tracker` absent (first visit) |
| **Generators Umbrin** | People spark lore badges; Murk/Obsidian/Shadow name bits show Umbrin lore hint tags |
| **WORLD_DUNGEON_LOOP** | Crafting handoff doc updated |
| **Typecheck** | `npx tsc --noEmit` — see progress log |

---

## Wave 8b — smoke verification (2026-07-29 PM)

**Worker:** Playtest smoke trace + doc/code alignment  
**Commit:** none (per owner request)

### Build health

| Check | Result |
|------|--------|
| **`npx tsc --noEmit`** | **Pass** (exit 0, ~13s) |
| **Import scan** | No broken imports on smoke path |

### Fixes applied

| Item | Change |
|------|--------|
| **`PLAYTEST_SMOKE.md`** | Level control → **Advancement** card (was wrongly "Abilities column"); Mage reset → **NEW** header button; optional stretch → **EXPORT** label |
| **`CharacterBuilder.tsx`** | Oracle Weave guidance: "Features" tab → **Paths** tab (matches UI label) |

### Smoke step results (code trace — no live browser run)

| Step | Path | Result | Notes |
|------|------|--------|-------|
| **Before** | Dev port 8500, localStorage keys, typecheck | **Pass** | `package.json` dev script; keys match `character-storage.js` / `session-handoff.ts` |
| **1** | Umbrin Oracle chargen + SAVE | **Pass** | Origin People/Class, Paths (Mystery/Curse), Weave RC message, SAVE, Load saved chips |
| **2** | Sheet view Oracle RC terminology | **Pass** | Build/Sheet toggle; CharacterSheet Revelation Caster copy |
| **3** | Session RC + rests | **Pass** | Add saved character; RC pool L3=4/4; Mystery/Curse badges; Short/Long rest in Party Resonance |
| **4** | Umbrin Mage chargen + SAVE | **Pass** | NEW, Arch path, Paths/ClassPathDisplay, Weave RP slider |
| **5** | Session RP + rests | **Pass** | RP pool column; per-row RP; Short/Long rest |
| **6** | Encounters → Session handoff | **Pass** | T{n} picker, Load in Session, `onLoadSession` → SESSION; banner + tier + scene notes |
| **7** | Generators → Session handoff | **Pass** | T3 + Build pack for Tier {n} + Load in Session; overwrites prior brief |
| **8** | Dungeon Guide Mechanics tab | **Pass** | Cycle & Shardspire, 17 entry classes, 10 victory rows, Expedition + Gate Bosses |

**Overall smoke path: PASS** (8/8 steps aligned; live browser not re-run this wave).

---

## Wave 8 — prestige feats + Umbrin sheet (2026-07-29 PM)

**Worker:** Content polish  
**Commit:** none

| Item | Result |
|------|--------|
| **Prestige feats** | Five thin draft effects enriched (Hardened Grip, Lightning Affinity, Dark Affinity, Primal Instinct, Combat Engineering) — all `draft: true` |
| **CharacterSheet** | Umbrin characters get lore blurb excerpt + Murkish language note |
| **UX copy** | `game-data.js` Mycelian **Undercommon** → **Mycelian**; Generators race pool filter cleaned |
| **Typecheck** | `npx tsc --noEmit` — see progress log |

---

## Wave 9b — Cosmology First Song split (2026-07-29 PM)

**Worker:** Content structure  
**Commit:** none

| Item | Result |
|------|--------|
| **firstSongSections** | 12 chapters (I–XII) split from EXTRACT; IX–XII `draft: true` |
| **CosmologyViewer** | First Song tab: chapter nav buttons I–XII († = draft), per-chapter body |
| **Tooling** | `tools/split_first_song.py` for re-ingest |
| **Typecheck** | `npx tsc --noEmit` exit 0 |

---

## Wave 10 — prestige polish + cosmology world stub + loot banner (2026-07-29 PM)

**Worker:** Content + Session UX overnight pass  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **Prestige draft feats** | 12 thin effects enriched (Slayer's Resolve, Life Drinker, Arcane Calculus, Cursebound Flesh, Beast Lore, Core Infusion, Conjure Flora, Anatomy Lore, Eldritch Combat, Curse Channeling, Blood Ritual, Dark Fortitude) — all `draft: true` |
| **World of Aethel nav** | `I–VI` extract-gap stub section + draft † markers on world section buttons; XIV keeps superseded banner |
| **Session loot banner** | Clarifies item count, source tab, Scene notes copy, and manual inventory assignment |
| **Handoff refresh** | Morning snapshot updated with waves 6–10 highlights (8 bullets) |
| **Typecheck** | `npx tsc --noEmit` — see progress log |

---

## Wave 11 — class draft L11–20 polish (2026-07-29 PM)

**Worker:** Content polish (prestige scan + class draft fallback)  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **Prestige draft feats** | 0 thin remaining — all 53 already enriched |
| **Class draft levels** | 5 Oracle/Paladin/Mage milestones enriched (L11/L13/L17, Paladin L16, Mage L12) — all `draft: true` |
| **Handoff refresh** | Morning snapshot updated with wave 11 class-draft bullet |
| **Typecheck** | `npx tsc --noEmit` — see progress log |

---

## Wave 11b — app health (2026-07-29 PM)

**Worker:** Typecheck + production build + component TODO scan  
**Commit:** none (per owner request)

### Build health

| Check | Result |
|------|--------|
| **`npx tsc --noEmit`** | **Pass** (exit 0, ~14s) |
| **`npm run build`** | **Pass** (exit 0, ~45s) — compiled, lint/types OK, static export 4 routes |

### ESLint warnings (non-blocking, pre-existing)

| File | Warning |
|------|---------|
| src/components/CharacterBuilder.tsx:567 | react-hooks/exhaustive-deps — useEffect missing dependency `abilities` |
| src/data/druid-shapeshifting.js:382 | import/no-anonymous-default-export |

### TODO / FIXME scan (src/components)

| Scan | Result |
|------|--------|
| **TODO / FIXME** | **0 matches** in src/components (also 0 across all of src/) |
| **Fixes applied** | None — no component TODOs tied to broken features |

### Code touch (Wave 11b)

None.

---

## Wave 12 — lint fixes + session initiative sort (2026-07-29 PM)

**Worker:** App health + Session UX  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **CharacterBuilder exhaustive-deps** | Intentional disable at racial ASI effect — avoids stacking bonuses on every manual score edit |
| **druid-shapeshifting default export** | Named `druidShapeshifting` const; clears `import/no-anonymous-default-export` |
| **Session initiative** | Round/Turn card: **Sort initiative** (persist order, turn → 0) + **Roll all** (d20+Dex, sort, round 1) |
| **Typecheck / build** | `npx tsc --noEmit` exit 0 (~12s); `npm run build` exit 0 (~41s) — lint clean |

### ESLint warnings (wave 12)

Wave 11b pre-existing warnings above — **both cleared** in wave 12.

---

## Wave 13 — encounters search + Umbrin picker + export fields (2026-07-29 PM)

**Worker:** UX polish overnight pass  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **EncountersBrowser** | Cross-tier search — tier/boss/POI/haven match chips jump to tier; clear (X) button; tier meta match shows full haven/POI lists |
| **CharacterBuilder — People** | **Umbrin** pinned first in picker (★ marker); search filter by name, lineage, trait, language |
| **Export JSON payload** | Always includes `sacredOath`, `oracleMystery`, `oracleCurse`, `druidCircle`, `secondaryClass` / `secondaryLevel` (aligned to `normalizeCharacter`) |
| **Typecheck** | `npx tsc --noEmit` — see progress log |

---

## Wave 14 — bestiary filters + session handoff tick + search shortcut (2026-07-29 PM)

**Worker:** UX polish overnight pass  
**Commit:** none (per owner request)

### 1. MonstersLibrary — filter/search polish

| Surface | Change |
|---------|--------|
| Search | Matches name, type, description, tags, zone, and CR (including `cr 5` prefix) |
| Clear search | X button on search input |
| Active filters | **Clear filters** button when any Type/CR/Size/Zone/Tier dropdown ≠ All; results count shows `(filtered)` |

### 2. GeneratorsPanel — Load in Session handoff

| Surface | Change |
|---------|--------|
| `page.tsx` | Shared `goToSession()` increments `sessionHandoffTick` then switches to Session tab |
| `SessionTracker.tsx` | `handoffTick` prop — `useEffect` re-consumes encounter handoff when tick changes (covers Generators, Encounters, Items) |
| `GeneratorsPanel.tsx` | Unchanged logic — `pushEncounterHandoff` + `onLoadSession`; wired through shared navigator |

### 3. Header — search keyboard shortcut

| Surface | Change |
|---------|--------|
| `/` key | Focuses tab search when not already in an input/textarea |
| Hint | Placeholder `(/ to focus)` + `kbd` badge on lg+ viewports |

### 4. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 14 edits (~13s).

---

## Files touched (wave 14)

- `src/components/MonstersLibrary.tsx` — CR/type/zone search, clear controls
- `src/app/page.tsx` — `sessionHandoffTick` + `goToSession()`
- `src/components/SessionTracker.tsx` — handoff tick re-apply
- `src/components/Header.tsx` — `/` shortcut + hint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 14 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 14 append

---

## Wave 15 — sheet print identity + session crowd UX + idempotent handoff (2026-07-29 PM)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. CharacterSheet — print identity strip

| Surface | Change |
|---------|--------|
| Header subtitle | Identity line under class row when set: secondary class level, Sacred Oath, Druid Circle, Oracle Mystery, Oracle's Curse |
| Print | Same strip uses `print:text-gray-700` — visible on paper without opening class-feature blocks |

### 2. SessionTracker — crowded combatants (light UX)

| Surface | Change |
|---------|--------|
| Filter chips | **All / Allies / Foes** when ≥ 7 combatants on table |
| Foes collapse | When ≥ 4 foes and filter = All, foes start collapsed; **Show foes (N)** expand / **Collapse foes** toggle |
| Active hint | Banner when active combatant hidden by filter |

### 3. Session handoff — idempotent consume

| Surface | Change |
|---------|--------|
| `session-handoff.ts` | `takeEncounterHandoff(sinceCreatedAt)` + `takeLootHandoff(sinceCreatedAt)` — skip already-applied batches |
| `SessionTracker.tsx` | Refs track last applied `createdAt`; unified `applyPendingHandoffs()` on mount + `handoffTick`; loot append uses functional `setSceneNotes` on tick |
| Regression fix | Mount + tick no longer double-consume same encounter/loot push |

### 4. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 15 edits (~14s).

---

## Files touched (wave 15)

- `src/components/CharacterSheet.tsx` — identity strip (secondary / oath / circle / mystery / curse)
- `src/components/SessionTracker.tsx` — combatant filter, foes collapse, idempotent handoff apply
- `src/lib/session-handoff.ts` — `takeEncounterHandoff` / `takeLootHandoff`
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 15 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 15 append

---

## Wave 16 — Spells Oracle UX + Paladin L3 oath enrichment (2026-07-29 PM)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Spells Library — Oracle as Revelation (not Weave)

| Surface | Change |
|---------|--------|
| Class dropdown | **Oracle (Revelations)** label — distinguishes from Weave casters |
| Filter banner | When Oracle selected: explains RC/Mystery path; spell list is thematic reference (Divination/Abjuration overlap), not Oracle spellbook |
| `spell-utils.js` | `isRevelationCaster()` + exported `REVELATION_CASTERS` |

### 2. Paladin draft oath L3 — 3 enriched vs Mercy

| Oath | Enrichment |
|------|------------|
| **Dominion** | Smite: liars in aura −1 saves; L3 Compelled Truth: 10-ft zone + psychic on failed Charisma save |
| **Silence** | L3 Hush: silent-since-combat-start rider adds disadvantage on target's next attack |
| **Martyr King** | Smite: redirect 5 ally damage/round; L3 Noble Bearing: aura morale + temp HP on smite |

All retain `draft: true`.

### 3. Build

```bash
npx tsc --noEmit   # exit 0 (~11s at start; re-run post-edit exit 0)
npm run build      # exit 0 (~47s) — static export OK
```

---

## Files touched (wave 16)

- `src/data/spell-utils.js` — revelation caster helpers
- `src/components/SpellsLibrary.tsx` — Oracle UX banner + label
- `src/data/paladin-oaths.js` — Dominion / Silence / Martyr King L3
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 16 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 16 append

---

## Wave 17 — SessionTracker lint + Paladin L3 + Spells clear-filters (2026-07-29 PM)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. SessionTracker — eslint-disable cleanup

| Surface | Change |
|---------|--------|
| Mount restore `useEffect` | Removed unused `eslint-disable-next-line react-hooks/exhaustive-deps` |
| Handoff tick `useEffect` | Removed unused disable — dependency array already valid |

Fixes wave 16 build lint warnings (2 unused directive reports).

### 2. Paladin draft oath L3 — 3 enriched vs Mercy

| Oath | Enrichment |
|------|------------|
| **Ancients** | Smite: extended root + fey/elemental save penalty; L3 Roots of Memory: 10-ft burst, Str save restrain, origin lore |
| **Chain** | Smite: CHA-mod redirect from bonded ally; L3 Linked Ward: reaction redirect + temp HP if paladin drops |
| **Grief** | Smite: killer-of-ally bonus + Grief Mark; L3 Dirge: cone/single Wis save with undead radiant rider |

All retain `draft: true`.

### 3. Spells Library — clear filters

| Surface | Change |
|---------|--------|
| Stats row | **Clear filters** button when any filter active (parity with MonstersLibrary) |

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~10s)
npm run build      # exit 0 (~42s) — static export OK; no eslint warnings
```

---

## Files touched (wave 17)

- `src/components/SessionTracker.tsx` — unused eslint-disable removal
- `src/data/paladin-oaths.js` — Ancients / Chain / Grief L3
- `src/components/SpellsLibrary.tsx` — clear-filters UX
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 17 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 17 append

---

## Wave 18 — Paladin L3 + CraftingBuilder filters (2026-07-29 PM)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Paladin draft oath L3 — final 2 enriched vs Mercy

| Oath | Enrichment |
|------|------------|
| **Vengeance** | L3 Mark of Retribution: 30-ft Wis save mark; +1d8 smite vs marked; advantage on opportunity attacks until end of next turn |
| **Chains Broken** | Smite: on hit removes grapple/restraint until end of next turn; L3 Break Bonds: touch or 30-ft ally; escape riders for magical binding |

All 9 draft oaths now have Mercy-parity L3 revelation text. Flame retained (on-crit rider already present).

### 2. CraftingBuilder — clear-filters + search polish

| Surface | Change |
|---------|--------|
| Components | Clear filters button; filtered count; search includes category/rarity/properties |
| Recipe catalog | Clear filters button; filtered count suffix |

Parity with MonstersLibrary / SpellsLibrary / ItemsLibrary filter UX.

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–18**, build green, points here.

### 4. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 18)

- `src/data/paladin-oaths.js` — Vengeance / Chains Broken L3
- `src/components/CraftingBuilder.tsx` — clear-filters + search haystack
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–18
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 18 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 18 append

---

## Wave 19 — Oracle curse boon depth finish + ItemsLibrary filters (2026-07-29 PM)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Oracle curse boon depth — wave 18b deferred (8 boons)

Finished enriching the 8 single-sentence draft curse boons deferred from wave 18b to ~2-sentence Spiral-Touched depth:

| Curse | Boons enriched |
|-------|----------------|
| **Burning Blood** | L5, L10, L20 |
| **False Life** | L20 |
| **Shattered Mind** | L3 |
| **Fate-Bound** | L20 |
| **Haunted** | L20 |
| **Consumed** | L20 |

Depth scan (`tools/oracle_curse_boon_depth.py`): **0 draft boons under 2 sentences**. All nine draft curses retain `draft: true`. **Oracle curse boon depth pass complete.**

### 2. ItemsLibrary — clear-filters UX

| Surface | Change |
|---------|--------|
| Dropped / Crafted tabs | Clear filters button; `(filtered)` count suffix when search/rarity/category/tier active |

Parity with MonstersLibrary / SpellsLibrary / CraftingBuilder.

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–19**, build green.

### 4. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 19)

- `src/data/oracle-curses.js` — 8 curse boon enrichments
- `src/components/ItemsLibrary.tsx` — clear-filters UX
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–19
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 19 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 19 append

---

## Wave 20 — class draft enrichments + Dungeon Guide search (2026-07-29 PM)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Oracle curses and Paladin L3 skipped — already at Mercy/Spiral-Touched depth. Enriched other short milestones:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Bard** | 11 | Crescendo die d10 — Inspire Courage roll adds to ally attack/save within 1 round |
| **Cleric** | 16 | Domain capstone — Channel Divinity duplicates domain 6th spell; 30-ft resistance aura |
| **Monk** | 16 | Ki Chain cap 7 — full chain release refunds 1 Ki on next unarmed hit |
| **Shaman** | 11 | Flask Tier III — three concurrent flasks; spend no longer ends totem pulse |
| **Dragoon** | 16 | Apex Assault — 1 bonus-action recharge; first leap ignores difficult terrain |

All retain `draft: true`.

### 2. Dungeon Guide — search/filter UX

| Surface | Change |
|---------|--------|
| Search | Tiers, bosses, havens, POIs, gate bosses, victory consequences |
| Filter | **Mapped tiers only** toggle; match count; clear filters button |

Light polish — parity with MonstersLibrary / ItemsLibrary filter patterns.

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–20**, build green.

### 4. Build

```bash
npm run build   # exit 0 (~45s)
```

---

## Files touched (wave 20)

- `src/data/class-draft-levels.js` — 5 class draft enrichments
- `src/components/DungeonGuide.tsx` — search/filter UX
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–20
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 20 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 20 append

---

## Wave 21 — continuity stamp + coffee list refresh (2026-07-30)

**Worker:** Continuity (quick scan)  
**Commit:** none (per owner request)

### 1. Continuity re-scan (post waves 19–20 / 20b)

| Target | Result |
|--------|--------|
| **Umbrin / no Drow-Lolth IP** | **Pass** — product path clean; legacy migration only |
| **Hybrid-B in player UI** | **Pass** — internal docs / `resonance-economy.js` header only |
| **Waves 19–20 surfaces** | **Pass** — oracle curse boon depth, class-draft enrichments, Items/Dungeon/Reputation filter UX; all retain `draft: true` |
| **17 classes / Bloodbound / Oracle RC** | **Pass** — unchanged |
| **Build** | `npx tsc --noEmit` **exit 0** (~10s) |

**Verdict:** **Green** — P0/P1 clear; no new P2 blockers.

### 2. Coffee list refresh

Top 10 draft files table updated in the brief opening (post waves 19–20: curses boon-deep, oaths L3-deep, five class milestones enriched).

### 3. Docs touched

- `src/data/CONTINUITY_REPORT.md` — wave 21 stamp + gate status line
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this append

---

## Wave 21 — class draft enrichments + header search help (2026-07-29 PM)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 20 covered Bard/Cleric/Monk/Shaman/Dragoon. This wave targets the next thinnest martial/utility casters:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Warrior** | 12 | Brutality Threshold — 100% max HP damage dealt unlocks Transcendent mutation tier for 3 rounds |
| **Wizard** | 16 | Arcane Tradition capstone — +1 tier school cast 1/long rest; 10-ft elemental resistance aura |
| **Thief** | 16 | Poison prep +1 — three toxins; Sneak Attack poison no longer costs bonus action |
| **Ranger** | 11 | Druidic Arrow combo — Hunter's Mark hit + slot for second radiant arrow (slot level d8) |
| **Tinker** | 16 | Third deployable slot — three gadgets; two activations share one bonus action |

All retain `draft: true`.

### 2. Header search — shortcut help tooltip

| Surface | Change |
|---------|--------|
| Search bar | `?` hover/focus tooltip documents **`/`** (focus) and **Esc** (clear & blur) |
| Existing | `/` global focus + Esc handler unchanged — UX gap was discoverability only |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–21**, typecheck green.

### 4. Typecheck

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 21)

- `src/data/class-draft-levels.js` — 5 class draft enrichments
- `src/components/Header.tsx` — search shortcut help tooltip
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–21
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 21 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 21 append

---

## Wave 22 — class draft enrichments + Session empty state (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 21 covered Warrior/Wizard/Thief/Ranger/Tinker. This wave targets Mage, Soldier, Crimson Agent, Mirrorsage, and Bard L16:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Bard** | 16 | Counter-Melody mastery — spend 1 Crescendo to redirect ally's failed spell/sonic save onto you with advantage |
| **Mage** | 18 | 9th-level slots — one 9th-tier Resonance slot; full-pool cost unless Archmage Reservoir unused |
| **Soldier** | 12 | Skill tree tier III — Formation/Overwatch capstone; Palisade +2 AC to allies in cover for 1 round |
| **Crimson Agent** | 12 | Skill tree tier III — Veinweave/Shadowblade capstone; Sneak Attack on Blood Mark refreshes one Veinweave charge |
| **Mirrorsage** | 18 | Focus Points +1 per battle — form shift no longer ends Echo Slot hold on prior spell |

All retain `draft: true`.

### 2. Session — combatants empty state

| Surface | Change |
|---------|--------|
| Combatants list | When no combatants, shows tip: **"Add saved character or foe."** (replaces generic initiative prompt) |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–22**, build green.

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~10s)
npm run build      # exit 0 (~45s)
```

---

## Files touched (wave 22)

- `src/data/class-draft-levels.js` — Bard/Mage/Soldier/Crimson Agent/Mirrorsage L11–20 enrichments
- `src/components/SessionTracker.tsx` — combatants empty-state tip
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–22
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 22 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 22 append

---

## Wave 23 — class draft + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 22 covered Bard/Mage/Soldier/Crimson Agent/Mirrorsage. This wave targets remaining thin canon-17 entries (Swashbuckler skipped — orphan):

| Class | Level | Enrichment |
|-------|-------|------------|
| **Dragoon** | 12 | Skill tree tier III — Dragon Lancer/hero capstone; Wyvern's Flow Momentum refund; Apex Assault overflow +1d6 per stack above cap |
| **Monk** | 20 | Transcendent Flow — stance shift twice per round; max Ki Chain grants +1 temp Ki until end of turn |
| **Shaman** | 17 | Flask Tier IV — four concurrent flasks; spending triggers Totem Pulse on nearest active totem |
| **Cleric** | 18 | Divine Intervention — once/week prayer succeeds on nat 1; success restores one Channel Divinity |
| **Druid** | 11 | Arch Druid Forms — circle arch shapes; Wild Shape CR = tier floor −1 (min CR 2); moved from `class-details.js` to draft merge |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Next thinnest after wave 22b (Beastmaster/Blademaster/Chronomancer): **Battlemage**, **Berserker**, **Mooncursed**.

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Battlemage** | Battle Flow | Momentum stacks persist through short rests along Aethel descent tiers |
| **Berserker** | Sweeping Blow | Ritual cleave through two adjacent foes — knockback + Stagger until Frenzy ends |
| **Mooncursed** | Beast Within | Auto-transform at ≤25% HP; choose form if multiple unlocked |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–23**, build green.

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~10s)
```

---

## Files touched (wave 23)

- `src/data/class-draft-levels.js` — Dragoon/Monk/Shaman/Cleric/Druid enrichments
- `src/data/class-details.js` — Druid L11 removed for draft merge
- `src/data/prestige-lorebook.json` — Battlemage, Berserker, Mooncursed hallmarks
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–23
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 23 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 23 append

---

## Wave 24 — class draft + prestige hallmark + Umbrin lore tip (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (3 thin entries)

Class drafts still dominate thin backlog (~50 mech stubs vs ~15 prestige hallmark lines). Wave 23 covered Dragoon/Monk/Shaman/Cleric/Druid; this wave targets remaining L12 skill-tree stubs:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Ranger** | 12 | Skill tree tier III — Beastwarden or Stalker's Path capstone; Hunter's Mark d8; Favored Terrain bonus to allies within 10 ft |
| **Thief** | 12 | Skill tree tier III — Shadowblade or Poisoner capstone; Sneak Attack on poisoned target refreshes one toxin prep (once/target per short rest) |
| **Tinker** | 12 | Skill tree tier III — Siege Engineer or Anacite Savant capstone; deployables +2 HP threshold; first bomb +5 ft radius each encounter |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (2 thin arrays)

Next thinnest after wave 23 (Battlemage/Berserker/Mooncursed): **Giant Killer**, **Berserker** (Deathlust still thin).

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Giant Killer** | Kneecap Strike | Huge+ leg cripple on crit or ≥ half max HP strike — −15 ft move; second kneecap Prone |
| **Berserker** | Deathlust | Each Frenzy kill +1 round (max +3); boss kill resets one Reckless Charge |

### 3. CharacterBuilder — Obsidian Burn lore tip

When **Umbrin** is selected under People, a one-line **Obsidian Burn (draft)** tip appears under the race picker with a **Lore (draft)** link that opens the COSMOLOGY tab (Umbrin key terms).

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~10s)
```

---

## Files touched (wave 24)

- `src/data/class-draft-levels.js` — Ranger/Thief/Tinker L12 enrichments
- `src/data/prestige-lorebook.json` — Giant Killer, Berserker hallmarks
- `src/components/CharacterBuilder.tsx` — Obsidian Burn tip + optional `onOpenLore`
- `src/app/page.tsx` — wire `onOpenLore` → COSMOLOGY tab
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–24
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 24 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 24 append

---

## Wave 25 — continuity stamp (2026-07-30)

**Worker:** Continuity (quick scan)  
**Commit:** none (per owner request)

### 1. Continuity re-scan (post wave 24)

| Target | Result |
|--------|--------|
| **Umbrin / no Drow-Lolth IP** | **Pass** — product path clean; Obsidian Burn tip uses Umbrin/Calan'thir/First Choir only; legacy migration only |
| **Hybrid-B in player UI** | **Pass** — internal docs / `resonance-economy.js` header only |
| **Wave 24 surfaces** | **Pass** — Ranger/Thief/Tinker L12 drafts, Giant Killer/Berserker hallmarks, Umbrin lore tip + Cosmology link; all retain `draft: true` |
| **17 classes / Bloodbound / Oracle RC** | **Pass** — unchanged |
| **Build** | `npx tsc --noEmit` **exit 0** (~8s) |

**Verdict:** **Green** — P0/P1 clear; no new P2 blockers.

### 2. Docs touched

- `src/data/CONTINUITY_REPORT.md` — wave 25 stamp + gate status line
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this append

---

## Wave 25b — class draft + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 24 covered Ranger/Thief/Tinker L12. Soldier/Crimson Agent/Mage/Warrior L12 were enriched in wave 22. This wave clears the remaining L12 skill-tree stubs plus Warrior capstone:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Bard** | 12 | Skill tree tier III — Virtuoso or Discord capstone; Counter-Melody +1 stack reserve; Song of Rest builds 1 Crescendo on ally HP recovery |
| **Mirrorsage** | 12 | Skill tree tier III — Light Weaver or Shattered One capstone; first witnessed spell echoes at half RP cost (min 1) |
| **Shaman** | 12 | Skill tree tier III — Theurgist or Bloodcaller capstone; totem placement releases flask mist in 10 ft (once/totem/encounter) |
| **Monk** | 12 | Skill tree tier III — Enlightened Master or Iron Fist capstone; stance entry +1 Ki Chain storage until shift |
| **Warrior** | 20 | Apex Form — fourth mutation slot 1/encounter per long rest; Brutality Threshold skips damage gate for Transcendent tier |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (2 thin arrays)

Next thinnest after wave 24 (Giant Killer/Berserker): **Echomancer**, **Gravetouched**.

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Echomancer** (#7) | Mirror Pulse | Echo retains original tier/school; redirect to second target within 30 ft |
| **Gravetouched** (#10) | Bone Shield | While active, Death Touch applies Vulnerable to necrotic until shield fades |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–25**, build green.

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~9s)
```

---

## Files touched (wave 25b)

- `src/data/class-draft-levels.js` — Bard/Mirrorsage/Shaman/Monk L12 + Warrior L20 enrichments
- `src/data/prestige-lorebook.json` — Echomancer, Gravetouched hallmarks
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–25
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 25 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 25b append

---

## Wave 26 — class draft + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 25 cleared remaining L12 skill-tree stubs. This wave targets the thinnest non-ASI milestones still under ~60 chars:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Cleric** | 11 | Destroy Undead (CR 2) — Turn destroys CR 2 or lower on failed save; sanctified ash lingers 1 round as holy focus |
| **Cleric** | 12 | Channel Divinity (3/rest) — third use per short rest; first Channel each encounter gains +10 ft radius on domain option |
| **Shaman** | 13 | Second active totem slot — two totems concurrently; placing second triggers weak pulse on first (once/encounter) |
| **Shaman** | 18 | Totem duration +1 round — totems persist one extra round; natural expiry releases stored flask mist in 5 ft burst |
| **Thief** | 17 | Death Blossom (Shadowblade) — once/short rest, Sneak Attack on poisoned target detonates toxin stacks in 10 ft radius |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (2 thin arrays)

Wave 26b (parallel) covered Verdant Animist/Chronomancer/Gravetouched. This wave picks next thinnest: **Bloodbound**, **Mooncursed**.

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Bloodbound** (#4) | Bloodwalk | Teleport adjacent to Bleeding target within 60 ft; next melee hit consumes Bleed stack to heal |
| **Mooncursed** (#12) | Curse Surge | Spend HP for lycan bonus trait without transforming; half HP cost at night |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–26**, build green.

### 4. Build

```bash
npm run build   # exit 0 (~45s)
```

---

## Files touched (wave 26)

- `src/data/class-draft-levels.js` — Cleric L11–12, Shaman L13/18, Thief L17 enrichments
- `src/data/prestige-lorebook.json` — Bloodbound, Mooncursed hallmarks
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–26
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 26 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 26 append

---

## Wave 27 — class draft + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 26 cleared Cleric/Shaman/Thief milestones. This wave targets the five shortest remaining non-ASI stubs:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Dragoon** | 11 | Extra Attack — second strike when you take the Attack action; Wyvern's Flow leap-attacks count as one attack for Extra Attack sequencing (once/turn) |
| **Mage** | 7 | 4th-level slots — gain one 4th-tier Resonance slot; overcast from this tier costs +1 RP beyond base (min 2 RP total) |
| **Mage** | 11 | 5th-level slots — gain one 5th-tier Resonance slot; tradition spells at this tier may be prepared without slot cost once per long rest |
| **Mage** | 13 | 6th-level slots — gain one 6th-tier Resonance slot; casting your school's signature spell at this tier does not trigger Burnout on success |
| **Mage** | 15 | 7th-level slots — gain one 7th-tier Resonance slot; allies within 10 ft gain advantage on saves vs. your school's element when you cast at this tier |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Skipped recently enriched (waves 24–26). Next thinnest: **Hexblade**, **Blademaster**, **Warlock**.

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Hexblade** (#11) | Eldritch Arc | Channel cantrips and 1st-tier hexes through bound-weapon strikes; crit applies hex rider at full tier (once/short rest) |
| **Blademaster** (#3) | Parry Counter | On successful dodge or Parry, retaliates at advantage; third Parry in encounter grants +1 maneuver DC |
| **Warlock** (#17) | Curse Chain | Stacking pact debuffs worsen each round; at 3 stacks curse jumps to adjacent foe; removing stacks triggers Soul Debt backlash |

### 3. Continuity quick scan

[`CONTINUITY_REPORT.md`](../../src/data/CONTINUITY_REPORT.md) — wave 27 stamp appended; P0/P1 clear; no new P2 blockers.

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~9s)
```

---

## Files touched (wave 27)

- `src/data/class-draft-levels.js` — Dragoon L11, Mage L7/L11/L13/L15 enrichments
- `src/data/prestige-lorebook.json` — Hexblade, Blademaster, Warlock hallmarks
- `src/data/CONTINUITY_REPORT.md` — wave 27 continuity stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–27
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 27 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 27 append

---

## Wave 28 — class draft + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 27 cleared Dragoon/Mage slot milestones. This wave targets the five shortest remaining non-ASI stubs:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Mage** | 17 | 8th-level slots — gain one 8th-tier Resonance slot; overcast from this tier costs +2 RP beyond base and requires a successful concentration check (DC 15 + spell tier) or triggers Burnout |
| **Crimson Agent** | 7 | Sneak Attack (4d6) — extra precision damage once/turn when you have advantage or an ally is within 5 ft; Blood Marked targets take +1d6 and refresh mark duration by 1 round on hit |
| **Crimson Agent** | 11 | Sneak Attack (5d6) — extra precision damage once/turn when you have advantage or an ally is within 5 ft; Veinweave charges spent on Sneak Attack do not consume bonus action (once/turn) |
| **Thief** | 11 | Sneak Attack (6d6) — extra precision damage once/turn when you have advantage or an ally is within 5 ft; poisoned targets take +1d6 and refresh one toxin prep on hit (once/target per short rest) |
| **Monk** | 11 | Extra Attack (unarmed) — second unarmed strike when you take the Attack action; Flurry of Blows counts as one attack for Extra Attack sequencing (once/turn) |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Skipped recently enriched (waves 24–27). Next thinnest: **Wyrmslayer**, **Soulrender**, **Storm Lord**.

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Wyrmslayer** (#18) | Drakebane Arsenal | Personal weapons and forged wyrmslayer gear ignore dragon elemental resistances — on a crit vs. dragon-kin, strip one resistance category until end of your next turn |
| **Soulrender** (#14) | Soul Harvest | Absorb the soul of a dying foe within 30 ft to gain one soul charge (max = tier floor + 2); charges fuel Agony Lance and Spectral Ward without expending spell slots |
| **Storm Lord** (#15) | Static Field | Create a 15 ft charged zone that shocks enemies at start of their turn (lightning damage = tier floor d6); Voltyros-aligned foes who enter save at disadvantage |

### 3. Build

```bash
npm run build   # exit 0 (~44s)
```

---

## Files touched (wave 28)

- `src/data/class-draft-levels.js` — Mage L17, Crimson Agent L7/L11, Thief L11, Monk L11 enrichments
- `src/data/prestige-lorebook.json` — Wyrmslayer, Soulrender, Storm Lord hallmarks
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–28
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 28 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 28 append

---

## Wave 29 — class draft + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 28 cleared Mage/Crimson Agent/Thief/Monk stubs. This wave targets the five shortest remaining non-ASI stubs:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Soldier** | 11 | Extra Attack (crossbow volley) — second shot when you take the Attack action with a crossbow or hand crossbow; Overwatch reactions do not consume your Extra Attack sequencing (once/turn) |
| **Soldier** | 16 | Overwatch zone expands to 4×4 — designate a 4-tile square within weapon range; enemies entering or starting turn in the zone provoke reaction shots at advantage; Palisade allies in the zone gain half cover |
| **Mirrorsage** | 11 | Echo Slot Expansion III — max 6 witnessed spells held concurrently; releasing an echo at half Resonance cost no longer ends your Mirror Beast shift (once/encounter) |
| **Shaman** | 16 | Spirit Cache — store two flask or totem effects between rests; spending one cached effect triggers Totem Pulse on your nearest active totem without placing a new one (once/encounter) |
| **Tinker** | 15 | Danger Close — bomb and flask detonations never harm allies; friendly fire redirected as concussive push (5 ft, no damage) and grants allies +1 AC until start of your next turn |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Skipped recently enriched (waves 24–28). Next thinnest non-recent paths: **Forge Master**, **Sapper**.

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Forge Master** (#8) | Relic Imbuement | Enhance crafted items with spell-like properties — imbue one weapon or armor piece per long rest with a 1st-tier spell rider; imbued gear retains the effect until destroyed or re-forged |
| **Sapper** (#13) | Field Scanner | Gain vision of hidden traps, tunnels, or buried structures — bonus action pulse reveals traps and secret doors within 30 ft through walls up to 1 ft thick; marked hazards stay visible to allies for 1 minute |
| **Sapper** (#13) | Tripwire Arsenal | Set mechanical traps with varied effects (stun, burn, slow) — deploy two tripwires per short rest; triggered traps apply their effect in 10 ft radius and grant one Demolition Pack charge (max 3) |

### 3. Continuity quick scan

[`CONTINUITY_REPORT.md`](../../src/data/CONTINUITY_REPORT.md) — wave 29 stamp appended; P0/P1 clear; no new P2 blockers.

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~7s)
```

---

## Files touched (wave 29)

- `src/data/class-draft-levels.js` — Soldier L11/L16, Mirrorsage L11, Shaman L16, Tinker L15 enrichments
- `src/data/prestige-lorebook.json` — Forge Master, Sapper hallmarks
- `src/data/CONTINUITY_REPORT.md` — wave 29 continuity stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–29
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 29 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 29 append

---

## Wave 30 — class draft + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 29 cleared Soldier L11/L16, Mirrorsage L11, Shaman L16, Tinker L15. This wave targets the five shortest remaining non-ASI stubs flagged at wave 29 close:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Soldier** | 18 | Formation Lock extends to 5-tile radius — allies in zone gain +2 AC and cannot be moved against their will; enemies lose one movement action; Palisade deploys inside zone cost no action (once/encounter) |
| **Mirrorsage** | 16 | Mirror Beast second shift per fight — change form once/encounter without Focus; second shift retains Echo Slot hold on prior form's last witnessed spell |
| **Tinker** | 18 | Anacite Drone second upgrade module — two concurrent modules; free module switch once/turn; shared HP pool with +2 destruction threshold |
| **Crimson Agent** | 16 | Veinweave mastery — three concurrent charges; spending on Sneak Attack/Blood Mark no longer ends Stealth stance; refresh one charge when Blood Marked target drops to 0 HP (once/encounter) |
| **Crimson Agent** | 18 | Blood Mark detonation chains — Marked foe at 0 HP splashes half Sneak Attack dice to nearest enemy within 15 ft; chain preserves mark duration (once/encounter) |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Skipped recently enriched (waves 24–29). Next thinnest non-recent paths: **Battlemage**, **Beastmaster**.

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Battlemage** (#1) | Arcane Grudge | When a spellcaster damages you, gain Grudge until encounter end; next melee hit vs. that caster deals +tier floor d6 force and ignores half spell resistance |
| **Battlemage** (#1) | Spellshock Guard | After spellstrike or casting within 5 ft of a foe, gain magic resistance = half tier floor (min 2) until next turn; stacks with Battle Flow Momentum spend |
| **Beastmaster** (#2) | Shared Instinct | Bound companions inherit one combat feat you possess; commanded companion gains advantage if you had advantage on your last attack that round |

### 3. Build

```bash
npm run build   # exit 0 (~42s)
```

---

## Files touched (wave 30)

- `src/data/class-draft-levels.js` — Soldier L18, Mirrorsage L16, Tinker L18, Crimson Agent L16/L18 enrichments
- `src/data/prestige-lorebook.json` — Battlemage Arcane Grudge/Spellshock Guard, Beastmaster Shared Instinct hallmarks
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–30
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 30 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 30 append

---

## Wave 31 — class draft + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (5 thin entries)

Wave 30 cleared Soldier L18, Mirrorsage L16, Tinker L18, Crimson Agent L16/L18. This wave targets the five shortest remaining non-ASI stubs:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Tinker** | 11 | Flask/bomb capacity +1 — maintain four concurrent flasks or bombs; Dual Drone Protocols fields two Anacite Drones concurrently with independent module slots (shared deploy action economy once/turn) |
| **Soldier** | 13 | Second palisade deploy per encounter — Palisade Tier II grants +3 AC (was +2) and 15 HP threshold before destruction; deploying both palisades links them — allies moving between linked segments ignore difficult terrain |
| **Soldier** | 17 | Overwatch Advance — after a successful Overwatch reaction shot, shift 1 tile without provoking opportunity attacks; Palisade allies in your new tile gain half cover until start of your next turn |
| **Dragoon** | 18 | Dragonflight range doubled once per short rest — Wyvern's Flow leap-attacks and Apex Assault may extend to double normal range; first leap each encounter ignores opportunity attacks |
| **Monk** | 18 | Diamond Soul — advantage on all saves while unarmored and not wielding a shield; when you succeed on a save you would have failed, regain 1 Ki (once/encounter) |

All retain `draft: true`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Skipped recently enriched (waves 24–30). Next thinnest non-recent paths: **Berserker**, **Chronomancer**, **Mooncursed**.

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Berserker** (#5) | Reckless Charge | Dash up to speed through enemy spaces — each foe passed takes tier floor d6 bludgeoning and must save or be Dazed (−1 action); ends Frenzy early if charge line missed |
| **Chronomancer** (#6) | Acceleration Field | Bonus action pulse in 15 ft radius — allies gain +10 ft movement and +2 initiative until start of next turn; enemies leaving zone save or lose one reaction |
| **Mooncursed** (#12) | Lunar Tides | At night or during celestial events, Lycan Form duration doubles and Curse Surge costs no HP; during full moon, Beast Within triggers at 35% HP instead of 25% |

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

### 4. Remaining thin stub counts

| Pool | Before wave 31 | After wave 31 |
|------|----------------|---------------|
| Class draft (non-ASI, &lt;70 chars) | 15 | **10** |
| Prestige hallmarks (&lt;80 chars) | 32 | **29** |
| ASI placeholders (&lt;70 chars) | 34 | 34 (expected — not enrichment targets) |

---

## Files touched (wave 31)

- `src/data/class-draft-levels.js` — Tinker L11, Soldier L13/L17, Dragoon L18, Monk L18 enrichments
- `src/data/prestige-lorebook.json` — Berserker Reckless Charge, Chronomancer Acceleration Field, Mooncursed Lunar Tides hallmarks
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–31
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 31 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 31 append

---

## Wave 32 — class draft clearance + prestige hallmark enrichments (2026-07-30)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

### 1. Class draft level enrichment (10 thin entries — pool cleared)

Wave 31 left **10** non-ASI stubs under 70 chars. This wave clears the entire remaining pool:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Bard** | 18 | Legendary performance — Hero Path finale upgrades to 2/rest; opening a finale builds 1 Crescendo stack and grants allies within 30 ft advantage on their next save vs. fear or charm |
| **Bard** | 20 | Maestro — Crescendo cap 7; opening verse always builds 2 stacks; when you spend your last Crescendo stack, allies within 30 ft regain 1d6 HP and gain +1 to their next attack roll |
| **Cleric** | 20 | Avatar of Faith — Channel Divinity restores on short rest once/day; when you Channel, allies within 30 ft gain temp HP equal to your tier floor and advantage on saves vs. your domain's opposed damage type until start of your next turn |
| **Crimson Agent** | 20 | Crimson Apex — Blood Gauge max 8; marks persist through death saves; when you stabilize with a mark active, detonate it for half Sneak Attack dice on nearest foe within 15 ft (once/encounter) |
| **Ranger** | 18 | Primeval Awareness — sense aberrations, dragons, and fey within 1 mile while outdoors; first detection each day applies Hunter's Mark without slot cost (once/day) |
| **Tinker** | 20 | Mech Overdrive — one deployable becomes permanent for battle duration; the overcharged gadget gains +2 HP threshold and its first activation each round costs no action (once/battle) |
| **Warrior** | 11 | Mutation Slot II at full capacity — maintain three prepared serums concurrently; activating a second mutation in the same encounter no longer increases toxicity strain on allies you share with |
| **Warrior** | 16 | Serum toxicity resistance — allies take half strain when you share serums; when you activate a mutation, one ally within 10 ft may ignore toxicity strain entirely for that activation (once/encounter) |
| **Warrior** | 18 | Mutation Slot IV preview — once per encounter, gain a temporary fourth serum slot for 3 rounds; the preview slot ignores Brutality Threshold gates but applies double toxicity strain when it expires |
| **Wizard** | 18 | Spell Mastery — choose one 1st- and one 2nd-level spell from your spellbook; cast either at will without slot cost; swapping selections requires a long rest and 10 minutes of study |

All ten retain `draft: true`.

### 2. Prestige hallmark enrichment (5 thin arrays)

Skipped recently enriched (wave 31: Berserker, Chronomancer, Mooncursed). Next thinnest non-recent paths:

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Warlock** (#17) | Soul Debt | Once per encounter, spend HP equal to spell tier × 5 instead of a slot — pact spells cost half HP; dropping to 0 HP from Soul Debt triggers Curse Chain backlash on nearest foe |
| **Warlock** (#17) | Eldritch Blast | Core attack scaling with level and pact alignment — fires two beams at tier 10+; pact riders (hex, shadowstep mark) apply on either beam; beams may split targets within 30 ft |
| **Giant Killer** (#9) | Scale the Beast | Climb onto Huge+ enemies as a bonus action to target weak zones — attacks from atop ignore half cover, gain +2 crit range, and Kneecap Strike applies on hit instead of crit only |
| **Bloodbound** (#4) | Sanguine Regeneration | Passive healing on kills and crits — regain HP equal to tier floor on kill; on crit, heal half damage dealt and refresh one Bloodletting Bleed stack on the target |
| **Gravetouched** (#10) | Undying Resilience | Gain resistance to necrotic and poison damage — when reduced to 0 HP by necrotic or poison, make a save at advantage to drop to 1 HP instead (once/long rest) |

### 3. Build

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~40s)
```

### 4. Remaining thin stub counts

| Pool | Before wave 32 | After wave 32 |
|------|----------------|---------------|
| Class draft (non-ASI, &lt;70 chars) | 10 | **0** |
| Prestige hallmarks (&lt;80 chars) | 29 | **24** |
| ASI placeholders (&lt;70 chars) | 34 | 34 (expected — not enrichment targets) |

---

## Files touched (wave 32)

- `src/data/class-draft-levels.js` — Bard L18/L20, Cleric L20, Crimson Agent L20, Ranger L18, Tinker L20, Warrior L11/L16/L18, Wizard L18 enrichments
- `src/data/prestige-lorebook.json` — Warlock Soul Debt/Eldritch Blast, Giant Killer Scale the Beast, Bloodbound Sanguine Regeneration, Gravetouched Undying Resilience hallmarks
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–32
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 32 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 32 append

---

## Wave 33a — prestige hallmark enrichments (2026-07-30)

**Worker:** Overnight wave 33a  
**Commit:** none (per owner request)

### 1. Prestige hallmark enrichment (12 thin entries — pool cleared)

Re-read before write; sibling had already enriched Hexblade Hex Mark, Storm Lord Stormstep, Verdant Animist Wild Synergy, Forge Master Smith's Temper/Forge Focus, Echomancer Echo Channel/Reverb Core, Soulrender Spectral Ward/Agony Lance, and Gravetouched Grim Grasp. **12** under-80-char hallmarks remained — all enriched (priority trio first):

| Prestige | Hallmark |
|----------|----------|
| **Bloodbound** (#4) | Crimson Domination |
| **Giant Killer** (#9) | Hunter's Mark |
| **Wyrmslayer** (#18) | Fearless Roar |
| **Mooncursed** (#12) | Lycan Form |
| **Battlemage** (#1) | Momentum Surge |
| **Beastmaster** (#2) | Pack Coordination |
| **Blademaster** (#3) | Precision Flow |
| **Wyrmslayer** (#18) | Scalebreaker Technique |
| **Berserker** (#5) | Frenzy |
| **Giant Killer** (#9) | Anchor Chain |
| **Wyrmslayer** (#18) | Draconic Lore Mastery |
| **Bloodbound** (#4) | Mistform |

### 2. Build

```bash
npx tsc --noEmit   # exit 0
```

### 3. Remaining thin stub counts

| Pool | Before wave 33a | After wave 33a |
|------|-----------------|----------------|
| Class draft (non-ASI, &lt;70 chars) | 0 | **0** |
| Prestige hallmarks (&lt;80 chars) | 12 | **0** |
| ASI placeholders (&lt;70 chars) | 34 | 34 (expected — not enrichment targets) |

---

## Files touched (wave 33a)

- `src/data/prestige-lorebook.json` — 12 hallmark enrichments
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 33a section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 33a append

---

## Wave 34 — thin-depth closure + Oracle Tier I + coffee refresh (2026-07-30)

**Worker:** Overnight wave 34  
**Commit:** none (per owner request)

### 1. Thin-depth milestone — class drafts & hallmarks complete

| Pool | Status |
|------|--------|
| Class draft (non-ASI, &lt;70 chars) | **0** (cleared wave 32) |
| Prestige hallmarks (&lt;80 chars) | **0** (cleared waves 33a/33b) |
| ASI placeholders (&lt;70 chars) | 34 (expected — not enrichment targets) |

No new class-draft or hallmark enrichments this wave — milestone confirmed; coffee list refreshed to reflect author-review phase.

### 2. Oracle mystery Tier I enrichment (3 thin options)

Scanned draft mysteries — enriched the three thinnest Tier I siblings (any mystery):

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Bones** | Marrow Drain | 2d6 necrotic touch-heal; undead +50% damage and cannot regain HP until end of next turn (Pale Ledger tally) |
| **Shadow** | Shadow Step | Teleport 3 tiles in dim/dark; silent arrival; +25% damage on next concealment attack before end of turn |
| **Stars** | Guiding Bolt | 2d6 radiant bolt; star-mark 2 rounds; next ally +2 to hit and +10% crit vs marked target |

All retain `draft: true`.

### 3. Coffee review refresh

- **Downgraded:** `prestige-lorebook.json` hallmark urgency → depth complete, author tone only (#7)
- **Elevated:** Oracle full trees (#1), Paladin revelation lists (#2), L11–20 author review (#3), Umbrin lore promote (#4), Resonance multiclass draft (#5)

### 4. Build

```bash
npm run build   # exit 0
```

### 5. Continuity stamp

Wave 34 green — see `src/data/CONTINUITY_REPORT.md` §51.

---

## Files touched (wave 34)

- `src/data/oracle-mysteries.js` — Bones Marrow Drain, Shadow Shadow Step, Stars Guiding Bolt Tier I enrichments
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–34; thin-depth complete status
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 34 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 34 append
- `src/data/CONTINUITY_REPORT.md` — wave 34 continuity stamp

---

## Wave 35b — continuity stamp (2026-07-30)

**Worker:** Continuity (quick scan)  
**Commit:** none (per owner request)

### 1. Continuity re-scan (post wave 34b)

| Target | Result |
|--------|--------|
| **Umbrin / no Drow-Lolth IP** | **Pass** — product path clean; legacy migration only |
| **Hybrid-B in player UI** | **Pass** — internal docs / `resonance-economy.js` header only |
| **Wave 34b surfaces** | **Pass** — Paladin Ancients/Flame/Grief/Martyr King L5 revelations; all retain `draft: true` |
| **17 classes / Bloodbound / Oracle RC** | **Pass** — unchanged |
| **ASI placeholders** | **34** in `class-draft-levels.js` — **intentional** ability score increases, not thin-content debt |
| **Build** | `npx tsc --noEmit` **exit 0** (~9s) |

**Verdict:** **Green** — P0/P1 clear; no new P2 blockers.

### 2. Docs touched

- `src/data/CONTINUITY_REPORT.md` — wave 35 stamp + gate status line
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 35b section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this append

---

## Wave 35c — author draft enrichments (Oracle Tier I + Paladin L9) (2026-07-30)

**Worker:** Overnight wave 35c  
**Commit:** none (per owner request)

### 1. Oracle mystery Tier I enrichment (6 thin options)

Scanned draft mysteries — enriched the six thinnest Tier I siblings (any mystery; Ancestor/Battle depth target):

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Battle** | Vanguard's Step | Move 2 tiles without provoking; ally +5% DR; both gain advantage on opportunity attacks before end of turn |
| **Cataclysm** | Gale of Unmaking | 4-tile wind line — 1d6 bludgeoning, push 1 tile, −1 movement; extinguishes flames; debris → difficult terrain 1 round |
| **Life** | Thorned Shelter | +2 AC, +10% DR, +5% healing 2 rounds; first melee attacker each round takes 1d4 piercing and cannot move away until end of turn |
| **Stars** | Fate's Glimpse | Ally reroll failed roll with +2; on success you gain advantage on next Revelation save before end of next turn |
| **Stars** | Clarity | End charm/illusion/fear; +10% saves 2 rounds; reveal shapeshifted/invisible within 2 tiles for 1 round |
| **Time** | Moment's Pause | Failed save loses next action; also −10% initiative and no reactions until pause resolves |

All retain `draft: true`. **Running total:** 9 Tier I options enriched (waves 34 + 35c).

### 2. Paladin draft oath L9 enrichment (3 vs Mercy template)

Mercy baseline L9: `Channel Life — transfer HP from self to ally` (44 chars).

| Oath | L9 revelation | Change |
|------|---------------|--------|
| **Grief** | Memorial Flame | 30-ft memorial light 1 minute; reveals hidden undead; allies +2 death saves; undead in light −1 attacks |
| **Dominion** | Law's Weight | 20-ft zone 3 rounds; lawbreakers save or half speed, −2 AC, no haste/dash until zone ends |
| **Ancients** | Echo of Ages | Aura advantage vs charm/frightened 1 minute; fey/elementals entering aura fail Wis save or hesitate (no attack until end of next turn) |

All three oaths retain `draft: true`. Five other draft oaths already at or above Mercy L9 depth — deferred.

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 35c)

- `src/data/oracle-mysteries.js` — Battle/Cataclysm/Life/Stars×2/Time Tier I enrichments
- `src/data/paladin-oaths.js` — Grief / Dominion / Ancients L9 revelation enrichment
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–35c checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 35c section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 35c append

---

## Wave 36 — Oracle Tier I thin batch (2026-07-30)

**Worker:** Overnight wave 36  
**Commit:** none (per owner request)

### 1. Oracle mystery Tier I enrichment (9 thin options)

Scanned draft mysteries — enriched the nine thinnest remaining Tier I siblings (≤126 chars; Ancestor/Battle depth target):

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Dream** | Slumber Glimpse | Action loss + initiative penalty + reaction lock; next attack vs target +2 to hit |
| **Flame** | Purging Flame | 1d8 + CHA heal, disease/poison cleanse; undead equal fire + save or −10% hit from ash |
| **Time** | Echo Strike | Echo repeats weapon/touch at half damage; charge refund if echo drops target below half HP |
| **Shadow** | Fear's Whisper | Fear 2 turns + reaction lock; allies +10% crit vs feared target |
| **Battle** | Host's Cry | +10% damage/+5% DR 2 rounds; first ally kill during cry heals 1d6 + RC refund |
| **Cataclysm** | Shardburst | 1d6 bludgeoning 2-tile burst within 4 tiles; −1 movement; prone vs wall on failed save |
| **Life** | Overflowing Light | 2d6 + CHA heal; temp HP overflow; condition cleanse when temp HP fades |
| **Life** | Resonant Seed | 2-tile zone 3 rounds; ally heal + minor condition end; undead radiant + movement penalty |
| **Shadow** | Psychic Lash | 1d8 + CHA psychic; concealment bonus + Dread + reaction lock |

All retain `draft: true`. **Running total:** 18 Tier I options enriched (waves 34 + 35c + 36). **Remaining thin:** **0** at ≤126 chars; **9** mid-tier (133–168 chars: Borrowed Beat, Mark of the Doomed, Ashen Shroud, Fault Line, Mirage, Bone Whisper, False Memory, Passion's Rush, Wrathful Brand).

### 2. Paladin draft oath L9 enrichment

Mercy baseline L9: `Channel Life — transfer HP from self to ally` (44 chars).

**Scan result:** **0** draft oaths remain below Mercy depth (shortest: Vengeance L9 at 49 chars). No Paladin L9 changes this wave — deferred to future pass if Dominion/Grief-tier depth desired across all nine oaths.

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 36)

- `src/data/oracle-mysteries.js` — Dream/Flame/Time/Shadow×2/Battle/Cataclysm/Life×2 Tier I enrichments
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–36 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 36 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 36 append

---

## Wave 37 — Oracle Tier I mid-tier batch (2026-07-30)

**Worker:** Overnight wave 37  
**Commit:** none (per owner request)

### 1. Oracle mystery Tier I enrichment (9 mid-tier options)

Scanned draft mysteries — enriched the nine remaining mid-tier Tier I siblings (133–168 chars; Ancestor/Battle depth target):

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Time** | Borrowed Beat | Move 2 tiles or cast Tier I Revelation before next enemy act; no provoke on move; +2 initiative for both |
| **Battle** | Mark of the Doomed | +2 to hit/+10% crit 2 rounds; crit rider +1d6; mark strips concealment |
| **Bones** | Ashen Shroud | +10% DR/+5% necrotic resist; −10% hit/saves vs fear in 2 tiles; corpses anti-raise 1 hour on fade |
| **Cataclysm** | Fault Line | 3-tile cracked earth 3 rounds; 1d4 bludgeoning + prone vs wall on failed save; structure cracks |
| **Dream** | Mirage | Illusory duplicate 2 rounds; failed save strikes mirage; duplicate moves 1 tile/round free |
| **Bones** | Bone Whisper | Speak with Dead passive; active truth + undead save-or-stun via Pale Ledger |
| **Dream** | False Memory | False event belief 1 round; failed save −10% initiative, no reactions, +2 to hit on next attack |
| **Flame** | Passion's Rush | 1d6 fire line + −1 movement on failed save; adjacent ally +10% damage/+5% DR |
| **Flame** | Wrathful Brand | +50% fire on next hit; ally attack heals 1d6 + target save or −10% hit from embers |

All retain `draft: true`. **Running total:** **27/27** Tier I options enriched (waves 34 + 35c + 36 + 37). **Remaining thin:** **0** at ≤126 chars; **0** mid-tier (133–168 chars).

### 2. Paladin draft oath L9 enrichment

Mercy baseline L9: `Channel Life — transfer HP from self to ally` (44 chars).

**Scan result:** **0** draft oaths remain below Mercy depth. No Paladin L9 changes this wave.

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 37)

- `src/data/oracle-mysteries.js` — Time/Battle/Bones×2/Cataclysm/Dream×2/Flame×2 Tier I enrichments
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–37 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 37 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 37 append

---

## Wave 38b — continuity stamp (2026-07-30)

**Worker:** Continuity (quick scan)  
**Commit:** none (per owner request)

### 1. Continuity re-scan (post wave 37)

| Target | Result |
|--------|--------|
| **Umbrin / no Drow-Lolth IP** | **Pass** — product path clean; legacy migration in `character-storage.js` only |
| **Hybrid-B in player UI** | **Pass** — internal docs / `resonance-economy.js` header only |
| **Wave 37 surfaces** | **Pass** — Oracle 9 Tier I mid-tier enrichments; all retain `draft: true`; **27/27** Tier I depth pass complete; Tier II/III remain author-draft review |
| **17 classes / Bloodbound / Oracle RC** | **Pass** — unchanged |
| **Thin-depth debt** | **Pass** — class drafts **0** non-ASI stubs; prestige hallmarks **0** under 80 chars; **34 ASI placeholders** intentional |
| **Build** | `npx tsc --noEmit` **exit 0** (~9s) |

**Verdict:** **Green** — P0/P1 clear; no new P2 blockers.

### 2. Coffee review refresh

Oracle Tier I depth pass **27/27 complete**; Tier II/III revelation trees still **author-draft review** — coffee list intro + row #1 updated (opening brief unchanged).

### 3. Docs touched

- `src/data/CONTINUITY_REPORT.md` — wave 38 stamp + gate status line
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 38b section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this append

---

## Wave 38 — Oracle Tier II thin batch (2026-07-30)

**Worker:** Overnight wave 38  
**Commit:** none (per owner request)

### 1. Oracle mystery Tier II enrichment (9 thin options)

Scanned draft mysteries — enriched the thinnest Tier II sibling in each of the nine draft mysteries (≤130 chars; Ancestor Spirit Walk / Echo Armor depth target):

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Battle** | Divine Fury | 2-round fury window; crit save-or-Fear; bonus-action second attack if first hits |
| **Bones** | Ledger's Command | +10% damage per commanded undead; +5% DR; one intercepts next single-target hit |
| **Cataclysm** | Storm Crown | 2d6 lightning/thunder per turn; save-or-hit debuff; ally DR vs ranged + weather-prone immunity |
| **Dream** | Unreality | Miss-to-echo passive retained; once/short rest vanish-on-hit with Dread rider |
| **Flame** | Undying Ember | 2d6 adjacent fire on 0 HP; save-or-hit debuff; ally 1d6 heal in 2 tiles |
| **Life** | Verdant Pulse | +5% healing received on sub-50% heal; once/combat stabilize-at-1 + condition cleanse |
| **Shadow** | Mind Spike | 2d8 + CHA psychic; Dread on fail; +50% damage + RC refund vs already-feared |
| **Stars** | Constellation Mark | +2 to hit on marks; first crit/round +1d6 radiant + reveal through concealment |
| **Time** | Paradox Skin | Slow resistance added; once/short rest absorb ally time/aging save — reroll +2 |

All retain `draft: true`. **Running total:** 9/27 Tier II options enriched. **Remaining thin:** **5** at ≤130 chars (Radiant Path, Rotting Touch, Field Command, Night's Embrace, Nightmare Lash).

### 2. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 38)

- `src/data/oracle-mysteries.js` — Battle/Bones/Cataclysm/Dream/Flame/Life/Shadow/Stars/Time Tier II enrichments
- `tools/oracle_tier2_lengths.py` — Tier II depth scan helper (new)
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–38 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 38 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 38 append

---

## Wave 39 — Oracle Tier II complete + Tier III start (2026-07-30)

**Worker:** Overnight wave 39  
**Commit:** none (per owner request)

### 1. Oracle mystery Tier II enrichment (5 remaining thin options)

Final thin Tier II batch (≤130 chars) — all five cleared:

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Stars** | Radiant Path | 2d6 radiant line; star-ash mark; ally path-shift without provoking |
| **Bones** | Rotting Touch | Decay riders — no HP regain; corpse anti-raise; undead 2d6 + heal half |
| **Battle** | Field Command | Command mark +10% damage/+5% DR; second ally 1-tile reposition |
| **Shadow** | Night's Embrace | +5% DR allies; fear saves; enter-save lose reactions; psychic burst from zone |
| **Dream** | Nightmare Lash | 2d8 + CHA psychic; Dread + reaction lock; +50% + RC refund vs feared |

All retain `draft: true`. **Running total:** 14/27 Tier II options enriched. **Remaining thin:** **0** at ≤130 chars.

### 2. Oracle mystery Tier III enrichment (5 shortest options)

Tier III scan (`tools/oracle_tier3_lengths.py`) — **0 thin at ≤130** pre-wave; enriched the five shortest draft Tier III capstones to Echo Armor depth:

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Stars** | Concord Alignment | Once/turn ally reroll; Guiding Bolt + Constellation Mark +1 tile |
| **Life** | Song of Mending | Stabilize ends minor condition; +10% healing received |
| **Shadow** | Hush Descends | Turn-start dread save; first psychic Revelation −1 charge inside zone |
| **Dream** | Threshold Collapse | Once/round false-absence save; illusions need second disbelieve |
| **Flame** | First Flame Convergence | Wrathful-heal ally DR; Zealot's Renewal backlash suppressed |

All retain `draft: true`. **Running total:** 5/9 Tier III options enriched. **Remaining thin:** **0** at ≤130 chars; **4** remain for author tone pass (Battle, Bones, Time, Cataclysm).

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 39)

- `src/data/oracle-mysteries.js` — Battle/Bones/Dream/Shadow/Stars Tier II + Stars/Life/Shadow/Dream/Flame Tier III enrichments
- `tools/oracle_tier3_lengths.py` — Tier III depth scan helper (new)
- `src/data/CONTINUITY_REPORT.md` — wave 39 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–39 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 39 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 39 append

---

## Wave 40 — Oracle Tier III complete + Tier II mid-tier batch (2026-07-30)

**Worker:** Overnight wave 40  
**Commit:** none (per owner request)

### 1. Oracle mystery Tier III enrichment (4 remaining capstones)

Final Tier III batch — Battle, Bones, Time, Cataclysm enriched to Bloodline Convergence / First Flame Convergence depth:

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Battle** | Fury of the Host | +5% ally DR; Fear immunity; free Tier I/round; ally kill heal 1d6; Exhaustion rider |
| **Bones** | Unfinished Chorus | Drain redirect to ally; undead +5% DR; corpse anti-raise; Exhaustion rider |
| **Time** | Spiral Convergence | +2 initiative; rewind ally +10% DR; enemy save-or-lose reaction; Exhaustion rider |
| **Cataclysm** | Seal's Fracture | 2d6/round; ally prone immunity; terrain spread; structure crack; Exhaustion rider |

All retain `draft: true`. **Running total:** **9/9** Tier III options enriched. **Remaining thin:** **0** at ≤130 chars.

### 2. Oracle mystery Tier II enrichment (5 mid-tier options)

Mid-tier scan (`tools/oracle_tier2_lengths.py`) — five shortest post-thin-clear options enriched to Ancestor Spirit Walk / Echo Armor depth:

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Flame** | Crown's Burn | 2d6 fire; save-or-hit debuff; ally heal min 1d6; +5% fire DR on heal |
| **Bones** | Death's Threshold | +5% non-magic DR; undead −10% first attack while below threshold |
| **Life** | Garden of Restoration | +5% healing received; undead 1d6 radiant + save-or-hit; poison/disease cleanse on entry |
| **Cataclysm** | Upheaval | 2d6 bludgeoning; ally prone immunity + +5% DR in burst |
| **Time** | Temporal Rift | Enemy −10% first attack; ally action-reduction DR; once/rift save reroll +2 |

All retain `draft: true`. **Running total:** 19/27 Tier II options enriched. **Remaining thin:** **0** at ≤130 chars; **8** mid-tier passives/actives remain (139–160 chars).

### 3. Build

```bash
npm run build   # exit 0
```

---

## Files touched (wave 40)

- `src/data/oracle-mysteries.js` — Flame/Bones/Life/Cataclysm/Time Tier II + Battle/Bones/Time/Cataclysm Tier III enrichments
- `src/data/CONTINUITY_REPORT.md` — wave 40 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–40 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 40 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 40 append

---

## Wave 41 — Oracle Tier II mid-tier complete (2026-07-30)

**Worker:** Overnight wave 41  
**Commit:** none (per owner request)

### 1. Oracle mystery Tier II enrichment (8 remaining mid-tier options)

Final mid-tier batch (139–160 chars pre-wave) — all eight cleared to Ancestor Spirit Walk / Echo Armor depth:

| Mystery | Revelation | Enrichment |
|---------|------------|------------|
| **Battle** | Relentless Strike | Miss stack +10% damage on next hit; crit save-or-Fear; RC refund retained |
| **Cataclysm** | Instability | Force burst save-or-prone; ally +5% DR in burst as tremor passes |
| **Dream** | Shared Dream | Concealment until act; +25% psychic on first strike after dream ends |
| **Flame** | Zealot's Renewal | End minor poison/disease; +5% fire DR; adjacent 1d4 fire scatter |
| **Life** | Life Linked | +5% healing received; +10% necrotic DR; +1d4 echo heal through link |
| **Shadow** | Silent Hunter | +25% psychic + Dread on concealment opener; post-Revelation crit boost |
| **Stars** | Omen Reader | Ally +2 AC vs deadliest thread; star-ash mark +10% ally crit once/combat |
| **Time** | Rewind Wound | +5% DR +2 initiative after rewind; RC refund if undo saves from sub-half HP |

All retain `draft: true`. **Running total:** **27/27** Tier II options enriched. **Remaining thin:** **0** at ≤130 chars. **Remaining mid-tier:** **0** (139–160 chars).

### 2. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 41)

- `src/data/oracle-mysteries.js` — Battle/Cataclysm/Dream/Flame/Life/Shadow/Stars/Time Tier II enrichments
- `src/data/CONTINUITY_REPORT.md` — wave 41 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–41 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 41 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 41 append

---

## Wave 42 — Paladin L13/L17 revelation + finalOathGift spot-check (2026-07-30)

**Worker:** Overnight wave 42  
**Commit:** none (per owner request)

### 1. Paladin draft oath L13/L17 enrichment (8 thinnest vs Mercy template)

Mercy baseline: L13 `Sanctify Ground — zone removes conditions each round` (52 chars); L17 `Grace Reversal — revive fallen ally if you fall to 0 HP` (55 chars).

| Oath | Level | Revelation | Change |
|------|-------|------------|--------|
| **Silence** | L13 | Still Mind | Charm/frightened immunity while silent; allies +2 concentration if silence breaks |
| **Flame** | L17 | Phoenix Rebirth | Revive ally in aura to half HP with fire shield once/combat per ally |
| **Grief** | L17 | Echo of the Fallen | Summon fallen ally spirit for 1 round — attack or +2 AC reaction |
| **Chains Broken** | L13 | Revolution's Cry | +10 ft movement, restraint save advantage; oppressors lose reaction |
| **Ancients** | L17 | Primordial Surge | Temp HP from land; fey/elementals save or rooted |
| **Grief** | L13 | Sorrow's Weight | 20-ft zone 3 rounds; slow + 2d6 necrotic; undead auto-fail |
| **Martyr King** | L17 | Last King's Gift | Ally drops to 1 HP + temp HP equal to level once/combat per ally |
| **Dominion** | L13 | Decree of Submission | 30-ft charm or fear command; oath-breakers disadvantage |

All retain `draft: true`. **Running total:** 8 enriched this wave; remaining draft L13/L17 at or above Mercy depth — pass **ongoing**.

### 2. finalOathGift spot-check (2 thinnest enriched)

| Oath | Change |
|------|--------|
| **Chains Broken** | Liberty Unbound — oppressors in burst save or pushed 10 ft and lose reactions |
| **Martyr King** | Crown Undying — +1 saves while crown persists; redirect from two allies per round |

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 42)

- `src/data/paladin-oaths.js` — 8 L13/L17 revelation enrichments + Chains Broken/Martyr King finalOathGift
- `tools/paladin_l13_l17_lengths.js` — new L13/L17 depth scan helper
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–42 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + wave 42 append

---

## Wave 43 — Paladin L13/L17 complete + finalOathGift + Umbrin lore (2026-07-30)

**Worker:** Overnight wave 43  
**Commit:** none (per owner request)

### 1. Paladin draft oath L13/L17 enrichment (6 remaining thin vs Mercy template)

Mercy baseline: L13 52 chars; L17 55 chars. Final batch — all draft oaths now at or above enriched tier (131+ chars):

| Oath | Level | Revelation | Change |
|------|-------|------------|--------|
| **Vengeance** | L13 | No Escape | 60-ft mark lock; no teleport/invisibility/extradimensional; OA advantage on flee |
| **Vengeance** | L17 | Final Verdict | Half-HP execute save; max-dice smite + no HP regain on success |
| **Chain** | L13 | Unbreakable Bond | Charm/fright/compulsion immunity; paladin may take charm effect instead |
| **Chain** | L17 | Final Stand | Full damage absorb 1 round; ally temp HP + resistance if paladin drops |
| **Dominion** | L17 | Sovereign Mandate | Advantage vs charm/fear/compulsion; enemies cannot lie on failed Wis save |
| **Martyr King** | L13 | Throne's Grace | Lay on Hands at aura radius 3 rounds; +1 HP per die; +1 death saves |

All retain `draft: true`. **Running total:** **0** draft L13/L17 below Mercy depth.

### 2. finalOathGift enrichment (7 remaining draft gifts)

All draft `finalOathGift` texts enriched to Flame/Chains Broken depth (≥226 chars):

| Oath | Change |
|------|--------|
| **Chain** | Unbroken Covenant — temp HP on redirected damage until lock ends |
| **Mercy** | Grace Eternal — necrotic resistance + free Lay on Hands during veil |
| **Ancients** | Primordial Crown — charm-save advantage while crown persists |
| **Dominion** | Sovereign's Ascendance — failed enemies cannot lie or disobey direct command |
| **Silence** | Vow Absolute — first smite each round does not break silence vow |
| **Grief** | Dirge of Passage — survivors +2 death saves while spirits active |
| **Vengeance** | Verdict Absolute — witness frighten on execution |

Mercy retains `finalOathGiftDraft: true`. **Running total:** **10/10** gifts at depth.

### 3. UMBRIN_LORE.md clarity polish

Light copy pass — clearer section headers, tightened prose. No new cosmology; Obsidian Burn / Umbra cult / Choir orthodoxy unchanged.

### 4. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 43)

- `src/data/paladin-oaths.js` — 6 L13/L17 + 7 finalOathGift enrichments
- `tools/paladin_l13_l17_lengths.js` — hyphenated oath id fix in scan helper
- `docs/mechanics/UMBRIN_LORE.md` — clarity polish
- `src/data/CONTINUITY_REPORT.md` — wave 43 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–43 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 43 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 43 append

---

## Wave 44 — Oracle L12/L18 depth + continuity stamp (2026-07-30)

**Worker:** Overnight wave 44  
**Commit:** none (per owner request)

### 1. Oracle mysticInsight / propheticSurge / finalRevelation enrichment (9 vs Ancestor)

Ancestor baselines: mysticInsight 118 chars; propheticSurge 141; finalRevelation 228. One enrichment per draft mystery (thinnest field):

| Mystery | Field | Revelation | Change |
|---------|-------|------------|--------|
| **Battle** | propheticSurge | War Prophecy | War Chorus banner flare; allies +DR/+damage; next Tier I free |
| **Bones** | finalRevelation | Ledger Unbound | Servants intercept hits; controlled undead +damage/+DR |
| **Cataclysm** | propheticSurge | Cataclysm Prophecy | Shattered Seal weep; area +25% + prone save |
| **Dream** | propheticSurge | Dream Prophecy | Veiled Threshold; double-save illusions + hit penalty |
| **Flame** | propheticSurge | Flame Prophecy | Crown kindle; no backlash heal + fire DR allies |
| **Life** | propheticSurge | Life Prophecy | Verdant Resonance; maximized heal + healing received + undead radiant |
| **Shadow** | propheticSurge | Shadow Prophecy | Hush gather; invisible + concealment psychic + Dread |
| **Stars** | propheticSurge | Star Prophecy | Concord align; initiative + crit + ally advantage |
| **Time** | propheticSurge | Time Prophecy | Spiral fold; initiative reset + ally save reroll |

**Running totals:** mysticInsight **0/9 thin**; propheticSurge **0/9 thin**; finalRevelation **1/9 thin** (Battle Avatar of the War Chorus, 193 chars — deferred).

All retain `draft: true`. Depth passes for Oracle Tier I/II/III + Paladin L3–L20 remain **complete** — **author tone review primary**.

### 2. Build

```bash
npm run build   # exit 0 (~42s)
```

---

## Files touched (wave 44)

- `src/data/oracle-mysteries.js` — 9 L12/L18/L20 enrichments
- `tools/oracle_l12_l18_l20_lengths.py` — new L12/L18/L20 depth scan helper
- `src/data/CONTINUITY_REPORT.md` — wave 44 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–44 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 44 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 44 append (opening/coffee untouched)

---

## Wave 45 — Oracle L20 depth complete + PLAYTEST_SMOKE (2026-07-30)

**Worker:** Overnight wave 45  
**Commit:** none (per owner request)

### 1. Battle finalRevelation enrichment (last thin L20)

Ancestor baseline: finalRevelation 228 chars. Final deferred item:

| Mystery | Field | Revelation | Change |
|---------|-------|------------|--------|
| **Battle** | finalRevelation | Avatar of the War Chorus | Three War Chorus banners (offense, defense, rally); allies +DR/+damage; sacrifice banner to prevent death or restore all RC |

**Running totals:** mysticInsight **0/9 thin**; propheticSurge **0/9 thin**; finalRevelation **0/9 thin**. **Oracle depth debt cleared.**

All retain `draft: true`. Paladin + Oracle Tier I/II/III + L12/L18/L20 depth passes **complete** — **author tone review primary**.

### 2. PLAYTEST_SMOKE Oracle Paths tip

Path A step 5 expanded: L1 revelation block, Patron/Prophecy trigger, Tier I charge costs at L3, optional L1 unlock hint check. L1 revelations already at parity from wave 15b — no data edits needed.

### 3. Typecheck

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 45)

- `src/data/oracle-mysteries.js` — Battle finalRevelation enrichment
- `docs/mechanics/PLAYTEST_SMOKE.md` — Oracle Paths L1/Tier I pass criteria
- `src/data/CONTINUITY_REPORT.md` — wave 45 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–45 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 45 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 45 append (opening/coffee untouched)

---

## Wave 46 — class-draft thin pass (2026-07-30)

**Worker:** Overnight wave 46  
**Commit:** none (per owner request)

### 1. Class-draft L11–20 enrichment (5 thinnest non-ASI under 100 chars)

Scan found **10** non-ASI milestones under 100 chars (L14/L19 ASI rows excluded — intentional). Enriched the **5 thinnest**:

| Class | Level | Feature | Change |
|-------|-------|---------|--------|
| **Thief** | L18 | Uncanny Dodge improvement | Fail Dex save vs visible effect → halve damage (once/encounter); successful Dodge regains toxin prep |
| **Mage** | L20 | Archmage Reservoir | 9th-tier cast without slot; no Burnout on overcast; allies +save vs school element 1 round |
| **Ranger** | L16 | Favored Terrain mastery | Party ignores designated terrain 1 hour; +10 ft move + Stealth advantage while led |
| **Oracle** | L16 | Prophecy Trigger mastery | Fail save → regain 1 RC (once/day); allies +save vs same effect type |
| **Ranger** | L20 | Legendary Hunter | Hit Chain 2 hits; third Druidic Arrow free once/encounter, double Mark damage |

**Running totals:** **5/10** enriched; **5 remain** under 100 chars (Shaman L20, Dragoon L20, Mirrorsage L19, Thief L20, Soldier L20 — 75–83 chars). All retain `draft: true`. Oracle + Paladin depth passes **complete** (draft for author). **Coffee primary:** author tone review Oracle/Paladin/Umbrin; **secondary:** L11–20 author tables.

### 2. Build

```bash
npm run build   # exit 0 (~40s)
```

---

## Files touched (wave 46)

- `src/data/class-draft-levels.js` — 5 milestone enrichments
- `tools/scan_class_draft_lengths.py` — new L11–20 depth scan helper
- `src/data/CONTINUITY_REPORT.md` — wave 46 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–46 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 46 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 46 append (opening/coffee untouched)

---

## Wave 47 — class-draft capstone pass (2026-07-30)

**Worker:** Overnight wave 47  
**Commit:** none (per owner request)

### 1. Class-draft L20 capstone enrichment (5 remaining non-ASI under 100 chars)

Enriched the **5 remaining** L20 capstones from wave 46 backlog:

| Class | Level | Feature | Change |
|-------|-------|---------|--------|
| **Shaman** | L20 | Primal Convergence | Spirit Walk triggers sequential totem pulses; flask mist 10 ft; allies +save vs spirit effects |
| **Dragoon** | L20 | Sky Sovereign | Wyvern's Flow + Apex Assault ignore OA 1 min/day; landing tiles difficult terrain; allies half cover |
| **Mirrorsage** | L20 | Infinite Reflection | Permanent Echo Slot beyond encounter limits; half Resonance release; no Mirror Beast shift end |
| **Thief** | L20 | Master of Shadows | Sneak Attack 8d6; crit poison bypass immunity once/target/long rest; free toxin prep refresh |
| **Soldier** | L20 | Immovable Line | Formation Lock allies anti-crit 1 round post-Guardian; Palisade +5 HP; Overwatch advantage from cover |

**Running totals:** **10/10** enriched across waves 46–47; **0 remain** under 100 chars (non-ASI). Scan confirms **0 thin non-ASI**; **34 ASI placeholders** intentional. All retain `draft: true`. Oracle + Paladin depth passes **complete** (draft for author). **Coffee primary:** author tone review Oracle/Paladin/Umbrin; **secondary:** L11–20 author tables.

### 2. Build

```bash
npx tsc --noEmit   # exit 0 (~7s)
```

---

## Files touched (wave 47)

- `src/data/class-draft-levels.js` — 5 L20 capstone enrichments
- `src/data/CONTINUITY_REPORT.md` — wave 47 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–47 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 47 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 47 append (opening/coffee untouched)

---

## Wave 48 — build green + handoff refresh (2026-07-30)

**Worker:** Overnight wave 48  
**Commit:** none (per owner request)

### 1. Build

```bash
npm run build   # exit 0 (~48s)
```

No code fixes required — production build clean after waves 46–47 class-draft capstone pass.

### 2. Handoff + midnight checkpoint refresh

Refreshed opening status bar + coffee section for waves **1–48**:

- **Depth passes complete:** Oracle revelations (all tiers + L12/18/20), Paladin oaths L3–L20, class-draft non-ASI thin, prestige hallmarks thin — all 0 thin
- Still **draft for author tone review**
- **Umbrin** · **Resonance** · **17 classes** · **P0/P1 = 0** · **build green**
- Start-here paths: HANDOFF, PLAYTEST_SMOKE, COLLABORATOR_DAY1, UMBRIN_LORE, RESONANCE_CANON, CONTINUITY_REPORT

---

## Files touched (wave 48)

- `src/data/CONTINUITY_REPORT.md` — wave 48 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–48 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 48 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — opening status bar + coffee refresh; this wave 48 append

---

## Wave 49 — Druid traits + prestige capstones (2026-07-30)

**Worker:** Overnight wave 49  
**Commit:** none (per owner request)

### 1. Druid shapeshifting trait enrichment (5 stubbiest hero-form lines)

Scanned `druid-shapeshifting.js` hero forms — five shortest remaining trait lines enriched with Aethel/circle tone:

| Form | Circle | Trait | Change |
|------|--------|-------|--------|
| **Snow Leopard** | Winterfang | Claw: 2d6 cold | Glacier Claw — Winterfang ice shards; +1d4 cold vs slowed |
| **Frost Wyrmling** | Winterfang | Scales of Ice: +2 AC | Rime Scales — frost plating on ice/snow; resist nonmagical B/P/S in cold terrain |
| **Insect Broodmother** | Rotshaper | +3 AC (chitin) | Brood Chitin — layered carapace sheds once/transformation to negate one crit |
| **Charbear** | Ashen Grove | Fire Claw: 2d8 fire | Ember Claw — Ashen Grove ash ignites; ignited foes shed 1d4 fire/turn |
| **Blight Elk** | Land | Antlers: 2d8 piercing | Blight Antlers — Land-circle decay; poisoned targets save at disadvantage vs Aura of Decay |

**Running totals:** **8/42** hero traits enriched (waves 48b+49); **18 remain** under 60 chars.

### 2. Prestige capstone enrichment (3 thinnest under 100 chars)

| Path | Capstone | Change |
|------|----------|--------|
| **Berserker** (#5) | Frenzy extra action | Aethel descent-tier Frenzy; boss kill resets duration once |
| **Chronomancer** (#6) | Stored-action burst | Temporal Tower clockwork core; allies +2 initiative; 2 Fatigue stacks after |
| **Storm Lord** (#15) | Stormform | Voltyros stormform; flight 60 ft., lightning crit 19–20, 10-ft shock aura |

**Running totals:** **3/5** capstones under 100 chars enriched; **2 remain** (Blademaster #3, Beastmaster #2).

### 3. Typecheck

```bash
npx tsc --noEmit   # exit 0 (~7s)
```

---

## Files touched (wave 49)

- `src/data/druid-shapeshifting.js` — 5 hero-form trait enrichments
- `src/data/prestige-lorebook.json` — 3 capstone enrichments
- `src/data/CONTINUITY_REPORT.md` — wave 49 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–49 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 49 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 49 append (opening/coffee untouched)

---

## Wave 50a — Prestige capstones + Druid stub pass (2026-07-30)

**Worker:** Overnight wave 50a  
**Commit:** none (per owner request)

### 1. Prestige capstone enrichment (2 remaining under 100 chars)

| Path | Capstone | Change |
|------|----------|--------|
| **Beastmaster** (#2) | Pack alpha command | Bound pack acts twice/round; inherits weapon feats — Primal Pack kin across Aethel wild tiers |
| **Blademaster** (#3) | Blade Echo perfect strike | One round/short rest auto-hit on foes already struck; third auto-hit grants free Parry Counter |

**Running totals:** **5/5** capstones under 100 chars enriched; **0 remain**.

### 2. Druid shapeshifting trait enrichment (9 stubbiest hero-form lines)

Scanned `druid-shapeshifting.js` hero forms — nine shortest remaining trait lines enriched with Aethel/circle tone:

| Form | Circle | Trait | Change |
|------|--------|-------|--------|
| **Snow Leopard** | Winterfang | +10 Stealth in snow/ice | Snowveil Stealth — white-fur blur; advantage on hide after moving through snow |
| **Insect Broodmother** | Rotshaper | Wall crawl without checks | Brood Wall Crawl — brood-limbs grip decay-softened stone across lower tiers |
| **Carrion Rat King** | Rotshaper | Summon Swarm (action) | Conjure rat swarm — carrion-king calls plague-rats from undercroft tiers |
| **Blight Elk** | Land | Toxic Presence | Wither plants/taint water — poisoned drinking water imposes disadvantage on next Con save |
| **Thunderhorn Stag** | Storm | Weather Sense | Storm-circle horns tingle when Voltyros weather shifts across descent tiers |
| **Tanglemaw** | Land | Bite + Thorny Body | Rootmaw Bite + barbed Thorny Body — thorn-vines hold prey; bleed on contact |
| **Tanglemaw** | Thorns | Bite + Thorny Body | Thornmaw Bite + briar Thorny Body — restrained foes take extra damage each turn |
| **Tempest Raptor** | Storm | Storm Shroud | Storm-blood fur crackles; metal weapons touching you save or drop for 1 round |

**Running totals:** **17/42** hero traits enriched (waves 48b+49+50a); **12 remain** under 60 chars.

### 3. Typecheck

```bash
npx tsc --noEmit   # exit 0 (~7s)
```

---

## Files touched (wave 50a)

- `src/data/prestige-lorebook.json` — 2 capstone enrichments (Beastmaster, Blademaster)
- `src/data/druid-shapeshifting.js` — 9 hero-form trait enrichments
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–50a checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 50a section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 50a append (opening/coffee untouched)

---

## Wave 51 — Druid hero-form final stub pass (2026-07-30)

**Worker:** Overnight wave 51  
**Commit:** none (per owner request)

### 1. Druid shapeshifting trait enrichment (12 remaining under-60 hero-form lines)

Scanned `druid-shapeshifting.js` hero forms — all **12** remaining trait lines under 60 chars enriched with Aethel/circle tone:

| Form | Circle | Trait | Change |
|------|--------|-------|--------|
| **Blazewood Stag** | Ashen Grove | Flaming Trail: 1d8 fire on entering trail tile | Ashen Grove embers cling to ash-scorched stone across descent tiers |
| **Blazewood Stag** | Ashen Grove | Conflagration (1/long rest): 10 ft. 6d6 fire Dex save | Ashen Grove antler-burst ignites ash-choked undergrowth |
| **Charbear** | Ashen Grove | Flame Aura: 5 ft. — 1d6 fire at start of enemy turn | Ashen Grove char-hide smolders; foes in aura save or catch embers |
| **Charbear** | Ashen Grove | Smoke Cloud (action): 20-ft. heavily obscured sphere | Ashen Grove ash-choked breath blinds foes in smoldering tier smoke |
| **Frost Wyrmling** | Winterfang | Breath Weapon: 30-ft. cone 4d6 cold (1/rest in form) | Winterfang rime breath freezes tier-mist into shard hail |
| **Carrion Rat King** | Rotshaper | Poison Bite: 1d8 + 2d6 poison; DC 13 Con or poisoned | Rotshaper plague-fangs drip undercroft venom across lower tiers |
| **Tanglemaw** | Land | Root Network: sense creatures on ground within 30 ft. | Land-circle root-sense pulses through tier soil and tangled undergrowth |
| **Blight Elk** | Land | Aura of Decay: 5 ft. — 1d4 poison at start of enemy turn | Land-circle rot breath seeps from tier blight and poisoned undergrowth |
| **Blight Elk** | Thorns | Aura of Decay: 5 ft. — 1d4 poison at start of enemy turn | Thorns-circle thorn-rot seeps from blighted undergrowth |
| **Beastlord (Alpha Hybrid)** | Moon | Chimera Cub: attacks +1d4 fire/cold/lightning each | Moon-beastlord cub fangs crackle with primal tri-element bite |
| **Beastlord (Alpha Hybrid)** | Moon | Alpha Dire Wolf: action — Wis save or frightened 15 ft. | Moon-beastlord howl echoes across Aethel wild tiers |
| **Mooncursed** | Moon | Lycanthropic Resilience: resist all except silver | Moon-circle curse-flesh shrugs off steel and spell across Aethel tiers |

**Running totals:** **29/42** hero traits enriched (waves 48b–51); **0 remain** under 60 chars.

### 2. Typecheck + build

```bash
npx tsc --noEmit   # exit 0 (~7s)
npm run build      # exit 0 (~41s)
```

---

## Files touched (wave 51)

- `src/data/druid-shapeshifting.js` — 12 hero-form trait enrichments
- `src/data/CONTINUITY_REPORT.md` — wave 51 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–51 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 51 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 51 append (opening/coffee untouched)

---

## Wave 52 — handoff refresh + continuity stamp (2026-07-30)

**Worker:** Overnight wave 52  
**Commit:** none (per owner request)

### 1. Handoff opening + coffee refresh (waves 1–51)

| Surface | Change |
|---------|--------|
| **Opening brief** | Waves **1–51 done**; depth line adds prestige capstones thin + druid hero traits thin (all 0 thin) |
| **Status paragraph** | Coffee primary: author tone Oracle/Paladin/Umbrin; L11–20 author tables; Resonance multiclass still draft |
| **Coffee table** | Refreshed post wave 51 — L11–20 elevated; prestige capstones cleared; Resonance multiclass elevated primary |

**Depth passes complete:** Oracle revelations (all tiers + L12/18/20) · Paladin oaths L3–L20 · class-draft non-ASI thin · prestige hallmarks thin · prestige capstones thin · druid hero traits thin — all 0 thin; content still draft for author tone review.

### 2. Build

```bash
npm run build      # exit 0 (~53s)
```

---

## Files touched (wave 52)

- `src/data/CONTINUITY_REPORT.md` — wave 52 stamp + status line
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — opening/coffee refresh + this wave 52 append
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–52 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 52 section

---

## Wave 53 — Druid base + arch form trait enrichments (2026-07-30)

**Worker:** Overnight wave 53  
**Commit:** none (per owner request)

### 1. Druid shapeshifting trait enrichment (2 stubbiest base-form lines under 40 chars)

Scanned `druid-shapeshifting.js` **BASE_DRUID_FORMS** — enriched two remaining base trait lines under 40 chars with Aethel/wild tone:

| Form | Tier | Trait | Change |
|------|------|-------|--------|
| **Boar Form** | Base (L1–10) | Tough Hide: resistance to slashing | Gristle Hide — boar-form bristle and gristle turn blade edges along Aethel wild trails |
| **Bear Form** | Base (L1–10) | AC 14 (unless normal AC is higher) | Rootbark Hide — bear-form plate drinks tier-root impacts like storm-worn oak bark |

**Running totals:** **7/14** base traits enriched (waves 52b + 53); **6 remain** under 60 chars.

### 2. Druid shapeshifting trait enrichment (3 stubbiest arch-form lines)

Scanned `druid-shapeshifting.js` **ARCH_DRUID_FORMS** — enriched three shortest arch trait lines with Aethel/wild tone:

| Form | Tier | Trait | Change |
|------|------|-------|--------|
| **Dire Wolf** | Arch (L11–20) | Bite: 2d6 piercing | Alpha Bite — arch dire-wolf fangs tear through tier-beast hide and pack-leader prey |
| **Earth Warden (Dire Bear)** | Arch (L11–20) | 30 temp HP in form | Stoneheart Buffer — earth-warden bulk drinks tier-stone impacts like riverbed gravel under siege |
| **Ironhorn Ram** | Arch (L11–20) | AC 17 (unless higher) | Hornplate Hide — ironhorn ram-form hide rings like tier-forged bronze against wild impacts |

**Running totals:** **3/15** arch traits enriched (wave 53); **6 remain** under 60 chars.

### 3. Typecheck

```bash
npx tsc --noEmit   # exit 0 (~8s)
```

---

## Files touched (wave 53)

- `src/data/druid-shapeshifting.js` — 2 base-form + 3 arch-form trait enrichments
- `src/data/CONTINUITY_REPORT.md` — wave 53 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–53 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 53 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 53 append

---

## Wave 54 — Druid base + arch form trait enrichments (final 60-char pass) (2026-07-30)

**Worker:** Overnight wave 54  
**Commit:** none (per owner request)

### 1. Druid shapeshifting trait enrichment (6 remaining base-form lines under 60 chars)

Scanned `druid-shapeshifting.js` **BASE_DRUID_FORMS** — enriched all six remaining base trait lines under 60 chars with Aethel/wild tone:

| Form | Tier | Trait | Change |
|------|------|-------|--------|
| **Wolf Form** | Base (L1–10) | Keen Senses: advantage on Perception (hearing/smell) | + wolf-form ears and nose read Aethel wild trails and tier-shadow ambush |
| **Wolf Form** | Base (L1–10) | Bite: 1d8 piercing + DC 11 Str save or prone | + wolf-form jaws snap pack discipline onto lower-tier prey and wild trails |
| **Bear Form** | Base (L1–10) | Claw: 2d6 slashing; +1 damage per attack (rage-like) | + bear-form talons rake tier-rooted oak and wild bramble like storm fury |
| **Hawk Form** | Base (L1–10) | Keen Sight: advantage on Perception (sight) | + hawk-form eyes track tier-thermals and distant prey across Aethel descent ledges |
| **Hawk Form** | Base (L1–10) | Dive Attack: 1d4 slashing + advantage from above | + hawk-form stoop strikes from Weave updrafts between Aethel descent tiers |
| **Panther Form** | Base (L1–10) | Pounce: 20 ft. move + claw 2d4 → DC 12 Str or grappled | + panther-form spring pins prey in tier-shadow and moonlit stone |

**Running totals:** **14/14** base traits enriched (waves 52b–54); **0 remain** under 60 chars.

### 2. Druid shapeshifting trait enrichment (6 remaining arch-form lines under 60 chars)

Scanned `druid-shapeshifting.js` **ARCH_DRUID_FORMS** — enriched all six remaining arch trait lines with Aethel/wild tone:

| Form | Tier | Trait | Change |
|------|------|-------|--------|
| **Dire Wolf** | Arch (L11–20) | Pack Tactics: advantage if ally within 5 ft. | + arch dire-wolf flanks read pack-leader signals across Aethel wild tiers |
| **Dire Wolf** | Arch (L11–20) | Howl (action): 30 ft. Wis save or frightened 1 minute | + arch dire-wolf cry echoes pack-leader dread across Aethel wild tiers |
| **Sky Serpent** | Arch (L11–20) | Lightning Bite: 2d8 lightning | + sky-serpent fangs crack Weave storm-blood; wet targets spark once per transformation |
| **Sky Serpent** | Arch (L11–20) | +2 Dex saves (Glide Reflexes) | Glide Reflexes: +2 Dex saves — sky-serpent coils read Weave updrafts and dodge tier-lightning across Aethel descent air |
| **Ironhorn Ram** | Arch (L11–20) | Cannot be knocked prone | Ironhorn Stance: cannot be knocked prone — ram-form legs brace like tier-forged bronze against wild impacts and siege pushes |
| **Shadow Lynx** | Arch (L11–20) | Attacks count as magical | Shadow-Touched Strikes: attacks count as magical — arch lynx claws cut through tier-shadow wards and mundane wild defenses |

**Running totals:** **15/15** arch traits enriched (waves 53–54); **0 remain** under 60 chars.

### 3. Verification + build

```bash
node tools/scan-druid-base-arch.mjs   # BASE under60: 0 · ARCH under60: 0 · HERO under60: 0
npx tsc --noEmit                      # exit 0 (~7s)
npm run build                         # exit 0 (~40s)
```

---

## Files touched (wave 54)

- `src/data/druid-shapeshifting.js` — 6 base-form + 6 arch-form trait enrichments
- `src/data/CONTINUITY_REPORT.md` — wave 54 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–54 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 54 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 54 append

---

## Wave 55 — handoff refresh + continuity stamp (2026-07-30)

**Worker:** Overnight wave 55  
**Commit:** none (per owner request)

### 1. Handoff opening + coffee refresh (waves 1–54)

| Surface | Change |
|---------|--------|
| **Opening brief** | Waves **1–54 done**; depth line adds **all druid form traits thin (base/arch/hero)** — all 0 under 60 chars |
| **Status paragraph** | Coffee primary: author tone Oracle/Paladin/Umbrin; L11–20 author tables; Resonance multiclass still draft |
| **Coffee table** | Refreshed post wave 54 — all druid trait tiers cleared; Resonance multiclass elevated primary |

**Depth passes complete:** Oracle revelations (all tiers + L12/18/20) · Paladin oaths L3–L20 · class-draft non-ASI thin · prestige hallmarks thin · prestige capstones thin · **all druid form traits thin (base/arch/hero)** — all 0 under 60 chars; content still draft for author tone review.

### 2. Build

```bash
npm run build      # exit 0 (~45s)
```

---

## Files touched (wave 55)

- `src/data/CONTINUITY_REPORT.md` — wave 55 stamp + status line
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — opening/coffee refresh + this wave 55 append
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–55 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 55 section

---

## Wave 56 — Prestige unlock/entrance blurbs + CharacterSheet draft badges (2026-07-30)

**Worker:** Overnight wave 56  
**Commit:** none (per owner request)

### 1. Prestige unlock/entrance enrichment (5 shortest after Blademaster/Berserker/Wyrmslayer)

Scanned `prestige-lorebook.json` — five shortest remaining unlock/entrance blurbs enriched with Aethel tone; both fields updated per path:

| Path | Original (chars) | Change |
|------|------------------|--------|
| **Hexblade** (#11) | Bind yourself to a cursed weapon willingly during a blood ritual in the Hollow Vale. (84) | Hollow Vale blood rite; willing doom-oath; Weave reads Hexblade proof |
| **Battlemage** (#1) | Slay a spellcasting enemy with a melee weapon while concentrating on an active spell. (85) | Hybrid battle-flow kill along Aethel descent tiers; concentration maintained |
| **Beastmaster** (#2) | Tame and command three different CR-appropriate beasts during a wilderness trial quest. (87) | Aethel wilderness trial; three CR beasts; pack bond unbroken |
| **Chronomancer** (#6) | Solve the Paradox Puzzle in the Temporal Tower and bind yourself to its clockwork core. (87) | Temporal Tower soul-bind; stolen beats as Chronomancer proof |
| **Storm Lord** (#15) | Survive a direct lightning strike atop the Spire of Storms and awaken the spark within. (87) | Voltyros lightning atop Spire of Storms; storm-spark awakening |

**Running totals:** **8/18** unlock/entrance blurbs enriched (waves 55b+56); **10 remain** (next shortest: Sapper #13 at 91 chars).

### 2. CharacterSheet — Oracle/Paladin draft badge UX

| Surface | Change |
|---------|--------|
| **Missing selections** | Paladin oath / Oracle mystery / Oracle curse not-selected callouts now show amber **Draft** badge + "Choose in Character Builder" hint |
| **Draft content headers** | Visible **Draft** badge on oath, mystery, curse, and L20 Final Oath Gift headers (replaces inline `(draft)` parenthetical) |

### 3. Typecheck

```bash
npx tsc --noEmit   # exit 0 (~10s)
```

---

## Files touched (wave 56)

- `src/data/prestige-lorebook.json` — 5 unlock/entrance enrichments (Hexblade, Battlemage, Beastmaster, Chronomancer, Storm Lord)
- `src/components/CharacterSheet.tsx` — Oracle/Paladin Draft badge UX
- `src/data/CONTINUITY_REPORT.md` — wave 56 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–56 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 56 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 56 append (opening/coffee untouched)

---

## Wave 57 — Prestige unlock/entrance blurbs completion (2026-07-30)

**Worker:** Overnight wave 57  
**Commit:** none (per owner request)

### 1. Prestige unlock/entrance enrichment (10 remaining after wave 56)

Scanned `prestige-lorebook.json` — all ten remaining thin unlock/entrance blurbs enriched with Aethel tone; both fields updated per path:

| Path | Original (chars) | Change |
|------|------------------|--------|
| **Sapper** (#13) | Use 5 or more trap types to defeat a siege beast or construct without direct melee attacks. (91) | Aethel siege trial; five trap types; no direct melee; field-engineering proof |
| **Soulrender** (#14) | Steal the soul of a living named enemy and bind it to a black crystal during a ritual event. (93) | Hollow Vale soul-rite; named foe soul harvest; harvested agony proof |
| **Gravetouched** (#10) | Survive fatal damage while cursed by a necromancer, then rise again unaided within one round. (96) | Fatal necromancer curse; unaided rise within one round; death-touched resilience proof |
| **Forge Master** (#8) | Forge a Tier IV relic weapon using your own recipe and defeat a named foe using only that weapon. (96) | Tier IV personal recipe; named foe kill on own steel; master-forged proof |
| **Echomancer** (#7) | Absorb and successfully reuse three different monster abilities during combat with a rare Mirror Crystal equipped. (97) | Aethel mirror-trial; three distinct abilities; reflected might proof |
| **Verdant Animist** (#16) | Infuse a Seed of the World Tree during a battle and defeat at least three foes using only summoned flora. (99) | Verdant tiers; World Tree seed; flora-only kills; wild overgrowth proof |
| **Giant Killer** (#9) | Defeat a CR+3 Large or larger creature without aid, using environmental hazards or a critical weak point. (103) | Solo CR+3 Large+ foe; terrain hazards or weak point; colossal hunter proof |
| **Mooncursed** (#12) | Survive a full lunar cycle while infected with lycanthropy and pass the Beast's Trial without succumbing. (105) | Full lunar cycle; Beast's Trial; moon's verdict proof |
| **Warlock** (#17) | Forge a soul pact with an entity from beyond the known planes. Survive the Binding Trial with mind and body intact. (117) | Beyond-plane pact; Binding Trial survival; eldritch debt proof |
| **Bloodbound** (#4) | Survive a vampiric infection through a dark relic or story-driven event and accept the curse. (91) | Hollow Vale relic/story curse; willing blood-oath; sanguine surrender proof |

**Running totals:** **18/18** unlock/entrance blurbs enriched (waves 55b–57); **0 remain** under 120 chars.

### 2. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~9s)
npm run build      # exit 0 (~42s)
```

---

## Files touched (wave 57)

- `src/data/prestige-lorebook.json` — 10 unlock/entrance enrichments (Bloodbound, Echomancer, Forge Master, Giant Killer, Gravetouched, Mooncursed, Sapper, Soulrender, Verdant Animist, Warlock)
- `src/data/CONTINUITY_REPORT.md` — wave 57 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–57 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 57 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 57 append (opening/coffee untouched)

---

## Wave 58 — Resonance multiclass player-facing clarity (2026-07-30)

**Worker:** Overnight wave 58  
**Commit:** none (per owner request)

### 1. Resonance multiclass clarity (draft formula — no new math)

Player-facing breakdown for RESONANCE_CANON §7 merge without inventing new rules:

| Surface | Change |
|---------|--------|
| **`resonance-economy.js`** | `multiclassRpBreakdown()` + `formatMaxRpTooltip()` helpers; `mergeMulticlassMaxRp` metadata adds `primaryPool` + `repModifier` for line display |
| **CharacterBuilder** | Multiclass panel shows **Draft** badge + line-by-line RP merge when secondary class set; Weave tab one-line merge summary |
| **CharacterSheet** | **Multiclass Resonance merge** callout with Draft badge + bullet breakdown |
| **SessionTracker** | Max-RP `/N*` button tooltip shows full merge summary for multiclass combatants |
| **CONTINUITY_GLOSSARY** | Multiclass Resonance (draft) row; `secondaryClass` / `secondaryLevel` / `classLevels` save fields; agent checklist #9 |
| **PLAYTEST_SMOKE** | Optional stretch: Mage L8 + Cleric L4 multiclass RP merge check |

**Formula unchanged (draft):** highest-tier Weave pool + ⌈25% secondary pool⌉ + Arcane Guilds rep once.

### 2. Build hygiene

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0
```

---

## Files touched (wave 58)

- `src/data/resonance-economy.js` — multiclass breakdown helpers + enriched merge metadata
- `src/components/CharacterBuilder.tsx` — multiclass RP merge panel + Weave tab summary
- `src/components/CharacterSheet.tsx` — multiclass Resonance merge callout
- `src/components/SessionTracker.tsx` — max-RP tooltip via `formatMaxRpTooltip()`
- `src/data/CONTINUITY_GLOSSARY.md` — multiclass Resonance + save fields
- `docs/mechanics/PLAYTEST_SMOKE.md` — optional multiclass stretch step
- `src/data/CONTINUITY_REPORT.md` — wave 58 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–58 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 58 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 58 append

---

## Wave 59 — Session wild-shape stub + overcast tier wiring (2026-07-30)

**Worker:** Overnight wave 59  
**Commit:** none (per owner request)

### 1. VQ-22 Wild-shape tracker stub

| Surface | Change |
|---------|--------|
| **`druid-shapeshifting.js`** | `shapeshiftUsesAtLevel()`, `wildShapeCrCap()`, `shapeshiftFormsForDruid()` helpers |
| **SessionTracker** | Per-Druid panel: uses X/Y, CR cap badge, form picker (base/hero/arch), **Spend use**, active form callout; long rest restores uses |

### 2. VQ-23 Overcast spell-tier wiring

| Surface | Change |
|---------|--------|
| **SessionTracker** | `castSpellTier` (T1–T9) → `spellCost()` base + rep modifier; total RP preview; **Apply cast spend** deducts base + surcharge |

### 3. Class-draft + Draft badge UX

| Surface | Change |
|---------|--------|
| **`class-draft-levels.js`** | Druid L13 (Primal Recovery), L15 (Arch form attunement), L17 (CR cap +1) |
| **LevelFeatureList** | Draft-count legend with inline badge sample |

### 4. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~12s)
npm run build      # exit 0 (~42s)
```

---

## Files touched (wave 59)

- `src/data/druid-shapeshifting.js` — wild-shape session helpers
- `src/components/SessionTracker.tsx` — wild-shape panel + overcast tier wiring
- `src/data/class-draft-levels.js` — Druid L13/L15/L17 draft milestones
- `src/components/LevelFeatureList.tsx` — draft count legend polish
- `src/data/CONTINUITY_REPORT.md` — wave 59 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–59 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 59 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 59 append

---

## Wave 60 — Overcast affinity + wild-shape depth + smoke stretch (2026-07-30)

**Worker:** Overnight wave 60  
**Commit:** none (per owner request)

### 1. Overcast school affinity depth (VQ-23 follow-up)

| Surface | Change |
|---------|--------|
| **SessionTracker** | Spell name lookup (`searchSpellsByName`) sets tier + school; school pill row shows affinity/opposition hints; base cost uses `schoolAffinityMods` + rep modifier |
| **`spell-utils.js`** | `searchSpellsByName()` helper for Session table lookup |

### 2. Wild-shape depth (VQ-22 follow-up)

| Surface | Change |
|---------|--------|
| **`druid-shapeshifting.js`** | `wildShapeDurationMinutes()`, `primalRecoveryRpGain()`, `hasPrimalRecovery()` |
| **SessionTracker** | 10 min duration stub (−1 min / Revert); Primal Recovery button (L13+, once/short rest, spend use → RP regain); short rest resets Primal Recovery |

### 3. PLAYTEST_SMOKE stretch

| Surface | Change |
|---------|--------|
| **PLAYTEST_SMOKE.md** | Optional stretch rows: overcast school affinity check + Druid wild-shape / Primal Recovery |

### 4. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~12s)
npm run build      # exit 0 (~42s)
```

---

## Files touched (wave 60)

- `src/data/spell-utils.js` — `searchSpellsByName()` helper
- `src/data/druid-shapeshifting.js` — duration + Primal Recovery helpers
- `src/components/SessionTracker.tsx` — overcast affinity + wild-shape depth
- `docs/mechanics/PLAYTEST_SMOKE.md` — stretch steps for overcast + wild-shape
- `src/data/CONTINUITY_REPORT.md` — wave 60 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–60 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 60 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 60 append

---

## Wave 61 — Class-draft L11–20 gaps + Overcast Burnout hint stub (2026-07-30)

**Worker:** Overnight wave 61  
**Commit:** none (per owner request)

### 1. Class-draft L11–20 gap fill

Mirrorsage L13/L15/L17, Mage L16, Bard L13/L15/L17 — see [`OVERNIGHT_PROGRESS.md`](./OVERNIGHT_PROGRESS.md) wave 61 table.

### 2. Overcast Burnout concentration hint

Post-**Apply cast spend**, when RP drops below 25% max (and/or Mage L17+ casts T8+), Session shows **Overcast check** line with Con save DC 15 + tier (Mage L17 draft).

### 3. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~11s)
npm run build      # exit 0 (~40s)
```

---

## Files touched (wave 61)

- `src/data/class-draft-levels.js` — 7 new draft milestones
- `src/data/resonance-economy.js` — `overcastBurnoutHintAfterCast()`
- `src/components/SessionTracker.tsx` — burnout cast hint UI
- `src/data/CONTINUITY_REPORT.md` — wave 61 stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–61 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 61 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 61 append

---

## Wave 62 — Session Ethos picker + Druid L15 arch attunement badge (2026-07-30)

**Worker:** Overnight wave 62  
**Commit:** none (per owner request)

### 1. Session Ethos row picker (affinity smoke)

| Surface | Change |
|---------|--------|
| **`resonance-economy.js`** | `PLAYER_ALIGNMENTS` export (9 ethos options shared with Builder) |
| **SessionTracker** | Compact **Ethos** pill row on every ally combatant — set alignment at table without Builder re-add; live affinity hint when spell school selected |

### 2. Druid L15 arch-form attunement Session badge

| Surface | Change |
|---------|--------|
| **`druid-shapeshifting.js`** | `hasArchFormAttunement()`, `ARCH_ATTUNEMENT_MAX`, `isFreeArchAttunementSwap()` |
| **SessionTracker** | L15+ **Arch attuned X/2** badge; Shift+click arch forms to attune; free swap between attuned forms once/encounter (resets short/long rest) |

### 3. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~13s)
npm run build      # exit 0 (~43s)
```

---

## Files touched (wave 62)

- `src/data/resonance-economy.js` — `PLAYER_ALIGNMENTS` export
- `src/data/druid-shapeshifting.js` — arch attunement helpers
- `src/components/SessionTracker.tsx` — Ethos picker + arch attunement UX
- `src/data/CONTINUITY_REPORT.md` — wave 62 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–62 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 62 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 62 append

---

## Wave 63 — PLAYTEST_SMOKE Burnout stretch + class-draft L13/L15/L17 gaps (2026-07-30)

**Worker:** Overnight wave 63  
**Commit:** none (per owner request)

### 1. PLAYTEST_SMOKE stretch

| Surface | Change |
|---------|--------|
| **`PLAYTEST_SMOKE.md`** | Optional stretch: **Overcast Burnout hint** after heavy overcast (Mage L17+ tier 8+, RP &lt; 25% post-cast); **Ethos row** pill smoke; **Druid arch attunement** L15 badge smoke |

### 2. Class-draft L11–20 gaps

| Surface | Change |
|---------|--------|
| **`class-draft-levels.js`** | Cleric/Monk/Ranger/Dragoon L13/L15/L17 + Tinker L13/L17 — **14 draft milestones** (Aethel tone, `draft: true`) |

### 3. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~8s)
npm run build      # exit 0 (~40s)
```

---

## Files touched (wave 63)

- `src/data/class-draft-levels.js` — 14 new draft milestones
- `docs/mechanics/PLAYTEST_SMOKE.md` — stretch rows
- `src/data/CONTINUITY_REPORT.md` — wave 63 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–63 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 63 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 63 append

---

## Wave 64 — Shaman totem Session stub (2026-07-30)

**Shipped:** `SessionTracker.tsx` now gives Shaman combatants a persistent, table-facing totem placement row:

- **L6+:** place or recall one Spirit, Echo, Divining, or Blight totem.
- **L13 draft+:** second active totem slot, visibly identified as draft-derived.
- **Long rest:** clears placed totems; ordinary Session persistence retains them between reloads.
- **Guardrail:** no effect, duration, damage, targeting, or pulse automation was invented. Resolve those through the Shaman path and GM.

**Class gap scan:** Paladin, Wizard, and Warrior L13/L15/L17 are already canon entries in `class-details.js`; intentionally no overlapping drafts were added.

**Validation:** `npx tsc --noEmit` (0, ~10s) · `npm run build` (0, ~41s).  
**Commit:** none.

### Suggested wave 65

Add a small PLAYTEST_SMOKE row for Shaman L6/L13 totem placement/recall, then have the author either supply a canonical per-totem effect table or keep the tracker as the explicit GM-resolved stub. Avoid Oracle/Paladin/Umbrin prose review unless the owner reopens it.

---

## Wave 65 — Shaman smoke coverage + hero-form trait depth (2026-07-30)

**Shipped:**

- **Shaman smoke coverage:** `PLAYTEST_SMOKE.md` now verifies L6 place/recall, L13's two distinct active slots and third-slot enforcement, plus long-rest clearing. It explicitly preserves GM resolution for all Totem Pulse and per-totem behavior.
- **Hero-form depth:** `druid-shapeshifting.js` enriches the remaining 13 concise hero-form traits across Moon, Storm, Thorns, Winterfang, and Rotshaper. No numeric values, ranges, action economy, or mechanical effects changed.

**Validation:** `npx tsc --noEmit` (0, ~11s).  
**Commit:** none.

### Suggested wave 66

Run the new Shaman smoke row manually in the browser, then inspect the Burnout badge/rest-clear behavior only if a concrete rough edge appears. Keep per-totem effect automation deferred until canon supplies a table.

---

## Wave 66 — Burnout recovery exits + Items Library no-results polish (2026-07-30)

**Shipped:**

- **Burnout recovery UX:** the transient post-cast **Overcast check** hint now clears on **Short Rest**, **Long Rest**, and direct **Full** Resonance restore. The existing Overcast **Clear** control already cleared it and remains intact. The calculated Burnout badge, threshold, and draft consequence stub are unchanged.
- **Items Library recovery UX:** a zero-match search/filter no longer leaves an empty catalog column. It explains that no dropped/crafted items match and presents an in-place **Clear all filters** action.

**Validation:** `npx tsc --noEmit` (0) · `npm run build` (0, ~47s).  
**Commit:** none.

### Suggested wave 67

Manually smoke the two recovery paths: trigger an Overcast hint, then use **Short Rest**, **Long Rest**, and **Full** to confirm it vanishes while the threshold badge reflects current RP; filter Items Library to zero matches and reset from the empty state. If further overnight work is needed, add only a glossary clarification for Session’s persisted fields (totem slots, arch attunement, ethos) after checking existing definitions; keep Oracle/Paladin/Umbrin tone review and per-totem automation deferred.

---

## Wave 67 — Session continuity + library empty-state parity (2026-07-30)

**Shipped:**

- **Continuity glossary:** Records the exact persisted Session combatant fields for Shaman totem placement, Druid arch attunement, one-free-swap tracking, the Ethos row, and transient `burnoutCastHint`. The addendum makes explicit that totems remain GM-resolved and that Short/Long Rest reset only the arch swap flag while attunements persist.
- **Spells Library recovery UX:** A zero-result query, filter combination, or empty Learned/Favorites view now offers **Clear all filters**. It returns to All and clears discovery inputs without erasing learned or favorite spell selections.
- **Bestiary recovery UX:** Search is now treated as an active filter; a zero-result state offers **Clear all filters** that clears search and dropdown filters together.

**Validation:** `npx tsc --noEmit` + `npm run build` pending.  
**Commit:** none.

### Suggested wave 68

Manually smoke the three zero-result recovery states (Items, Spells—including Learned/Favorites, and Bestiary search), then run the existing Burnout recovery checks. If all pass, keep overnight work to a narrow Session usability defect or an author-approved draft-content batch; do not reopen Oracle/Paladin/Umbrin tone review or add per-totem behavior without canon.

---

### Wave 67 validation update

`npx tsc --noEmit` **passed** (~10s) and `npm run build` **passed** (~41s).

---

## Wave 68 — Recovery smoke coverage + Ashen Grove draft enrichment (2026-07-30)

**Shipped:**

- **Recovery smoke coverage:** `PLAYTEST_SMOKE.md` now has concrete optional-stretch rows for zero-result recovery in **Items**, **Spells** (including Learned/Favorites), and **Bestiary**. The new Burnout row repeats the trigger and confirms that **Short rest**, **Long rest (+8h)**, and direct **Full** restore clear the transient Overcast check hint.
- **Ashen Grove draft clarity:** Charbear and Blazewood Stag are now explicitly draft hero forms in `druid-shapeshifting.js`; `ClassPathDisplay` renders their shared **Draft** badge. Six existing traits received descriptive context only—no values, range, action economy, effects, unlocks, or availability changed.
- **Deferred scope preserved:** No Oracle/Paladin/Umbrin author-tone review and no per-totem automation.

**Validation:** `npx tsc --noEmit` + `npm run build` pending.  
**Commit:** none.

### Suggested wave 69

Run the new four smoke rows in a browser with a persisted Mage and confirm the Draft badge appears only for Circle of the Ashen Grove. If an actual recovery defect appears, fix that narrow behavior; otherwise inspect filter-bearing Encounters/Generators for an equivalent actionable empty state. Keep authored class/lore expansion and totem effects deferred until canonical source material is supplied.

---

### Wave 68 validation update

`npx tsc --noEmit` **passed** and `npm run build` **passed** (~49s).

---

## Wave 69 — Encounters filter recovery parity (2026-07-30)

**Shipped:**

- **Actionable Floor Encounters empty states:** An active search now reports its tier-match count and displays **Clear filters**. A zero-tier match gets a dedicated reset card; a query that only empties the chosen tier’s Safe Havens or Points of Interest gets the same in-place reset. Positive search matches still let the GM jump directly to a matching tier.
- **Generators audited and skipped:** Its tier buttons drive generation only; it does not have a filtered catalog or filter-driven empty state, so no fake recovery UI was added.
- **No redundant draft expansion:** Wave 65 completed the remaining concise Druid hero traits and wave 68 completed Ashen Grove’s draft context. This wave does not retouch Oracle, Paladin, Umbrin, or totem automation.

**Validation:** `npx tsc --noEmit` (0) · `npm run build` (0, ~48s).  
**Commit:** none.

### Suggested wave 70

Run the Floor Encounters smoke path with (1) a no-tier-match query and (2) a query that matches another tier but empties the currently selected tier’s havens/POIs; verify each reset restores the same selected tier and leaves **Load in Session** intact. If both pass, choose a new author-approved draft-content batch from a fresh thin-copy scan rather than revisiting completed Druid traits or Oracle/Paladin/Umbrin tone.

---

## Wave 70 — Encounter smoke stretch + cosmology draft flavor (2026-07-30)

**Shipped:**

- **Floor Encounters smoke coverage:** `PLAYTEST_SMOKE.md` now provides deterministic searches for both recovery modes: `zzzz-wave-70` for the global zero-tier reset and T1 `Crystalfront` for the POI-only local reset. Both checks preserve the selected tier and its **Load in Session** control.
- **Fresh draft content batch:** World of Aethel sections X and XI now show the existing draft treatment while their short export and forbidden-school labels gain presentation flavor only. Existing goods, locations, school names, spell access, restrictions, costs, and rules remain unchanged.
- **Deferred scope preserved:** Oracle/Paladin/Umbrin author tone work, totem automation, and 3D work remain untouched.

**Validation:** `npx tsc --noEmit` (0) · `npm run build` pending.  
**Commit:** none.

### Suggested wave 71

Run the two deterministic Floor Encounters smoke paths in a browser and confirm that both reset controls preserve the current tier and **Load in Session**. If they pass, prefer a fresh, source-bounded thin-copy scan outside Oracle/Paladin/Umbrin (for example non-mechanical dungeon/cosmology extract labels) and keep every enrichment visibly draft; do not add totem effect automation without a canonical table.

---

### Wave 70 validation update

`npx tsc --noEmit` **passed** (~8s) and `npm run build` **passed** (~41s).

**Clarification:** The fresh draft batch expands eight concise cosmology labels under the X/XI draft markers; no existing goods, places, school names, or rules changed.

---

## Wave 71 — Draft label consistency + cosmology trade flavor (2026-07-30)

**Shipped:**

- **Draft badge consistency:** Circle of the Ashen Grove is now marked `(draft)` in the Builder selector; its selected circle, hero-form heading, and individual forms show draft status. Character Sheet repeats that status beside the circle and hero-form names. Session’s form picker and active-form line preserve it as well.
- **Draft flavor batch:** The existing World X draft extract gains presentation-only context for **Divine Essence** and **Shard Markets**. The named goods, locations, trade rule, and all mechanics remain unchanged.
- **Deferred scope preserved:** Oracle/Paladin/Umbrin tone review, totem automation, and 3D work remain untouched.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~50s).  
**Commit:** none.

### Suggested wave 72

Run a compact persisted-Ashen-Grove smoke pass across Builder → Sheet → Session: select the circle, confirm every draft marker is visible, add the character to Session, select a hero form, and verify no non-Ashen circle shows a draft label. If it passes, inspect a fresh, source-bounded non-mechanical dungeon or cosmology extract label batch; keep mechanics and totem effects deferred.

---

## Wave 72 — Ashen Grove persistence smoke + legends draft flavor (2026-07-30)

**Shipped:**

- **Persisted Ashen Grove smoke:** `PLAYTEST_SMOKE.md` now gives one reproducible Builder → refresh → Sheet → Session path for a saved Ashen Grove Druid. It checks draft markers for the selected circle and both hero forms, then validates Session’s picker and active-form status. It also explicitly guards against status leaking to a non-Ashen circle.
- **Source-bounded draft batch:** World XIII **Legends & Songs** is now visibly draft. Its three pre-existing source labels are unchanged; each has a short, presentation-only Draft color blurb.
- **Scope preserved:** No mechanics, source promotion, history/NPC expansion, Oracle/Paladin/Umbrin review, totem automation, or 3D work.

**Validation:** `npx tsc --noEmit` + `npm run build` pending.  
**Commit:** none.

### Wave 72 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~43s).

### Suggested wave 73

Run the persisted Ashen Grove smoke path in a browser and, if a real visibility or persistence defect appears, fix that narrow issue. Otherwise, choose a fresh source-bounded non-mechanical extract outside the completed World X/XI/XIII batches; keep every enrichment short and explicitly draft, with no automated totem behavior.

---

## Wave 73 — Appendix draft flavor + Dungeon Guide empty state (2026-07-30)

**Shipped:**

- **Source-bounded draft batch:** World XV **Appendices** is now visibly draft. Its four pre-existing source labels remain unchanged; each has one short presentation-only Draft color line. No chronology, lineage, dungeon-reference, or calendar fact was added.
- **Dungeon Guide recovery:** Tier Details now shows a clear zero-match state and **Clear filters** action when a search or mapped-only combination has no matching tier. It no longer presents a stale tier outside the active filter.
- **Scope preserved:** No mechanics, source promotion, Oracle/Paladin/Umbrin review, totem automation, or 3D work.

**Validation:** `npx tsc --noEmit` + `npm run build` pending.  
**Commit:** none.

### Suggested wave 74

Run the persisted Ashen Grove smoke path only if browser capacity is available; fix a confirmed narrow defect if found. Otherwise, inspect a fresh source-bounded non-mechanical cosmology or dungeon label batch outside World X/XI/XIII/XV, or add an equivalent filter-reset recovery where an active filter can still leave a stale detail view.

---

### Wave 73 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~47s).

---

## Wave 74 — Dungeon Guide overview recovery smoke (2026-07-30)

**Shipped:**

- **Overview recovery:** Dungeon Guide’s Overview grid now replaces a true zero-match result with an in-place **Clear filters** action. This matches Tier Details recovery without changing tier data, selection, or filter semantics.
- **PLAYTEST_SMOKE stretch:** A deterministic `zzzz-wave-74` path verifies the Overview recovery card, reset behavior, all-ten-tier return, and selected-tier preservation.
- **Scope preserved:** No cosmology or prestige flavor batch was added: the remaining fresh World sections are source-gap placeholders, mechanics, or explicitly superseded. Oracle/Paladin/Umbrin tone review, totem automation, and 3D work remain untouched.

**Validation:** `npx tsc --noEmit` + `npm run build` pending.  
**Commit:** none.

### Suggested wave 75

Browser-smoke the Tier Details and Overview zero-result paths together, including a mapped-only plus impossible-query combination. If both preserve selected tier and reset cleanly, prefer a new source-bounded lore batch only after a fresh non-mechanical extract with usable labels is identified; otherwise inspect a separate Session or Builder recovery path from the current handoff.

### Wave 74 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s).

---

## Wave 75 — Dungeon Guide paired recovery smoke (2026-07-30)

**Shipped:**

- **Paired recovery smoke:** `PLAYTEST_SMOKE.md` now exercises Tier Details and Overview with the same deterministic `zzzz-wave-75` impossible query plus **Mapped tiers only**. Each reset must retain the selected tier while restoring its respective tier controls.
- **Mechanics recovery:** Dungeon Guide’s filtered **Victory Consequences by Tier** list now has an explicit no-match explanation and **Clear filters** action instead of a blank list. The same smoke addendum verifies reset restores all ten consequence rows.
- **Scope preserved:** No source facts, mechanics, Oracle/Paladin/Umbrin review, prestige prose, totem automation, or 3D work changed.

**Validation:** `npx tsc --noEmit` + `npm run build` pending.  
**Commit:** none.

### Suggested wave 76

Run the paired Dungeon Guide smoke in a browser when available. If it passes, prioritize a confirmed, source-bounded draft extract with usable untouched labels; otherwise fix only a reproducible recovery or state-preservation defect found on the smoke path.

### Wave 75 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s).

---

## Wave 76 — Races draft color + prestige hallmark provenance (2026-07-30)

**Shipped:**

- **Fresh source-bounded cosmology batch:** World VIII **Races of Aethel** is now visibly draft. Its five existing extract labels remain unchanged; each receives one presentation-only color line. No ancestry, origin, location, ability, or gameplay fact was added.
- **Prestige thin-copy pass:** Bloodbound’s **Bloodletting Strikes**, Forge Master’s **Ember Pulse**, and Hexblade’s **Doom Sigil** now have compact draft flavor. The Builder and Character Sheet show a small **draft** badge on precisely those hallmarks; the underlying mechanical claims remain unchanged.
- **Scope preserved:** No Dungeon Guide recovery work, source promotion, mechanics, Oracle/Paladin/Umbrin tone review, totem automation, or 3D work.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~48s).  
**Commit:** none.

### Suggested wave 77

Browser-check the new World VIII draft marker and all three prestige draft badges in Builder and Character Sheet. If they render correctly, run the existing paired Dungeon Guide recovery smoke only for a real regression, then seek another confirmed source-bounded non-mechanical batch rather than adding more empty-state recovery.

---

## Wave 77 — prestige provenance smoke + thin-copy pass (2026-07-30)

**Shipped:**

- **PLAYTEST_SMOKE coverage:** A new deterministic optional stretch checks World VIII’s visible **Draft** marker, then confirms Builder → Sheet badge persistence for the three wave 76 hallmark enrichments: Bloodbound’s **Bloodletting Strikes**, Forge Master’s **Ember Pulse**, and Hexblade’s **Doom Sigil**.
- **Next prestige thin batch:** Sapper’s **Demolition Pack** and **Saboteur’s Toolkit**, plus Soulrender’s **Echo of Death**, now have compact draft flavor. Their `draftHallmarkIndices` make the existing small **draft** badge visible in both Builder and Character Sheet.
- **Scope preserved:** No numeric effect, prerequisite, capstone, class eligibility, Dungeon Guide empty-state work, Oracle/Paladin/Umbrin review, totem automation, source promotion, or 3D work.

**Validation:** pending wave 77.  
**Commit:** none.

### Suggested wave 78

Run the new Wave 77 Builder → Sheet smoke path and validate typecheck/build. If it passes, only pursue a fresh, source-bounded cosmology or dungeon flavor extract with a confirmed gap; do not re-open empty-state recovery without a regression.

### Wave 77 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~45s).

---

## Wave 78 — prestige thin batch + Myth & History draft flavor (2026-07-30)

**Shipped:**

- **Next prestige thin batch:** Hexblade’s **Blade Hunger**, Storm Lord’s **Eye of the Tempest**, Verdant Animist’s **Living Terrain**, and Warlock’s **Pact Sigils** now have compact draft flavor. Their `draftHallmarkIndices` expose the existing small **draft** badge in Builder and Character Sheet.
- **Fresh source-bounded cosmology batch:** World VII **Myth & History** is visibly draft. Its five existing extract labels remain intact; each has one presentation-only Draft color line. No chronology, people, places, or dungeon facts changed.
- **Scope preserved:** No numeric effect, prerequisite, capstone, class eligibility, Oracle/Paladin/Umbrin review, totem automation, Dungeon Guide empty-state work, source promotion, or 3D work.

**Validation:** pending wave 78.  
**Commit:** none.

### Suggested wave 79

Smoke the four new hallmark badges through Builder → Sheet and World VII’s visible Draft marker. If they render correctly, run a fresh thin-capstone scan and add only a source-bounded, explicitly draft batch; avoid reopening completed empty-state work or author-tone review.

### Wave 78 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s).

---

## Wave 79 — wave 78 badge smoke + short prestige capstones (2026-07-30)

**Shipped:**

- Wave 78’s four hallmark draft markers now have deterministic Builder → Sheet smoke coverage.
- The short-capstone scan selected **Gravetouched**, **Warlock**, **Battlemage**, and **Hexblade**. Their expanded presentation-only draft prose carries a new normalized `draftCapstone` flag, rendered as a compact **draft** badge in Builder and Sheet.
- No capstone resolution, eligibility, prerequisites, source facts, Oracle/Paladin/Umbrin review, totem automation, or 3D work changed.

**Validation:** pending wave 79.  
**Commit:** none.

### Suggested wave 80

Browser-run both Wave 79 provenance paths. Then scan the remaining undrafted capstones before considering a second small, explicitly draft batch; preserve the current badge-only presentation boundary.

### Wave 79 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). Commit: none.

---

## Wave 80 — second prestige capstone draft batch (2026-07-30)

**Shipped:**

- **Short-capstone scan:** The next four shortest still-undrafted capstones — **Sapper** (111 chars), **Forge Master** (114), **Bloodbound** (116), and **Echomancer** (118) — now carry expanded, presentation-only draft prose and `draftCapstone: true`.
- **Provenance smoke:** `PLAYTEST_SMOKE.md` now has one Builder → Sheet path for precisely those four compact **draft** capstone badges. It explicitly keeps resolution and automation out of scope.
- **Scope preserved:** No capstone numerical resolution, class eligibility, prerequisites, Oracle/Paladin/Umbrin author review, totem automation, cosmology/dungeon facts, or 3D work changed.

**Remaining:** **10** undrafted prestige capstones remain (the 18 total minus eight draft-badged capstones).

**Validation:** pending wave 80.  
**Commit:** none.

### Suggested wave 81

Run the Wave 80 provenance path in-browser if a visual pass is wanted, then choose either the next four shortest undrafted capstones (Wyrmslayer, Verdant Animist, Mooncursed, Giant Killer; Echomancer’s 118-char tie was resolved by lower path number) or a fresh source-bounded cosmology/dungeon draft extract with a confirmed gap.

### Wave 80 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~47s). Commit: none.

---

## Wave 81 — third prestige capstone draft batch (2026-07-30)

**Shipped:**

- **Short-capstone scan:** The next four shortest still-undrafted capstones — **Wyrmslayer** (118 chars), **Verdant Animist** (121), **Mooncursed** (122), and **Giant Killer** (126) — now carry expanded, presentation-only draft prose and `draftCapstone: true`.
- **Provenance smoke:** `PLAYTEST_SMOKE.md` now has one Builder → Sheet path for precisely those four compact **draft** capstone badges. It explicitly keeps resolution and automation out of scope.
- **Scope preserved:** No capstone numerical resolution, class eligibility, prerequisites, Oracle/Paladin/Umbrin author review, totem automation, cosmology/dungeon facts, or 3D work changed.

**Remaining:** **6** undrafted prestige capstones remain (the 18 total minus 12 draft-badged capstones).

**Validation:** pending wave 81.  
**Commit:** none.

### Suggested wave 82

Run the Wave 81 Builder → Sheet provenance path in-browser if a visual pass is wanted, then rescan and draft-enrich the next four shortest of the remaining six undrafted prestige capstones. Preserve the badge-only presentation boundary and append the result to the overnight docs.

### Wave 81 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~43s). Commit: none.

---

## Wave 82 — fourth prestige capstone draft batch (2026-07-30)

**Shipped:**

- **Short-capstone rescan:** The next four shortest remaining undrafted capstones — **Soulrender**, **Blademaster**, **Berserker**, and **Storm Lord** — now carry expanded, presentation-only draft prose and `draftCapstone: true`.
- **Provenance smoke:** `PLAYTEST_SMOKE.md` now has one Builder → Sheet path for precisely those four compact **draft** capstone badges. It explicitly keeps resolution and automation out of scope.
- **Scope preserved:** No capstone numerical resolution, class eligibility, prerequisites, Oracle/Paladin/Umbrin author review, totem automation, cosmology/dungeon facts, or 3D work changed.

**Remaining:** **2** undrafted prestige capstones remain: **Beastmaster** and **Chronomancer**.

**Validation:** pending wave 82.  
**Commit:** none.

### Suggested wave 83

Draft-enrich the final two capstones, **Beastmaster** and **Chronomancer**, then run their Builder → Sheet draft-badge provenance check. Preserve the presentation-only boundary and append the result to the overnight docs.

### Wave 82 validation update

`npx tsc --noEmit` passed (~12s) and `npm run build` passed (~42s). Commit: none.

---

## Wave 83 — final prestige capstone draft batch (2026-07-30)

**Shipped:**

- **Final capstone rescan:** **Beastmaster** and **Chronomancer** now carry expanded, presentation-only draft prose and `draftCapstone: true`.
- **Provenance smoke:** `PLAYTEST_SMOKE.md` now names the Builder → Sheet check for both final compact **draft** capstone badges.
- **Completion:** The complete 18-path scan reports **0** prestige capstones without `draftCapstone`.
- **Scope preserved:** No capstone numerical resolution, class eligibility, prerequisites, Oracle/Paladin/Umbrin author review, totem automation, cosmology/dungeon facts, or 3D work changed.

**Remaining:** **0** undrafted prestige capstones remain.

**Validation:** pending wave 83.  
**Commit:** none.

### Suggested wave 84

Optional small next lane: add a concise prestige-capstone draft-completeness note to the morning handoff after an author confirms the presentation pass. Do not promote, resolve, or automate any capstone.

### Wave 83 validation update

`npx tsc --noEmit` passed and `npm run build` passed (build ~47s). The JSON scan confirms `18/18` `draftCapstone: true`; **0** remain undrafted. No commit created.

---

## Wave 84 — prestige presentation handoff + unmapped-depth draft extract (2026-07-30)

**Shipped:**

- **Morning author schedule:** Wave 83’s complete prestige-capstone presentation pass is logged for review: **18/18** paths are draft-badged and **0** remain. This is a scheduling handoff only; no capstone is promoted, resolved, or given new mechanics.
- **Dungeon draft batch:** Tiers **6–10** now have richer presentation-only copy for their existing tier, haven, point-of-interest, gate, and boss labels. Each unmapped tier carries a visible **Draft extract** badge and an in-context scope note that its routes, hazards, encounter resolution, and maps remain unconfirmed.
- **Source boundary:** Copy stays within the existing `floor-encounters.json` labels and survivor-rumor framing. No new places, bosses, rewards, procedures, or mechanical effects were introduced.

**Remaining:** Prestige capstones **0/18** undrafted; prestige hallmarks **0/18** without the existing draft treatment; mapped dungeon tiers **5/10**, with T6–T10 deliberately still unmapped draft extracts.

**Validation:** pending Wave 84.  
**Commit:** none.

### Suggested wave 85

After author scheduling, either run a narrow visual pass for the new unmapped-depth **Draft extract** notice and preserve the source boundary, or select a separate thin blurb lane only after confirming its entries are presentation-only and already source-bounded. Do not reopen Oracle/Paladin/Umbrin review or promote prestige drafts.

### Wave 84 validation update

`npx tsc --noEmit` passed and `npm run build` passed (build ~50s). No commit created.

### Wave 84 hallmark completion update

The strict hallmark scan found **18/18** paths with hallmark records, **0** entries under 80 characters, and two still under the requested 100-character presentation target: Sapper **Saboteur’s Toolkit** (92) and Soulrender **Echo of Death** (97). Both are now expanded as explicitly draft, presentation-only copy; the rescan is expected to report **0** under 100. The 10 previously explicit `draftHallmarkIndices` entries remain draft-badged; not every hallmark is a draft entry.

### Wave 84 final validation

`npx tsc --noEmit` and `npm run build` passed (build ~47s). Final scan: **18/18** paths with hallmarks, **0** under 80, **0** under 100; **18/18** draft capstones and **0** undrafted. No commit created.

---

## Wave 85 — unmapped-depth visibility smoke + feat draft batch (2026-07-30)

**Shipped:**

- **Dungeon Guide draft visibility:** T6–T10 now render their existing `draftNote` directly in **Tier Details**, paired with a visible **Draft extract** badge. The note is included in Dungeon Guide search matching, so the provisional status is discoverable without inventing mapped content.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now provides a deterministic T6–T10 pass for the new notice, including the source boundary: route, hazard, map, and encounter-resolution content remains unconfirmed.
- **Feat thin-description batch:** **Acrobatic Mastery**, **Arcane Armor**, **Arcane Flexibility**, and **Arcane Pulse** replace the generic compendium placeholder with short, draft presentation copy bounded by their existing prerequisite and effect fields. Builder shows a compact **Draft** badge for precisely these entries.

**Scope preserved:** No feat prerequisite or effect changed; no feat behavior was automated. T6–T10 remain unmapped. No Oracle/Paladin/Umbrin author-tone work, totem automation, new dungeon facts, source promotion, 3D work, deletion, or commit occurred.

**Validation:** pending Wave 85.

### Suggested wave 86

Run the Wave 85 T6–T10 and feat-provenance smoke in-browser. If it passes, choose the next four generic feat placeholders only after confirming each enrichment can stay bounded to its existing prerequisite/effect text and draft badge; otherwise repair only a confirmed visibility defect.

### Wave 85 validation update

`npx tsc --noEmit` passed (~10s) and `npm run build` passed (~43s). No commit created.

---

## Wave 86 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Arcane Recall**, **Arcane Transfusion**, **Armor Crusher**, and **Battle Awareness** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one type-filtered Builder pass covering all four descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **84** exact generic placeholder descriptions remain. The separate short-effect scan reports **8** draft feats under 80 characters because it evaluates untouched effect strings, not descriptions.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** pending Wave 86.  
**Commit:** none.

### Suggested wave 87

Select the next four exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching Builder provenance smoke and rerun the scans. Do not convert the short-effect metric into a rules-rewrite lane.

### Wave 86 scan correction

The completed exact-placeholder scan reports **112** remaining descriptions, superseding the earlier provisional **84** figure.

### Wave 86 validation update

`npx tsc --noEmit` passed (~7s) and `npm run build` passed (~47s). No commit created.

---

## Wave 87 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Battlefield Commander**, **Battlefield Tactician**, **Beast Whisperer**, **Berserker Rage**, **Bleeding Edge**, **Blood Magic**, **Brace for Impact**, and **Break Line** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **104** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** pending Wave 87.  
**Commit:** none.

### Suggested wave 88

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

---

### Wave 93 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **56** remaining. No commit created.

### Wave 87 validation update

`npx tsc --noEmit` passed (~8s) and `npm run build` passed (~41s). The exact generic-placeholder scan reports **104** remaining. No commit created.

---

## Wave 88 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Bull Rush**, **Channeled Flow**, **Cleaving Momentum**, **Climb Anywhere**, **Close Quarters Combat**, **Cold Reader**, **Combat Intuition**, and **Combat Slide** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **96** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** pending Wave 88.  
**Commit:** none.

### Suggested wave 89

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Wave 88 validation update

`npx tsc --noEmit` passed and `npm run build` passed (~44s). The exact generic-placeholder scan reports **96** remaining. No commit created.

---

## Wave 89 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Concentrated Will**, **Counterspell Adept**, **Crippling Strike**, **Cultural Expert**, **Danger Sense**, **Diligent Researcher**, **Disarming Blow**, and **Disguise Expert** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one compact type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **88** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** pending Wave 89.  
**Commit:** none.

### Suggested wave 90

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Wave 90 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **80** remaining. No commit created.

### Wave 89 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **88** remaining. No commit created.

---

## Wave 90 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Dispel Precision**, **Double Tap**, **Draw Cut**, **Dungeon Cartographer**, **Echo Spell**, **Efficient Caster**, **Empowered Summoning**, and **Energy Sink** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one compact type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **80** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** pending Wave 90.  
**Commit:** none.

### Suggested wave 91

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

---

## Wave 91 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Ether Anchor**, **Exploit Weakness**, **Field Medic**, **Field Surgeon**, **Flash Cast**, **Fleet of Foot**, **Forensic Investigator**, and **Foresight Surge** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one compact type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **72** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** pending Wave 91.  
**Commit:** none.

### Suggested wave 92

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Wave 91 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **72** remaining. No commit created.

---

## Wave 92 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Herbalist**, **Illusionist’s Trick**, **Inspiring Presence**, **Intuitive Reflex**, **Jack of All Trades**, **Librarian's Eye**, **Lingering Magic**, and **Lock Savant** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one compact type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **64** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** pending Wave 92.  
**Commit:** none.

### Suggested wave 93

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Wave 92 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~44s). The exact generic-placeholder scan reports **64** remaining. No commit created.

---

## Wave 93 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Lunge**, **Magical Fortitude**, **Mana Burn**, **Mental Buffer**, **Mental Fortress**, **Merchant’s Guile**, **Mirror Cast**, and **Mystic Focus** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **56** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** pending Wave 93.  
**Commit:** none.

### Suggested wave 94

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

---

## Wave 94 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Mystic Recoil**, **Natural Leader**, **Night Hunter**, **Overchannel**, **Overrun**, **Planar Knowledge**, **Polyglot**, and **Precise Shot** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **48** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

`npx tsc --noEmit` and `npm run build` passed (build ~42s).

### Suggested wave 95

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

---

## Wave 95 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Precision Throw**, **Protective Casting**, **Punishing Blow**, **Quick Learner**, **Quick Recovery**, **Quick Ritualist**, **Reckless Swing**, and **Resilient Mind** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **40** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

Pending Wave 95 typecheck and build.

### Suggested wave 96

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~42s). The exact generic-placeholder scan reports **40** remaining. No commit created.

---

## Wave 96 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Ritual Channeler**, **Rogue’s Escape**, **Runic Scholar**, **Runic Shield**, **Savage Momentum**, **Shattering Smash**, **Shield Bash**, and **Shield Expert** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** Pending validation; expected **32** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** Pending Wave 96 typecheck and build.  
**Commit:** none.

### Suggested wave 97

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add matching Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

---

## Wave 99 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Tenacity**, **Tinker Adept**, **Tough as Nails**, **Trap Sense**, **Twin Cast**, **Unshakeable**, **Unstoppable Force**, and **Versatile Artisan** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one compact type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** **8** canonical exact generic placeholder records remain; the raw literal match also sees the pre-existing duplicate `master_tracker` entry, which is excluded because the visible Master Tracker record was normalized in wave 98.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** Pending Wave 99 typecheck and build.  
**Commit:** none.

### Suggested wave 100

Finish the final eight canonical exact generic placeholders with the same bounded presentation-only draft pass, Builder provenance smoke, and rescan; preserve all source prerequisite/effect strings.

### Wave 99 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The canonical exact generic-placeholder scan reports **8** remaining; the raw literal search returns **9** because it includes the pre-existing duplicate `master_tracker` record. No commit created.

### Validation update

`npx tsc --noEmit` passed (~7s) and `npm run build` passed (~41s). The exact generic-placeholder scan reports **16** remaining. No commit created.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). The exact generic-placeholder scan reports **32** remaining. No commit created.

---

## Wave 97 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Silent Casting**, **Silent Movement**, **Silver Tongue**, **Skill feats1. Master Tracker**, **Spell Deflection**, **Spell Reservoir**, **Spell Scribe**, and **Spellweave** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** Pending validation; expected **24** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** Pending Wave 97 typecheck and build.  
**Commit:** none.

### Suggested wave 98

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add matching Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Validation update

`npx tsc --noEmit` passed. `npm run build` passed (build ~41s). The exact generic-placeholder scan reports **24** remaining. No commit created.

---

## Wave 98 — generic feat draft batch (2026-07-30)

**Shipped:**

- **Feat presentation:** **Steady Hands**, **Still Casting**, **Stubborn Resolve**, **Sure Shot**, **Tactical Flanker**, **Tactical Insight**, **Target Mark**, and **Temporal Flux** now replace their generic compendium placeholders with bounded, presentation-only draft copy and `draft: true`. The existing Builder feat-card branch shows each compact **Draft** badge.
- **Label correction:** The malformed Wave 97 display label **Skill feats1. Master Tracker** is now **Master Tracker**, matching the clear source title; no mechanics changed.
- **Smoke coverage:** `PLAYTEST_SMOKE.md` now supplies one type-filtered Builder pass covering all eight descriptions, badges, preserved prerequisite/effect strings, and the non-automated selection boundary.
- **Rescan:** Pending validation; expected **16** exact generic placeholder descriptions remain.

**Scope preserved:** No prerequisite, effect, selection behavior, or feat automation changed. No Oracle/Paladin/Umbrin author-tone review, totem automation, T6–T10 mapped content, deletion, or commit occurred.

**Validation:** Pending Wave 98 typecheck and build.  
**Commit:** none.

### Suggested wave 99

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add matching Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

---

## Wave 100 — final generic feat presentation pass (2026-07-30)

### Shipped

- **Final exact-placeholder batch:** **Versatile Grip**, **Volley**, **Weapon Finesse**, **Weapon Mastery**, **Whip Control**, **Whirlwind Striker**, **Wilderness Chef**, and **Wilderness Walker** now have bounded presentation-only draft descriptions and `draft: true`; the established Builder feat-card branch renders their compact **Draft** badges.
- **Duplicate investigation:** `master_tracker` and `skill_feats1_master_tracker` are a genuine duplicate pair: same visible name, prerequisite, and effect, with different IDs/types. `master_tracker` still contained a Skill compendium placeholder, so it received the same bounded draft presentation and badge. Both records remain untouched structurally for author review.
- **Provenance:** `PLAYTEST_SMOKE.md` adds the compact type-filtered Builder check for the final eight plus an explicit duplicate-record author check.

### Rescan and boundary

- **0** exact `General feat from the Decennium Descent compendium.` descriptions remain.
- No prerequisite, effect, selection behavior, type, or automation changed; no Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

### Suggested wave 101

Have the author resolve the Master Tracker canonical-record decision, then prioritize a bounded source-backed encounter, dungeon, or generator playtest lane rather than reopening author-tone prose.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **0** remaining. No commit created.

---

## Wave 101 — Session rest feedback (2026-07-30)

### Shipped

- **Rest-label correction:** The horn clock's time-only control now says **Advance +8h**, so it no longer implies a resource-restoring action. **Long rest (+8h)** remains the explicit recovery control.
- **Rest outcome feedback:** Short and Long Rest now leave a compact, accessible status line in the Party Resonance card. It reports the affected ally count and rest effects already performed by the tracker; it does not add new recovery rules or automate table-facing resolution.
- **Smoke:** `PLAYTEST_SMOKE.md` distinguishes time advance from a rest and verifies both outcome summaries.

### Morning ASK OWNER

- **Master Tracker duplicate:** `master_tracker` and `skill_feats1_master_tracker` remain intact pending an owner decision on the canonical record/type. Do not delete, merge, or retype either record based on this log.

### Boundary

No content tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

### Suggested wave 102

Run the new Session rest smoke manually, then take one bounded source-backed Encounter Library friction pass (selection-to-Session clarity or an actionable empty state) without inventing encounters. Keep the Master Tracker decision with the owner.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). No commit created.

---

## Wave 102 — Floor Encounter handoff choice + rest smoke stretch (2026-07-30)

### Shipped

- **Specific source-entry handoffs:** Floor Encounters now gives each existing Point of Interest a **Use as site in Session** action and each Safe Haven a **Use as fallback haven in Session** action. The tier-level action is renamed **Load tier brief in Session** and explains it sends the tier defaults.
- **Preserved handoff contract:** A POI choice changes only the `Site` line; a haven choice changes only `Fallback haven`. The existing tier/floor/gate-boss lines, draft-depth warning, Session navigation, and idempotent handoff bridge are unchanged.
- **Rest feedback smoke stretch:** `PLAYTEST_SMOKE.md` now confirms that **Advance +8h** does not emit rest feedback, while Short/Long Rest name affected allies and only Long Rest names the 8h horn advance.

### Boundary

No encounter content, content tables, T6–T10 mapped dungeon material, recovery rules, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

### Morning ASK OWNER

`master_tracker` and `skill_feats1_master_tracker` remain intact pending an owner decision on the canonical record/type. Do not delete, merge, or retype either record.

### Validation

Pending Wave 102 typecheck and build.

### Suggested wave 103

Browser-smoke one non-default POI handoff, one non-default haven handoff, and the rest-feedback distinction. If they pass, inspect one narrow Generator usability friction that can reuse current source outputs; do not add encounter tables or invented generator content.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~47s). No commit created.

---

## Wave 103 — Generator pack handoff guardrails (2026-07-30)

### Shipped

- **Source-output handoff:** Generators now enables **Load in Session** only after **Build pack** has produced the displayed pack. The handoff sends that exact output; it no longer creates an unseen fallback brief at click time.
- **Tier freshness:** Changing tiers clears the previously built pack and disables the handoff until the newly selected tier has its own pack, preventing mismatched tier metadata and scene text.
- **Recovery feedback:** Copying a spark reports success or gives a visible manual-copy recovery message if clipboard access is unavailable. Queuing a pack similarly reports its result.
- **Smoke:** `PLAYTEST_SMOKE.md` now covers pack-first enablement, tier-change clearing, Session staging, and clipboard feedback.

### Boundary

No generator/encounter tables or new content were added. No T6–T10 mapped dungeon work, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

### Validation

`npx tsc --noEmit` and `npm run build` passed (build ~47s). Browser smoke was not available in this environment; use the appended smoke rows against the running local app.

### Suggested wave 104

Run the Wave 102 selected-POI and selected-haven paths plus the Wave 103 Generator smoke in a browser. If they pass, take one similarly narrow existing-output Session handoff friction only; keep the Master Tracker canonical-record decision with the owner.

---

## Wave 104 — Bestiary selected-foe Session handoff (2026-07-30)

### Shipped

- **Bestiary detail → Session:** A selected monster now exposes **Add foe in Session**. It stages only the existing source stat block’s name, listed HP, CR, and zone, then opens Session.
- **Editable Session arrival:** Session adds exactly one foe using those source values and confirms it in a compact banner. Initiative, HP, and conditions remain editable through the existing Combatants controls; no monster behavior or encounter resolution was invented.
- **Smoke:** `PLAYTEST_SMOKE.md` appends a deterministic selected-foe path. Browser verification remains pending alongside the Wave 102 POI/haven and Wave 103 Generator paths because browser attachment is unavailable.

### Boundary

No Bestiary, loot, generator, or encounter content tables changed. No T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending the owner’s canonical-record decision.

### Validation

Pending Wave 104 typecheck and build.

### Suggested wave 105

Browser-smoke the Bestiary foe, selected POI/haven, and pack-first/tier-clear/clipboard paths. If they pass, take a narrow saved-character refresh/import discoverability pass in Session without changing character storage or inventing inventory/encounter automation.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). The existing non-fatal `SessionTracker` exhaustive-deps warnings remain; no commit created.

---

## Wave 105 — Session saved-character refresh discoverability (2026-07-30)

### Shipped

- **Session saved-list clarity:** The Add saved character card states that it reads browser-local saves and that adding a hero creates an encounter copy rather than a linked live character.
- **Return and recovery path:** Available heroes now expose class and level, the card shows its current count, and **Refresh saved list** provides an accessible count result. The empty state gives the concrete **CHARACTERS → SAVE → SESSION → Refresh saved list** path.
- **Import boundary:** The UI explicitly says Session has no separate JSON-import action; it does not imply unsupported import behavior or alter the character storage format.
- **Smoke:** `PLAYTEST_SMOKE.md` appends saved-list return, refresh-feedback, and import-boundary checks alongside the still-pending Bestiary and Generator handoff paths.

### Boundary

No saved-character storage semantics, payload fields, inventory automation, encounter resolution, content tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending the owner’s canonical-record decision.

### Validation

Pending Wave 105 typecheck and build.

### Suggested wave 106

Browser-smoke the saved-character refresh path together with the pending Bestiary foe, selected POI/haven, and Generator pack-first/tier-clear/clipboard paths. If those pass, take one small Session usability gap that uses existing data only; keep storage semantics and manual table-facing boundaries intact.

### Validation update

`npm run build` passed (~44s) with the two existing non-fatal `SessionTracker` exhaustive-deps warnings. `npx tsc --noEmit` then passed (~9s); its initial concurrent run raced Next’s `.next` generation and was rerun after the build. No commit created.

---

## Wave 106 — Spell cast-preview Session handoff (2026-07-30)

### Shipped

- **Spell reference handoff:** Spell Library cards now offer **Preview in Session**, staging the selected spell’s existing name, school, tier, casting time, range, and duration before opening Session.
- **Clear Session boundary:** An indigo arrival banner confirms the preview and directs players to choose a caster and use the existing spell lookup / Overcast controls. It neither spends RP nor resolves a cast.
- **Smoke:** `PLAYTEST_SMOKE.md` now covers arrival of the reference fields and confirms the handoff cannot add a combatant, alter saved data, or automate casting. Wave 105’s saved-list refresh path remains covered.

### Boundary

No Oracle RP behavior changed: Oracle remains Revelation Charges and its spell list remains reference-only. No character-storage schema, automated inventory, encounter resolution, source tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending the owner’s canonical-record decision.

### Validation

Pending Wave 106 typecheck and build.

### Suggested wave 107

Browser-smoke the saved-character refresh and spell-preview paths with the pending Bestiary, selected POI/haven, and Generator handoffs if attachment becomes available. Otherwise, take one narrow Session usability gap using existing sources only; preserve storage and table-facing resolution boundaries.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~54s). The two existing non-fatal `SessionTracker` exhaustive-deps warnings remain. No commit created.

---

## Wave 107 — Items reference-preview Session handoff (2026-07-30)

### Shipped

- **Item reference handoff:** Items Library details now offer **Preview in Session**, staging only the selected item’s existing name, rarity, tier, category, source type, and description.
- **Clear Session boundary:** A teal arrival banner displays that reference and directs the GM to resolve acquisition, crafting, use, and any inventory change manually. It does not write Scene notes, add inventory, alter resources, add a combatant, or change saved-character data.
- **Smoke:** `PLAYTEST_SMOKE.md` now covers dropped and crafted item preview arrival plus the explicit no-auto-inventory/manual-resolution boundary.

### Boundary

No item, loot, crafting, encounter, or dungeon source tables changed. No inventory or RP-spend automation, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. `master_tracker` and `skill_feats1_master_tracker` remain untouched pending the owner’s canonical-record decision.

### Validation

`npx tsc --noEmit` passed. `npm run build` pending.

### Suggested wave 108

Browser-smoke the Wave 107 item preview together with the pending saved-character, spell, Bestiary, selected POI/haven, and Generator paths if attachment becomes available. Otherwise, inspect the two existing non-fatal `SessionTracker` hook warnings and make only a dependency-safe, behavior-preserving correction.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). The existing two non-fatal `SessionTracker` exhaustive-deps warnings remain; no warning-reduction refactor was attempted. No commit created.

---

## Wave 108 — Session filter clarity + handoff-suite consolidation (2026-07-30)

### Shipped

- **Combatant filter clarity:** When the crowded-table filter or collapsed-foes behavior hides rows, the **Combatants** heading now reports the visible subset (for example, **3 of 7 shown**). Existing filter and **Show foes** controls, initiative ordering, and stored combatants remain unchanged.
- **Consolidated smoke:** `PLAYTEST_SMOKE.md` now gives the existing saved-character, spell, item, Bestiary, selected POI/haven, and Generator checks a single Session-handoff suite pass, retaining every handoff's individual manual-resolution boundary.

### Hook-warning assessment

`npx eslint src/components/SessionTracker.tsx` confirms the two warnings at the mount and `handoffTick` effects: both omit the locally recreated `applyPendingHandoffs` function. Adding it as a one-line dependency would rerun both effects after every render because the function identity changes, potentially reapplying pending handoffs. A safe correction requires a callback/refactor with dependency analysis, so it is intentionally deferred rather than suppressed or changed behaviorally.

### Boundary

No source tables, inventory automation, character-storage schema, RP/cast automation, encounter resolution, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

### Suggested wave 109

If browser attachment is available, execute the consolidated handoff suite. Otherwise, leave the hook warnings intact unless a focused callback/ref dependency design can prove mount and tick behavior remain one-consumption-only; take only another narrow existing-output Session/Builder friction after that.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). Production build repeats the same two intentional non-fatal `SessionTracker` exhaustive-deps warnings; no new lint warnings or type errors appeared. No commit created.

---

## Wave 109 — hidden active-turn recovery (2026-07-30)

### Shipped

- **Active-turn recovery:** When a Combatants filter or the crowded-foes collapse hides the current turn, the existing notice now has **Show active turn**. It selects the active combatant's side (Allies or Foes) and expands foes when needed, restoring the highlighted row in one action.
- **Smoke:** `PLAYTEST_SMOKE.md` adds filtered-ally and collapsed-foe paths, explicitly confirming visibility-only behavior.

### Boundary

No initiative ordering/value, turn/round state, combatant data, character-storage schema, inventory automation, RP/cast automation, encounter resolution, source tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 110

Browser-smoke the Wave 108 handoff suite and Wave 109 active-turn recovery when attachment is available. Otherwise, take one similarly narrow Session empty-state, handoff-dismissal, or initiative-chrome friction only if it preserves current table state and existing manual-resolution boundaries.

### Validation

Pending Wave 109 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). Production build repeats only the two intentional non-fatal `SessionTracker` exhaustive-deps warnings; no commit created.

---

## Wave 110 — Session notice dismissal + empty-table orientation (2026-07-30)

### Shipped

- **Arrival-notice cleanup:** When two or more existing Session handoff banners are open, a compact **Dismiss all notices** control clears the local banners together. Its visible boundary confirms this does not change Scene notes, combatants, tier, horn time, resources, or any other table state.
- **Empty-table orientation:** The no-combatants state now gives the existing three entry routes (saved character, Bestiary, Ally / Enemy) and explicitly confirms that current Scene notes, tier, horn time, and arrival notices are retained while the table is built.
- **Smoke:** `PLAYTEST_SMOKE.md` appends direct checks for stacked-notice dismissal and empty-table state preservation.

### Boundary

No handoff payload, scene notes, initiative ordering/value, turn/round state, combatant data, character-storage schema, inventory automation, RP/cast automation, encounter resolution, source tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 111

Browser-smoke Wave 109's active-turn recovery and Wave 110's state-preserving notice/empty-table paths when attachment is available. Otherwise, take one further narrow Builder or Session clarity friction only where it preserves current state and manual-resolution boundaries; do not reopen hook dependencies or author-review lanes.

### Validation

Pending Wave 110 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentional non-fatal `SessionTracker` exhaustive-deps warnings; no commit created.

---

## Wave 111 — Character Sheet printable draft-badge parity (2026-07-30)

### Shipped

- **Print provenance consistency:** Prestige hallmark and capstone draft badges now use the shared Sheet `DraftBadge`, matching the already printable draft markers elsewhere on the Character Sheet.
- **Smoke:** `PLAYTEST_SMOKE.md` appends an onscreen-to-print-preview check using existing prestige records; Wave 110’s state-preserving Session smoke rows remain intact and pending browser execution.

### Boundary

No prestige data, prerequisites, capstone behavior, character storage, Session state, inventory automation, RP/cast automation, encounter resolution, source tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 112

Browser-smoke Waves 109–111 when attachment is available: active-turn recovery, stacked-notice/empty-table preservation, and Sheet print-preview draft provenance. Otherwise, take only one additional narrow state-preserving Session or Builder clarity gap; do not reopen hooks or author-review lanes.

### Validation

Pending Wave 111 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 112 — Session notice-dismissal confirmation (2026-07-30)

### Shipped

- **State-preserving outcome feedback:** **Dismiss all notices** now leaves an accessible confirmation that names the number of local arrival banners closed and explicitly confirms that Scene notes, combatants, tier, horn time, turn, round, and resources are unchanged.
- **Fresh-arrival clarity:** A later source-backed Session arrival clears the stale dismissal confirmation, so the current banner is never visually contradicted.
- **Smoke:** `PLAYTEST_SMOKE.md` appends dismissal-confirmation and later-arrival-reset checks. Wave 109–111 browser rows remain available and non-blocking.

### Boundary

No handoff payload, Scene notes, combatants, initiative ordering/value, turn/round state, tier, horn time, resources, character storage, inventory automation, RP/cast automation, encounter resolution, source tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit changed. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 113

Browser-smoke Waves 109–112 when attachment is available. Otherwise, inspect one further narrow Session or Builder presentation gap that uses existing state only; preserve manual-resolution boundaries and do not reopen `SessionTracker` hook dependencies.

### Validation

Pending Wave 112 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 123 — Hero-path reference clarity + smoke (2026-07-30)

**Shipped:** Builder and printable Sheet now explain the existing absence of hero-path records instead of leaving the path area blank. Existing arch-path cards still render; the note neither creates a path nor treats its absence as a progression result. `PLAYTEST_SMOKE.md` appends this check and explicitly rechecks Wave 122’s pre-selection Cosmology **Draft extract** notice.

### Author review queue

- Decide the canonical Master Tracker record/type; retain both `master_tracker` and `skill_feats1_master_tracker` until then.
- Review Oracle, Paladin, and Umbrin tone; no overnight author-tone pass was performed.
- Confirm, revise, or defer the draft Resonance multiclass RP merge before canonization.
- Re-ingest the Drow → Umbrin source decision only after the tone/canon review.

**Boundary:** No path, class, progression, save, Cosmology, dungeon, inventory, Resonance, Session, or automation rule changed. No content tables, T6–T10 mapped material, author-tone review, deletion, or commit occurred.

**Suggested wave 124:** Browser-smoke the two focused Wave 123 rows when available; otherwise inspect one small existing-state Builder/Sheet blank-state only, leaving author review, Session hooks, inventory automation, and dungeon design closed.

**Validation update:** `npx tsc --noEmit` passed; `npm run build` passed in ~41s. Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 122 — Cosmology draft visibility (2026-07-30, append)

**Status:** Existing Cosmology draft batches now announce themselves before selection: World of Aethel and First Song show a **Draft extract** notice when draft sections are present, while the existing † picker signals and detailed section notes remain intact. `PLAYTEST_SMOKE.md` combines that check with Wave 121 feat-search recovery and Sheet People & traits paths.

**Coffee lane:** Browser-smoke the appended Wave 122 path if an attachment is available. Otherwise, take only one narrow existing-state Builder/Sheet clarity improvement. Keep author tone, T6–T10 design, inventory automation, and `SessionTracker` hook refactors out of scope.

**Validation:** `npx tsc --noEmit` passed; `npm run build` passed in ~42s with only the two intentionally deferred `SessionTracker` exhaustive-deps warnings. No commit created.

---

## Wave 121 final append — morning checklist and hero-state clarity (2026-07-30)

### ASK OWNER

1. Resolve the canonical Master Tracker record/type: `master_tracker` and `skill_feats1_master_tracker` remain intact; do not delete, merge, or retype either.
2. Approve or redirect the Oracle/Paladin/Umbrin author-tone review; no further presentation work is scheduled before it.
3. Confirm, revise, or defer the Resonance multiclass RP merge draft before canonization.

**Shipped:** Builder Feats adds a name search plus a clear no-match recovery; Sheet/print adds saved people, lineage, and existing sourced trait names, with explicit blank/unresolved state.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (~51s); only the two deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings remain. No commit created.

**Suggested wave 122:** Browser-smoke Wave 121 when available; otherwise take only a small existing-label Cosmology/Dungeon draft-marker consistency pass.

---

## Wave 121 — Morning checklist (2026-07-30)

### ASK OWNER before further canon or presentation work

1. **Master Tracker duplicate:** decide the canonical record/type for `master_tracker` and `skill_feats1_master_tracker`. Both remain intact; do not delete, merge, or retype either pending that decision.
2. **Oracle / Paladin / Umbrin tone:** approve or redirect the author-tone pass; overnight presentation work is closed pending that review.
3. **Resonance multiclass draft:** confirm, revise, or defer the current draft RP merge model before it becomes canon.

### Wave 121 shipped

- Builder Feats now names an empty existing type filter and directs the player back to available feat types.
- The printable Sheet now shows the saved people and its existing sourced trait names, or an explicit missing-record/source-summary state.

### Boundary

No feat, people, trait, class, Resonance, character-storage, Session, inventory/RP/cast automation, encounter, cosmology, or dungeon source rule changed. No content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

### Suggested wave 122

Run the small Wave 121 Builder → save → Sheet/print smoke when a browser is available. Otherwise, take one draft-marker consistency pass across existing Cosmology/Dungeon labels only; leave owner decisions, author tone, Session hooks, and automation closed.

### Validation

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 120 — Oracle Mystery and Curse recorded-state parity (2026-07-30)

### Shipped

- **Builder clarity:** Blank existing `oracleMystery` and `oracleCurse` state now says **No Oracle Mystery recorded** and **No Oracle's Curse recorded**, retaining the known L1 choice timing and unsaved-selection boundary.
- **Sheet / print parity:** The existing blank Oracle callouts now use the same wording while retaining their L1 requirement, **Draft** badges, and direction to Character Builder.
- **Smoke:** `PLAYTEST_SMOKE.md` appends blank-both and one-recorded-selection Builder → save → Sheet/print checks.

### Boundary

No Mystery or Curse source data, Oracle rule, revelation, boon, class feature, character-storage shape, progression, Session behavior, inventory/RP/cast automation, encounter resolution, content table, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit changed. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 121

Browser-smoke Waves 118–120 recorded-state rows when attachment is available. Otherwise, defer further Oracle presentation work until author review rather than extending this lane.

### Validation

Pending Wave 120 `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~49s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 119 — Sacred Oath recorded-state parity (2026-07-30)

### Shipped

- **Builder clarity:** A Paladin with blank existing `sacredOath` state now says **No Sacred Oath recorded**, retains the known L3 choice timing, and makes the unsaved-selection boundary explicit.
- **Sheet / print parity:** The existing blank-oath callout now uses the same wording while retaining the L3 requirement and its direction to Character Builder.
- **Smoke:** `PLAYTEST_SMOKE.md` appends deterministic L1 blank and L3 required Builder → save → Sheet/print checks.

### Boundary

No oath source data, oath rule, class feature, character-storage shape, progression, Session behavior, inventory/RP/cast automation, encounter resolution, content table, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit changed. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 120

Browser-smoke Wave 118 Ethos and Wave 119 Sacred Oath blank → save → Sheet/print paths when attachment is available. Otherwise, take only one narrow source-bounded Builder clarity gap using existing state, such as Oracle Mystery / Curse empty-state parity, without changing Oracle rules or author-tone content.

### Validation

Pending Wave 119 `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~55s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 118 — Ethos recorded-state parity (2026-07-30)

### Shipped

- **Builder clarity:** An unselected existing Ethos state now explains that it is not recorded, while accurately pointing to its existing save and spell-cost-preview role.
- **Sheet / print parity:** The printable identity badges explicitly render **Ethos not recorded** until a saved value exists, then render the existing selected ethos.
- **Smoke:** `PLAYTEST_SMOKE.md` adds blank and selected Builder → save → Sheet/print checks.

### Boundary

No ethos source table, spell-cost calculation, character-storage shape, class, feature, Resonance, Session behavior, inventory/RP/cast automation, encounter resolution, content table, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit changed. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 119

Browser-smoke Waves 116–118 when attachment is available. Otherwise, make one source-bounded Builder clarity improvement using only an existing saved state.

### Validation

Pending Wave 118 `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` passed. `npm run build` passed in ~42s; production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 117 — Sheet prestige-path intent parity (2026-07-30, final append)

**Delivered:** The saved selected-prestige panel on Character Sheet now states that it records path intent only and grants neither prerequisites nor features. Its existing requirements and **Draft** badges are unchanged; `PLAYTEST_SMOKE.md` appends Builder → Sheet → print coverage.

**Boundary:** No prestige source data, prerequisite, feature, class, Resonance, save rule, Session behavior, automation, encounter resolution, content table, T6–T10 mapped material, author-tone lane, deletion, or commit changed.

**Suggested wave 118:** Browser-smoke Wave 117 when attachment is available. Otherwise, make only one narrow, source-bounded Builder clarity improvement using existing saved state.

**Validation:** `npx tsc --noEmit` passed; `npm run build` passed in ~41s. The build reports only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 117 — Sheet prestige-path intent parity (2026-07-30)

### Shipped

- **Saved-intent boundary on Sheet:** When an existing selected prestige path is shown on the Character Sheet, its panel now explicitly says it is recorded intent only and grants neither prerequisites nor features.
- **Smoke:** `PLAYTEST_SMOKE.md` appends Builder → Sheet → print coverage for the same selected path, its existing requirements, and its existing draft badges.

### Boundary

No prestige source data, prerequisite, feature, class, Resonance, or character-storage rule changed. No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 118

Browser-smoke the Wave 117 Builder → Sheet → print path when attachment is available. Otherwise, take one narrow, source-bounded Builder clarity gap that uses existing saved state only; keep progression, automation, Session hooks, and author-review lanes closed.

### Validation

Pending Wave 117 `npx tsc --noEmit` and `npm run build`.

---

## Wave 116 — prestige-path intent clarity (2026-07-30)

### Shipped

- **Arch-path boundary:** Selecting a prestige path on **Class** now makes its intent-only status explicit: requirements and draft provenance remain on **Paths**, and selection does not grant prerequisites or features.
- **Smoke:** `PLAYTEST_SMOKE.md` adds a Class → Paths verification using only an existing prestige path and its current requirements/badges.

### Boundary

No prestige source data, prerequisite, feature, class, Resonance, or character-storage rule changed. No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 117

Browser-smoke Waves 114–116’s Builder → Sheet → print and prestige-path paths when attachment is available. Otherwise, take only one narrow, source-bounded Builder clarity gap using existing state.

### Validation

`npx tsc --noEmit` and `npm run build` passed (build ~49s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 117 — Sheet prestige-path intent parity (2026-07-30)

### Shipped

- **Saved-intent boundary on Sheet:** When an existing selected prestige path is shown on the Character Sheet, its panel now explicitly says it is recorded intent only and grants neither prerequisites nor features.
- **Smoke:** `PLAYTEST_SMOKE.md` appends Builder → Sheet → print coverage for the same selected path, its existing requirements, and its existing draft badges.

### Boundary

No prestige source data, prerequisite, feature, class, Resonance, or character-storage rule changed. No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 118

Browser-smoke the Wave 117 Builder → Sheet → print path when attachment is available. Otherwise, take one narrow, source-bounded Builder clarity gap that uses existing saved state only; keep progression, automation, Session hooks, and author-review lanes closed.

### Validation

Pending Wave 117 `npx tsc --noEmit` and `npm run build`.

---

## Wave 115 — printable Sheet multiclass + feature provenance (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **RP merge print block** | Existing draft **Multiclass Resonance merge** lines stay together and print with their provenance badge. |
| **No-pool secondary print boundary** | A selected secondary class without a second eligible Weave pool now retains Builder’s existing clarity on the Character Sheet and in print. |
| **Level-feature print legend** | Draft-milestone summary and per-feature **Draft** badges now use explicit print-safe text, border, and background styling. |
| **Smoke** | `PLAYTEST_SMOKE.md` appends the three focused print-preview paths. |

### Scope boundary

- No class, feature, multiclass, Resonance, or character-storage source rule changed.
- No Session state, inventory/RP/cast automation, encounter resolution, content table, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two deferred `SessionTracker` `applyPendingHandoffs` warnings remain unchanged.

### Suggested wave 116

Browser-smoke Wave 114–115’s Builder → Sheet → print paths when available. If browser remains unavailable, take only one narrow, confirmed Builder clarity gap from the handoff using existing state; do not reopen Session hooks or author-review work.

### Validation

Pending Wave 115 typecheck and production build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 114 — Builder secondary-class clarity + printable feat provenance (2026-07-30)

### Shipped

- **Secondary-class clarity:** The Builder now explains when a selected secondary class is retained without contributing a second eligible Weave pool. Existing eligible pairs still use the existing **Multiclass RP merge** draft panel and its detailed calculation.
- **Draft-feat continuity:** Selected draft feats now retain their compact **Draft** marker in Builder’s Chosen feats summary and on the Character Sheet, including print preview.
- **Smoke:** `PLAYTEST_SMOKE.md` appends source-bounded selection, merge-panel, and Sheet print-preview checks.

### Boundary

No feat, class, Resonance, or source-table rules changed. No character-storage schema, Session behavior, inventory automation, RP/cast automation, encounter resolution, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 115

Browser-smoke the Wave 114 Builder/Sheet checks plus the pending Wave 109–113 Session rows when attachment is available. Otherwise, inspect one narrow remaining Character Sheet print or presentation gap that only consumes existing saved state; leave Session filter recovery and hook dependencies alone.

### Validation

Pending Wave 114 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~42s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 113 — Session filtered-table recovery (2026-07-30)

### Shipped

- **Empty filtered-view recovery:** When the existing Allies/Foes filter leaves a non-empty table with no visible rows, Session now explains that no combatants match the current view and offers **Show all combatants**.
- **State-preserving return:** Recovery changes only the existing display filter and expands the existing foes view; combatants, initiative, turn/round, scene notes, tier, horn time, resources, and handoff state remain untouched.
- **Smoke:** `PLAYTEST_SMOKE.md` appends deterministic empty-Foes-view and state-preservation checks. Browser execution remains non-blocking.

### Boundary

No handoff payload, combatant data, initiative ordering/value, turn/round state, Scene notes, tier, horn time, resources, character storage, inventory automation, RP/cast automation, encounter resolution, source tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit changed. The existing `SessionTracker` hook warnings remain intentionally deferred.

### Suggested wave 114

Browser-smoke Waves 109–113 when attachment is available. Otherwise, take only another confirmed narrow presentation gap using current state; preserve manual-resolution boundaries and do not reopen `SessionTracker` hook dependencies.

### Validation

Pending Wave 113 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Umbrin migration authorized (2026-07-30)

**Shipped:** The living rulebook extract (`rulebook_output.txt`) now replaces the 38 legacy Drow-era references in its Peoples, traits, variants, ability-summary, and language material with **Umbrin**. The race chapter now uses **Murkish**, **Umbrin Magic**, and **Obsidian Highborn**; it removes legacy external naming and adds an explicit author-review note for the Calan'thir / First Choir **Obsidian Burn** account.

**Companion consistency:** No active companion data still uses Drow-era product copy. Legacy save aliases remain intentionally in `src/lib/character-storage.js` so existing characters migrate to Umbrin.

**Author review remaining:** Approve or revise the Obsidian Burn motive/theology; supply Umbrin naming examples; review Murk cult terminology; decide whether to promote any Oracle mystery or Paladin oath beyond its current `draft: true` status.

**Suggested next rulebook wave:** Review the Umbrin chapter line-by-line against the full source document, then promote one bounded Oracle mystery or Paladin oath only after its rules text is reconciled with the existing `draft: true` data.

---

## Rulebook wave — Oath of Grief tone pass (2026-07-30)

**Shipped:** The draft **Oath of Grief** in `src/data/paladin-oaths.js` now has bounded rulebook-tone prose for remembrance, mourning, and the duty of passage. The pass changes no rules text, numbers, revelation list, or eligibility, and it deliberately retains `draft: true`.

**Source boundary:** `rulebook_output.txt` is the editable living extract. The full `decennium descent player rulebook.docx` exists but was not edited in this wave, so its Umbrin Peoples material still needs a controlled synchronization after author approval.

**Author review remaining:** Oath of Grief mechanics/revelation wording; Obsidian Burn motive and theology; Umbrin names; Murk-cult terminology; and docx synchronization of approved Peoples prose.

**Suggested next rulebook wave:** Reconcile the docx against the living extract, then take a second bounded Oracle mystery or Paladin oath tone pass while preserving its draft status.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — controlled docx sync assessment + Oath of the Chain (2026-07-30)

**Docx status: deferred safely.** The full `decennium descent player rulebook.docx` is present and `python-docx` is installed, but the available document tooling cannot inspect and apply a paragraph-scoped binary change with a reviewable backup through the normal safe edit path. No docx bytes were written, so the original document is intact. `rulebook_output.txt` remains the living Umbrin source; this is an extract-only handoff, not a claim that the docx is synchronized.

**Delivered:** The draft **Oath of the Chain** in `src/data/paladin-oaths.js` now presents its existing protective vows in rulebook voice: a vigil freely borne, wards kept when danger closes, and sacrifice that does not demand another's suffering. Its smite, aura, signature power, revelations, oathbreaker record, final gift, numbers, and `draft: true` status are unchanged.

**Author review remaining:** Confirm the approved Umbrin Peoples wording for the docx sync; then use a paragraph-aware Office or `python-docx` workflow with a backup and post-save extraction comparison. Review Oath of the Chain for promotion separately from its retained draft status.

**Suggested next rulebook wave:** Make the docx sync its own guarded task: back up the document, replace only the verified Peoples paragraphs, export a fresh text extract, and diff the Umbrin chapter against `rulebook_output.txt` before accepting the save.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — guarded Umbrin docx sync (2026-07-30)

**Delivered:** `decennium descent player rulebook.docx` has been synchronized to the living Umbrin extract through targeted People/rulebook paragraph replacements. The beside-source backup is `decennium descent player rulebook.pre-umbrin-backup.docx`. The docx now uses **Umbrin**, **The Murk**, **Murkish**, **Umbrin Magic**, and **Obsidian Highborn**, including the extract's non-mechanical Obsidian Burn author-review note.

**Verification:** The saved document reopened successfully. A fresh full-document scan finds no whole-word Drow reference; “drowsy” is intentionally unchanged. No application code, mechanics, draft status, deletion beyond the three obsolete external-name-list paragraphs, or commit occurred.

**Next:** Keep Obsidian Burn and Umbrin naming examples in author review. If a further tone pass is chosen, limit it to one Oracle mystery and preserve `draft: true`.

---

## Rulebook wave — Cataclysm Oracle mystery tone pass (2026-07-30)

**Delivered:** The draft **Cataclysm** mystery in `src/data/oracle-mysteries.js` received one bounded prose pass. Its theme, combat role, reputation, and existing **The Unbound Wound** capstone now carry concise rulebook voice about breaking an untenable position to clear a perilous path.

**Mechanics and provenance:** No charge cost, range, area, duration, damage, immunity, Exhaustion, patron, or other Revelation text was changed. Cataclysm remains `draft: true` through the shared draft helper; this is not a canon promotion.

**Author review remaining:** Review Cataclysm's full draft tree before any promotion. Obsidian Burn theology and Umbrin naming examples remain author-only decisions; this pass adds neither.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`; no commit or deletion occurred.

---

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

**Cataclysm spot-check update:** The `rulebook_output.txt` Oracle extract confirms Cataclysm's source theme (destruction, upheaval, instability), area-damage/battlefield-control role, and feared/suspect reputation. It supplies no non-Ancestor Mystery tree, so the Cataclysm draft tree remains unpromoted; no contradiction found.

**Suggested next:** After author review, reconcile one complete Oracle mystery tree against the rulebook before considering a `draft` promotion; otherwise keep further content work to similarly bounded, source-safe prose.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Oath of Chains Broken tone pass (2026-07-30)

**Delivered:** The draft **Oath of Chains Broken** in `src/data/paladin-oaths.js` now carries a bounded rulebook-voice pass in its theme and existing conduct clauses: liberation is a continuing duty to protect the freed without becoming a new tyrant.

**Mechanics and provenance:** Smite, aura, signature power, revelation spells, oathbreaker text, final gift, numbers, and selection timing are unchanged. The Oath remains `draft: true`; this is not a canon promotion.

**Cataclysm spot-check:** Pending a direct check against the workspace's `rulebook_output.txt`; no rulebook claim was inferred or force-promoted.

**Author review remaining:** **14** untouched `draft: true` Oracle Mystery / Sacred Oath profiles remain after Cataclysm, Oath of Grief, Oath of the Chain, and this pass. Continue with the Oath of Silence or a single Mystery profile after author review; Obsidian Burn theology and Umbrin names remain author-only decisions.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`; no commit or deletion occurred.

---

## Rulebook wave — Oath of Silence + Dream mystery tone pass (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Oath of Silence:** The draft oath in `src/data/paladin-oaths.js` now speaks in bounded rulebook voice about humility, restraint, and judging only after hearing the full matter. Its mechanics, revelation spells, oathbreaker text, final gift, values, and explicit `draft: true` status are unchanged.
- **Dream mystery:** The draft Dream profile in `src/data/oracle-mysteries.js` received a thin presentation pass for its theme, combat role, and reputation. Revelation mechanics, patron, charges, ranges, durations, and shared `draft: true` provenance are unchanged.

### Boundary

No Obsidian Burn theology, Umbrin name list, class mechanics, promotion, deletion, or commit was added. Both profiles remain author-review drafts.

### Handoff

**12** untouched draft Mystery/Oath profiles remain from the prior 14-profile queue. Suggested next bounded pass: **Oath of the Martyr King**; alternatively, take one remaining Mystery profile while retaining its draft status.

### Validation

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Morning owner-ruling handoff — 2026-07-30

**Locked and shipped:** The Umbrin geography and tone now flow **Obsidian Burn → The Murk → Blackglass Reach → Veyr-Obsid → the Quiet Deep**. Name examples and transactional-allegiance language are canon in `UMBRIN_LORE.md`.

**Rules:** `master_tracker` is canonical; the clone is hidden from new Builder selections but retained deprecated for save history. Hybrid-B multiclass Resonance is approved, while unrelated non-core pool tables remain draft. **Mystery of Shadow** and **Oath of Grief** are promoted; all other Mystery/Oath/Curse drafts, including the Spiral-Touched benchmark, remain untouched.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~74s). The build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Continuity stamp — locked Umbrin geography (2026-07-30)

**Locked canon:** The Murk remains the Umbrin region and approach; Blackglass Reach is its surface/near-Murk marches; Veyr-Obsid is the primary Umbrin city; and the Quiet Deep is the deeper underworld. Obsidian Burn theology remains canon.

**Posture:** The world broadly distrusts Umbrin for betrayal and cult association. Alliances are tentative, transactional, and self-serving—not redemption by default.

**Boundary:** No personal-name list was invented; no mystery, oath, or curse was promoted; Master Tracker and Resonance remain unresolved. Rulebook extract and docx were synchronized; a pre-geography docx backup was created. No companion data changed, so no typecheck was required; no commit or deletion occurred.

---

## Midnight coffee-prep decision pack (2026-07-30)

**Delivered:** [`AUTHOR_REVIEW_QUEUE.md`](./AUTHOR_REVIEW_QUEUE.md) is the concise owner decision surface for the provisional Obsidian Burn theology, owner-supplied Umbrin naming examples, the two Master Tracker records, Resonance multiclass, and draft-to-approved candidates.

**Continuity:** Mystery/Oath profile tone queues and all nine draft Oracle curse profile passes are complete; every associated `draft: true` marker remains unchanged. Spiral-Touched remains rulebook-complete. The pack records both Master Tracker records without deletion: `master_tracker` (`Skill`) and `skill_feats1_master_tracker` (`General`).

**Morning suggestion (~06:00):** Keep work light until the author is awake. Record the four owner rulings in the pack first, then choose a small explicit promotion batch. No code changed in this append, so no build was run.

---

## Rulebook wave — Oracle curse tone pass + coffee refresh (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Nine draft curse profiles:** `src/data/oracle-curses.js` now gives **Wound Eater**, **Soul-Cracked**, **Haunted**, **Tongues**, **Burning Blood**, **False Life**, **Shattered Mind**, **Consumed**, and **Fate-Bound** bounded rulebook voice in their profile blurbs and limitations.
- **Rules preserved:** Curse names, IDs, limitation effects, boon unlocks, boon text, values, costs, ranges, durations, damage, and progression are unchanged. All nine profiles remain explicitly `draft: true`.
- **Author boundary:** No Obsidian Burn theology, Umbrin names, promotion, deletion, or commit was added.

### Coffee checklist — author handoff

1. Supply the unresolved **Obsidian Burn** motive/theology; do not infer it from draft text.
2. Supply approved **Umbrin naming examples**; do not generate a replacement list.
3. Reconcile the **Master Tracker duplicate** before treating either copy as authoritative.
4. Review and approve or revise the **Resonance multiclass** draft formula before canonizing it.
5. After a profile-by-profile rules and prose review, promote only individually approved `draft` content.

### Continuity and handoff

The Oracle curse tone-pass queue is **0 remaining**: all **9** draft curse profiles received this presentation-only pass. **Spiral-Touched** remains the sole rulebook-complete curse tree; none of the nine drafts were promoted.

**Next suggestion:** Resolve the five coffee-checklist author decisions, then conduct a focused approval review beginning with the complete draft curse trees before any `draft → approved` promotion.

### Validation

Pending `npx tsc --noEmit` and `npm run build`; no commit created.

### Validation update

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Life + Stars Oracle mystery tone pass (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Life mystery:** The draft Life profile in `src/data/oracle-mysteries.js` now uses bounded rulebook voice for restoration that holds through a hard fight, protective shelter, and the courage required to preserve life.
- **Stars mystery:** The draft Stars profile now frames foresight as difficult but usable clarity: finding an opening, guiding an ally, and naming the path a party may not want to ignore.
- **Rules preserved:** Revelation trees, patron text, costs, ranges, durations, damage, numbers, and all progression fields are unchanged. Both mysteries retain `draft: true` through the shared draft helper.

### Boundary

No Obsidian Burn theology, Umbrin name, mechanic, promotion, deletion, or commit was added. Both profiles remain author-review drafts.

### Handoff

The prior queue reported **8** untouched profiles; the source/profile audit after this pass identifies **7** without a recorded tone pass: Oracle **Battle**, **Bones**, **Shadow**, and **Time**; Paladin **Oath of Dominion**, **Oath of Flame**, and **Oath of the Ancients**. Reconcile the one-profile count discrepancy before treating the queue as complete.

**Suggested next:** Take **Shadow** or **Time** as the next thinnest Oracle profile, retaining `draft: true`; then author-review each completed full tree before any promotion.

### Validation

Pending `npx tsc --noEmit` and `npm run build`; no commit created.

### Validation update

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Oath of the Martyr King + Flame mystery tone pass (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Oath of the Martyr King:** The draft oath in `src/data/paladin-oaths.js` now speaks in bounded rulebook voice about stewardship, freely borne responsibility, and refusing to demand a burden the oathkeeper will not take. All mechanics, revelations, oathbreaker text, final gift, values, and explicit `draft: true` status are unchanged.
- **Flame mystery:** The draft Flame profile in `src/data/oracle-mysteries.js` received a thin presentation pass for theme, combat role, and reputation. Its patron, complete Revelation tree, costs, ranges, durations, damage, and shared `draft: true` provenance are unchanged.

### Boundary

No Obsidian Burn theology, Umbrin name list, class mechanics, promotion, deletion, or commit was added. Both profiles remain author-review drafts.

### Handoff

**10** untouched draft Mystery/Oath profiles remain. Suggested next bounded pass: **Oath of Mercy** or **Oath of Vengeance**; retain `draft: true` and review each completed profile before any promotion.

### Validation

Pending `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Oath of Mercy + Oath of Vengeance tone pass (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Oath of Mercy:** The profile in `src/data/paladin-oaths.js` now uses bounded rulebook voice for shelter, healing, and the duty to spare life where the oath can still protect it. Its existing conduct clauses received presentation-only expansion, and the profile is explicitly retained as `draft: true`.
- **Oath of Vengeance:** The draft oath now frames its existing conduct around disciplined pursuit, sworn judgment, and honoring genuine surrender without abandoning allies.
- **Rules preserved:** Smite, aura, signature power, revelation spells, oathbreaker material, final gift, numeric values, and selection timing are unchanged for both Oaths.

### Boundary

No Obsidian Burn theology, Umbrin names, mechanic, promotion, deletion, or commit was added. Both Oaths remain author-review drafts.

### Handoff

**8** untouched `draft: true` Oracle Mystery / Sacred Oath profiles remain. Suggested next bounded pass: select the thinnest remaining Oracle Mystery, retain `draft: true`, and review every completed tree before promotion.

### Validation

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Shadow + Time Oracle mystery tone pass (2026-07-30)

**Delivered:** Draft **Shadow** received a bounded profile pass for disciplined silence, concealment, and fear used with purpose. Draft **Time** received the same treatment for measured delay, costly reversal, and the narrow opening a party can use before a fight turns.

**Rules preserved:** Only theme, combat role, and reputation changed for each profile. Both retain `draft: true` through `draftMysteryRevelations`; their patrons, full Revelation trees, costs, ranges, durations, damage, values, and progression remain unchanged.

**Queue reconciled:** The verified seven-profile queue is reduced by these two passes to **5**: **Battle**, **Bones**, **Oath of Dominion**, **Oath of Flame**, and **Oath of the Ancients**.

**Next:** Take **Bones** as the final remaining Oracle profile; preserve `draft: true`, do not invent Obsidian Burn theology or Umbrin names, and review completed trees before promotion.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit or deletion occurred.

---

## Rulebook wave — final five-profile tone pass (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Oracle — Battle + Bones:** `src/data/oracle-mysteries.js` now gives both draft profiles bounded rulebook voice. Battle centers the responsibility of command under fire; Bones centers care for the dead and the limits of borrowed power.
- **Paladin — Dominion, Flame + Ancients:** `src/data/paladin-oaths.js` now presents their existing themes and conduct clauses as accountable authority, restrained cleansing, and humble guardianship of old covenants.
- **Rules preserved:** Battle/Bones changed only theme, combat role, and reputation. The Oaths changed only theme, conduct clauses, and source provenance wording. Every Revelation tree, oath mechanical field, value, duration, range, cost, progression field, and selection rule is unchanged.
- **Draft preserved:** Both Mysteries retain shared `draft: true`; all three Oaths retain explicit `draft: true`. No profile was promoted.

### Continuity and handoff

The reconciled remaining tone-pass queue is **0**. No Obsidian Burn theology or Umbrin names were authored.

**Next suggestion:** Hold for author resolution of Umbrin lore blockers, then take the separate curse-tone pass. Before any new overnight prose wave, run the coffee checklist: confirm draft labeling, author-only lore boundaries, and unchanged mechanical fields.

### Validation

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.