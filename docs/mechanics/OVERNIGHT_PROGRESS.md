# Overnight Progress — Decennium Descent (2026-07-29)

**Workspace:** `DecenniumDescent-main`  
**Protocol:** No commits; no mass deletion. Draft-flagged Aethel content only where canon gaps exist.

---

### Wave 75 validation update

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~46s)
```

### Wave 75 validation update

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~46s)
```

## Chargen / content gaps (overnight worker)

### 1. Race rename — Drow → **Umbrin** *(Umbral Elf was interim)*

**Status:** Landed (overnight AM pass + late 2026-07-29 PM Umbrin rename). **Umbral Elf** was an interim label; **Umbrin** is current per Director/owner direction.

| Surface | Change |
|---------|--------|
| `races.js` | `umbrin` id, **Umbrin** display name, Umbrin Magic / Umbrin Weapon Training traits, Murkish language |
| `builder-races.js` | People picker shows **Umbrin** |
| `racial-variants.json` | Subraces parent **Umbrin**; **Obsidian Highborn** noble line |
| `feats.js` | Nightfang Training → Umbrin heritage prereq |
| `character-storage.js` | Legacy `Drow` / `Umbral Elf` / `Noble Umbral Elf` → Umbrin / Obsidian Highborn on load |
| `bestiary_data_full.json` | 10 Umbral Elf* creature names → **Umbrin *** |
| `CONTINUITY_GLOSSARY.md` | Umbrin row; Umbral Elf noted as legacy alias |
| `docs/mechanics/UMBRIN_LORE.md` | Draft lore stub (Obsidian Burn, Calan'thir exile, perverse Umbra) |

Builder warnings and Character Sheet resolve race via saved `race` string + migration — no remaining product-path **Drow** or **Umbral Elf** labels in chargen data.

### 2. Draft quality polish

| Area | Work |
|------|------|
| **Paladin Sacred Oaths** | All 9 draft oaths retain full L3/L5/L9/L13/L17 **revelation spell** lists; `source` strings now reference CONTINUITY_GLOSSARY Sacred Oath / Revelation spells distinction. Mercy remains rulebook canon (no `draft` flag). |
| **Oracle mysteries** | Patron names normalized to glossary form (Echo Court, War Chorus, Hush Beneath the Song, etc.) — removed inconsistent leading "The". Trees unchanged; `draft: true` on nine mysteries. |
| **Mage L2** | `class-details.js` L2 now notes **Arcane Tradition / school focus** plus Spellbook prepare +1 spell per long rest. |

### 3. Prestige feat drafts

| Check | Result |
|-------|--------|
| `tools/find_missing_prestige_feats.py` | **0 missing** (53 prestige feat refs ↔ 336 defined feats) |
| Empty `effect` fields | None found among prestige draft stubs |
| Draft prestige feats | 53 entries with Aethel-toned descriptions + mechanical effects (`draft: true`) |

### 4. L11–20 class coverage (`class-draft-levels.js`)

All **17 canon classes** now have L11–20 representation (canon in `class-details.js` and/or draft milestones):

| Class | L11–20 source |
|-------|----------------|
| Bard, Cleric, Crimson Agent, Mage, Mirrorsage, Ranger, Shaman, Soldier, Tinker, Dragoon, Monk, Warrior, Thief | Existing draft milestones |
| **Druid** | Rulebook canon in `class-details.js` (L11–20 complete) |
| **Oracle** | Canon L12/15/18/20 + **new draft** L11, 13, 14, 16, 17, 19 |
| **Paladin** | Canon L11/13/15/17/18/20 + **new draft** L12, 14, 16, 19 |
| **Wizard** | Canon L11/13/15/17/20 + **new draft** L12, 14, 16, 18, 19 |

Draft entries use `draft: true` via `class-level-utils.js` and show "(draft)" in Features UI.

### 5. Typecheck

```bash
npx tsc --noEmit
```

**Exit 0** — no TypeScript errors after chargen edits.

---

## Files touched (this worker)

- `src/data/class-draft-levels.js` — Oracle, Paladin, Wizard L11–20 gap fill
- `src/data/oracle-mysteries.js` — patron name glossary alignment
- `src/data/class-details.js` — Mage L2 progression note
- `src/data/CONTINUITY_GLOSSARY.md` — remove stale race-rename pending row
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this file

## Still author-side (not blocking playtest)

- Rulebook docx still says "Drow" — re-ingest ticket when owner updates source files
- Paladin oaths 9/10 and Oracle mysteries 9/10 remain `draft: true` pending author promotion
- L11–20 draft milestones need rulebook table cross-check before canon promotion

---

## Wave 2 — mechanics polish (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Director authority for draft text.

### 1. Umbrin race scrub (`src/`)

**Status:** Verified clean. Product-path data (`races.js`, `builder-races.js`, `racial-variants.json`, `feats.js`, `bestiary_data_full.json`) uses **Umbrin** only. Legacy `Drow` / `Umbral Elf` strings remain **only** in `character-storage.js` migration maps (intentional). `CONTINUITY_GLOSSARY.md` / `CONTINUITY_REPORT.md` document the rename — not player-facing.

**TODO (author-side):** `rulebook_output.txt` still contains Drow/D&D ingest names — re-ingest when owner updates source docx; do not bulk-edit rulebook txt in companion.

### 2. Reputation — Umbrin strange alliances

| Surface | Change |
|---------|--------|
| `REPUTATION.md` | Already documented (Umbrin note § Factions) — no edit |
| `ReputationPanel.tsx` | Footer updated: Resonance modifiers wired; one-line Umbrin strange-alliance note in full editor mode |

### 3. Multiclass RP formula (`RESONANCE_CANON.md` §7)

Expanded Director default: **highest Weave caster pool + 25% of secondary caster max** (round up). Example stub added. Flagged not implemented — `defaultMaxRp()` still single-class.

### 4. Burnout session stub

| Surface | Change |
|---------|--------|
| `resonance-economy.js` | `BURNOUT_EFFECT_STUB` export (disadvantage on Weave checks; −1 action this turn) |
| `SessionTracker.tsx` | When `burnoutRisk` set: badge tooltip + draft effect line under RP row |

### 5. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 2 edits.

---

## Files touched (wave 2)

- `docs/mechanics/RESONANCE_CANON.md` — §7 multiclass draft formula; shipped/draft list updates
- `src/data/resonance-economy.js` — `BURNOUT_EFFECT_STUB`
- `src/components/ReputationPanel.tsx` — wired RP footer + Umbrin alliance note
- `src/components/SessionTracker.tsx` — Burnout draft effect stub UI
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 2 section

---

## Wave 3 — collaborator-ready content (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. P0/P1 vague queue empty.

### 1. Multiclass Builder UI

| Surface | Change |
|---------|--------|
| `CharacterBuilder.tsx` | Optional **Secondary class** + **Secondary level** dropdowns (17 canon classes); RP max uses `resolveMaxRp` with multiclass opts |
| `character-storage.js` | Persists `secondaryClass` / `secondaryLevel` on normalize |
| `CHARGEN_PROGRESSION.md` | Multiclass table + manual JSON examples |
| `RESONANCE_CANON.md` | Shipped list updated — Builder UI live |

### 2. Generators — Umbrin / Drow scrub

| Surface | Change |
|---------|--------|
| `GeneratorsPanel.tsx` | **People spark** generator from `builder-races.js` (includes **Umbrin**); explicit Drow filter on race pool |

Product-path `src/` has no player-facing Drow except intentional legacy migration in `character-storage.js`.

### 3. Cosmology viewer — key terms

| Surface | Change |
|---------|--------|
| `CosmologyViewer.tsx` | **Key terms** panel: Calan'thir, First Choir, Umbra, Lumina, Umbrin |

### 4. Collaborator Day 1 doc

| Surface | Change |
|---------|--------|
| `docs/mechanics/COLLABORATOR_DAY1.md` | First-day read list, smoke path, Umbrin lore + Resonance canon touchstones |

### 5. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 3 edits.

---

## Files touched (wave 3)

- `src/components/CharacterBuilder.tsx` — multiclass dropdowns + RP display
- `src/lib/character-storage.js` — secondary class fields
- `src/components/GeneratorsPanel.tsx` — People spark (Umbrin in pool)
- `src/components/CosmologyViewer.tsx` — glossary terms panel
- `docs/mechanics/CHARGEN_PROGRESSION.md` — multiclass section
- `docs/mechanics/COLLABORATOR_DAY1.md` — new
- `docs/mechanics/RESONANCE_CANON.md` — Builder UI note
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 3 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 3 summary

---

## Wave 4 — author-draft consistency (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Draft-flagged Aethel content only.

### 1. Oracle mystery spot-check (vs Ancestor template)

| Mystery | Result |
|---------|--------|
| **Battle** | Tier I/II/III charge costs 1/2/3; `finalRevelation` (Avatar of the War Chorus) present — no edits |
| **Time** | Tier I/II/III charge costs 1/2/3; `finalRevelation` (The Spiral Opens) present — no edits |
| **Shadow** | Tier I/II/III charge costs 1/2/3; `finalRevelation` (Marquis's Glimpse) present — no edits |
| **Ancestor (canon ref)** | Fixed **Ghost Chant** Tier II cost 1→2 charges; **Spirit Walk** description now prefixes "Spend 2 charges" |

### 2. Paladin oath spot-check (vs Mercy template)

| Oath | Result |
|------|--------|
| **Vengeance** | L3/L5/L9/L13/L17 revelation spells + oathbreaker complete — added draft **Final Oath Gift (L20): Verdict Absolute** |
| **Flame** | L3/L5/L9/L13/L17 revelation spells + oathbreaker complete — added draft **Final Oath Gift (L20): Purifying Crown** |

`finalOathGift` optional field added to `SacredOath` typedef (Mercy remains without per-oath L20 text until rulebook supplies it).

### 3. Character Sheet — multiclass display

| Surface | Change |
|---------|--------|
| `CharacterSheet.tsx` | Header shows `Primary L# + Secondary L#` when `secondaryClass` set; oath block shows level-gated revelation spells, L11 signature, and L20 `finalOathGift` when present |

### 4. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 4 edits.

---

## Files touched (wave 4)

- `src/data/oracle-mysteries.js` — Ancestor Tier II charge consistency
- `src/data/paladin-oaths.js` — `finalOathGift` field + Vengeance/Flame L20 drafts
- `src/components/CharacterSheet.tsx` — secondary class + oath progression display
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 4 section

---

## Wave 5 — Paladin L20 completion + oracle spot-check + session multiclass (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Continuity green; Umbrin locked; Resonance named Resonance.

### 1. Paladin L20 `finalOathGift` drafts

| Oath | Result |
|------|--------|
| **Mercy** | Canon oath untouched; added draft **Grace Eternal** with `finalOathGiftDraft: true` |
| **Dominion** | Draft **Sovereign's Ascendance** |
| **Ancients** | Draft **Primordial Crown** |
| **Silence** | Draft **Vow Absolute** |
| **Chain** | Draft **Unbroken Covenant** |
| **Grief** | Draft **Dirge of Passage** |
| **Chains Broken** | Draft **Liberty Unbound** |
| **Martyr King** | Draft **Crown Undying** |
| **Vengeance / Flame** | Already shipped wave 4 — no edits |

`finalOathGiftDraft` optional field added to `SacredOath` typedef; Character Sheet shows `(draft)` on L20 gift when set.

### 2. Oracle mystery spot-check (remaining draft mysteries + Ancestor)

| Mystery | Result |
|---------|--------|
| **Battle / Time / Shadow** | Tier I/II/III 1/2/3 charges; `finalRevelation` present — no edits (wave 4 baseline) |
| **Bones / Cataclysm / Dream / Flame / Life / Stars** | Tier I/II/III charge costs 1/2/3; descriptions match — no edits |
| **Ancestor (canon ref)** | Fixed **Bloodline Convergence** tier III description — added missing **Spend 3 charges** prefix |

### 3. Session — multiclass on combatant row

| Surface | Change |
|---------|--------|
| `SessionTracker.tsx` | Multiclass badge (`Primary L# + Secondary L#`) on combatant row when `secondaryClass` set; saved-PC notes include secondary class |

### 4. Handoff refresh

| Doc | Change |
|-----|--------|
| `OVERNIGHT_HANDOFF.md` | New top **Morning snapshot (wave 5)** table — Umbrin, Resonance, P0/P1=0, smoke path, collaborator day1 |

### 5. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 5 edits.

---

## Files touched (wave 5)

- `src/data/paladin-oaths.js` — L20 gifts for 8 oaths + Mercy draft gift + `finalOathGiftDraft` typedef
- `src/data/oracle-mysteries.js` — Ancestor Bloodline Convergence charge prefix
- `src/components/CharacterSheet.tsx` — `(draft)` on L20 gift when `finalOathGiftDraft`
- `src/components/SessionTracker.tsx` — multiclass badge + notes
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 5 morning snapshot
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 5 section

---

## Wave 6 — deeper content (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Director drafts OK (`draft: true`).

### 1. Oracle curse spot-check (9 draft curses vs Spiral-Touched)

| Check | Result |
|-------|--------|
| **Boons I–V (L3/5/10/15/20)** | All 9 draft curses complete — no missing tiers |
| **Limitations** | All 9 have 3 limitations each (Spiral-Touched pattern) |
| **Thin boons** | Enriched 4 sub-Spiral descriptions: **Burning Blood** Boon I, **Consumed** Boons I & II, **Fate-Bound** Boon IV |

### 2. Druid — 7 circles Paths display + hero forms

| Surface | Change |
|---------|--------|
| `druid-shapeshifting.js` | `druidPathBlocksForCircle()` filters arch path + injects circle hero-form traits into Paths tab |
| `CharacterBuilder.tsx` | Paths tab shows selected circle's arch path + hero forms; hint when no circle chosen |
| **Thorns hero forms** | Replaced placeholder "Same as Land" stubs with full Thorn-variant traits |
| **Shadow Lynx** (arch form) | Added third trait (Shadow Pounce) |

All 7 circles (`land`, `moon`, `storm`, `thorns`, `winterfang`, `rotshaper`, `ashen`) map to arch paths in `class-paths.js`.

### 3. Items/crafting filter edges + GM note

| Surface | Change |
|---------|--------|
| `ItemsLibrary.tsx` | Tab switch resets filters; crafted tab uses dynamic **skill** categories + rarities from data; search includes ingredients/effects |
| `WORLD_DUNGEON_LOOP.md` | GM note: crafting has **no Session handoff** (unlike Encounters/Generators) — log loot manually |

### 4. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 6 edits.

---

## Files touched (wave 6)

- `src/data/oracle-curses.js` — thin boon enrichment (4 entries)
- `src/data/druid-shapeshifting.js` — Thorns hero forms, Shadow Lynx, `druidPathBlocksForCircle()`
- `src/components/CharacterBuilder.tsx` — circle-filtered Paths display
- `src/components/ItemsLibrary.tsx` — crafted-tab search/filter fixes
- `docs/mechanics/WORLD_DUNGEON_LOOP.md` — crafting→session GM note
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 6 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 6 paragraph

---

## Wave 7 — items→Session handoff + generator Umbrin tags (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion.

### 1. Crafting/items → Session handoff (thin)

| Surface | Change |
|---------|--------|
| `session-handoff.ts` | `pushLootHandoff` / `consumeLootHandoff` — append-only loot lines (`items-crafted` \| `items-dropped`) |
| `ItemsLibrary.tsx` | **Log loot in Session** on crafted/dropped detail; calls `onLoadSession()` |
| `SessionTracker.tsx` | Consumes loot handoff on mount; appends bullet lines to scene notes; dismiss banner; fixed early-return skipping handoffs when no saved session |
| `page.tsx` | `ItemsLibrary onLoadSession` → SESSION tab |

### 2. Generators — Umbrin lore tags

| Surface | Change |
|---------|--------|
| `GeneratorsPanel.tsx` | Umbrin People spark shows lore tag badges (Murk exile, Obsidian Burn, Umbra faith, strange alliances); Murk/Obsidian/Shadow name bits trigger Umbrin lore hint badges on name spark |

### 3. Docs

| Doc | Change |
|-----|--------|
| `WORLD_DUNGEON_LOOP.md` | Crafting handoff note updated — thin append via Log loot in Session |

### 4. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 7 edits.

---

## Files touched (wave 7)

- `src/lib/session-handoff.ts` — loot handoff API
- `src/components/ItemsLibrary.tsx` — Log loot in Session button
- `src/components/SessionTracker.tsx` — consume loot + handoff mount fix
- `src/components/GeneratorsPanel.tsx` — Umbrin lore tags on name/people sparks
- `src/app/page.tsx` — ItemsLibrary session tab wiring
- `docs/mechanics/WORLD_DUNGEON_LOOP.md` — handoff note
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 7 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 7 paragraph

---

## Wave 7b — prestige Paths display + draft feat polish (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Director drafts OK (`draft: true`).

### 1. Prestige — Builder Paths tab (all 18 entries)

| Check | Result |
|-------|--------|
| `prestige-lorebook.json` empty fields | **0** — all 18 paths have requirements, hallmarks, capstone |
| Requirement string parsing | `parsePrestigeRequirementLines()` drops empty segments from leading `-` delimiters (no blank bullets) |
| Data normalization | `prestige.js` trims strings and filters empty hallmark slots on import |
| Builder / sheet display | Requirements, hallmarks (bulleted list), and capstone render only when non-empty |

### 2. Prestige draft feat spot-fix (3 thin effects)

| Feat | Prestige path | Change |
|------|---------------|--------|
| **Companion Training** | Beastmaster | Aethel wild-tier pack command; dual-companion at L10+; kill-advantage chain |
| **Necrotic Affinity** | Gravetouched | Grave-cold absorption reaction; low-tier raise block on necrotic kills |
| **Quickened Thought** | Chronomancer | Temporal Tower tone; concentration advantage; banked cantrip on initiative |

All three retain `draft: true` and prestige prerequisite blurbs.

### 3. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 7b edits.

---

## Files touched (wave 7b)

- `src/lib/prestige-utils.ts` — `parsePrestigeRequirementLines`, `cleanHallmarks`; feat parse uses cleaned segments
- `src/data/prestige.js` — trim/filter normalization on map
- `src/components/PrestigeRequirements.tsx` — bulleted requirements + trimmed unlock
- `src/components/CharacterBuilder.tsx` — bulleted hallmarks; hide empty sections
- `src/components/CharacterSheet.tsx` — bulleted hallmarks + capstone line
- `src/data/feats.js` — Companion Training, Necrotic Affinity, Quickened Thought enrichment
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 7b section

---

## Wave 8 — prestige feat polish + Umbrin sheet lore (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Director drafts OK (`draft: true`).

### 1. Prestige draft feat enrichment (5 thin effects)

| Feat | Prestige path | Change |
|------|---------------|--------|
| **Hardened Grip** | Forge Master | Disarm retaliation, grip-lock bonus action, oversized-weapon forge context |
| **Lightning Affinity** | Storm Lord | Outdoor cover ignore, Storm Charge reaction storage |
| **Dark Affinity** | Bloodbound | Shadow-step bonus action in dim light/darkness |
| **Primal Instinct** | Mooncursed | Moonlight initiative; pack howl grants ally advantage |
| **Combat Engineering** | Sapper | +2 emplaced cover AC, kill-zone choke deploy once/short rest |

All five retain `draft: true` and prestige prerequisite blurbs.

### 2. CharacterSheet — Umbrin lore panel

When saved race is **Umbrin**, sheet shows a violet lore card: race blurb excerpt from `races.js`, full language list, and Murkish under-tongue note.

### 3. UX copy scrub

| Surface | Change |
|---------|--------|
| `game-data.js` | Mycelian languages **Undercommon** → **Mycelian** (aligns `builder-races.js`) |
| `GeneratorsPanel.tsx` | Removed obsolete legacy Drow race-pool filter (Umbrin-only pool) |

Product-path `src/` had no remaining player-facing Drow / Umbral Elf strings outside intentional `character-storage.js` migration.

### 4. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 8 edits.

---

## Files touched (wave 8)

- `src/data/feats.js` — Hardened Grip, Lightning Affinity, Dark Affinity, Primal Instinct, Combat Engineering
- `src/components/CharacterSheet.tsx` — Umbrin lore blurb + Murkish language note
- `game-data.js` — Mycelian language label
- `src/components/GeneratorsPanel.tsx` — race pool filter cleanup
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 8 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 8 paragraph

---

## Wave 9b — Cosmology First Song chapter split (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; structure existing extract prose only — no invented lore.

### 1. First Song chapter stubs (IX–XII + full I–VIII)

| Item | Result |
|------|--------|
| **Source** | `The_Cosmology_of_Decennium_Descent_EXTRACT.txt` |
| **Split tool** | `tools/split_first_song.py` → `firstSongSections[]` in `cosmology-lore.json` |
| **Chapters** | 12 sections (I–XII); IX–XII flagged `draft: true` with extract split note |
| **Backward compat** | `firstSong` remains Ch I excerpt; `firstSongChapters` title list refreshed |

### 2. CosmologyViewer chapter nav

First Song tab now mirrors World of Aethel: Roman-numeral chapter buttons (I–XII), † marks draft chapters, per-chapter body scroll with draft banner on IX–XII.

### 3. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after CosmologyViewer edits.

---

## Files touched (wave 9b)

- `src/data/cosmology-lore.json` — `firstSongSections` I–XII from extract
- `src/components/CosmologyViewer.tsx` — First Song chapter navigation
- `tools/split_first_song.py` — reusable extract splitter
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 9b section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 9b paragraph

---

## Wave 9 — header search + prestige polish + sheet/bestiary/session UX (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Director drafts OK (`draft: true`).

### 1. Prestige draft feat enrichment (7 thin effects)

| Feat | Prestige path | Change |
|------|---------------|--------|
| **Favored Enemy (Dragon)** | Wyrmslayer | Breath-save aura, lair-hazard pursuit once/short rest |
| **Giant Slayer** | Giant Killer | Counter-strike reaction on colossal melee miss |
| **Master Smithing** | Forge Master | Named masterwork temper weekly; minor armor property |
| **Siege Savant** | Sapper | Cover-ignore detonations; collapse weak wall section |
| **Trapsetter** | Sapper | Typed traps with DC formula; reposition reaction on trigger |
| **Stormcaller** | Storm Lord | Static Field save penalty; storm outdoor radius boost |
| **Verdant Bond** | Verdant Animist | Plant memory relay; terrain movement while flora active |

All seven retain `draft: true` and prestige prerequisite blurbs.

### 2. Header search stub

| Surface | Change |
|---------|--------|
| `Header.tsx` | Live tab filter dropdown (label + keywords); Enter opens first match; no match → CHARACTERS; Escape clears |

Keywords include `umbrin`, `dungeon`, `session`, etc. — thin client index over existing nav only (CONTENT_GAPS #3 partial).

### 3. Printable sheet CSS — Umbrin lore card

| Surface | Change |
|---------|--------|
| `globals.css` | `.umbrin-lore-card` print block (avoid break, gray border, readable type); fix `#aethel-character-sheet` print id |
| `CharacterSheet.tsx` | Lore card uses `umbrin-lore-card` + `umbrin-lore-title` classes |

### 4. MonstersLibrary — Umbrin bestiary search

| Check | Result |
|-------|--------|
| Umbrin-named entries in `bestiary_data_full.json` | **10** (Umbrin, Arachnomancer, Elite Warrior, Favored Consort, House Captain, Inquisitor, Mage, Matron, Spider-Priestess, Shadowblade) |
| Search filter | Name match confirmed; **tags** now included in search index + placeholder updated |

### 5. Session — gate boss button label

| Surface | Change |
|---------|--------|
| `SessionTracker.tsx` | Button reads **Add Gate Boss: {boss name} ({stub HP} HP)** with `aria-label` for screen readers |

### 6. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 9 edits.

---

## Files touched (wave 9)

- `src/data/feats.js` — Favored Enemy (Dragon), Giant Slayer, Master Smithing, Siege Savant, Trapsetter, Stormcaller, Verdant Bond
- `src/components/Header.tsx` — tab search stub with dropdown + Enter/Escape
- `src/app/globals.css` — Umbrin lore card print styles; sheet print id fix
- `src/components/CharacterSheet.tsx` — Umbrin lore card print classes
- `src/components/MonstersLibrary.tsx` — tags in search index
- `src/components/SessionTracker.tsx` — gate boss button label + aria-label
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 9 section

---

## Wave 10 — prestige polish + cosmology world stub + loot banner (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Director drafts OK (`draft: true`).

### 1. Prestige draft feat enrichment (12 thin effects)

| Feat | Prestige path | Change |
|------|---------------|--------|
| **Slayer's Resolve** | Wyrmslayer | Dragon attack reaction — disadvantage or breath save advantage |
| **Life Drinker** | Bloodbound | Sub-half-HP melee necrotic rider on blooded foes |
| **Arcane Calculus** | Chronomancer | Stored-spell discharge — Dex save force splash |
| **Cursebound Flesh** | Mooncursed | Drop-to-1 while transformed once/long rest |
| **Beast Lore** | Beastmaster | Short-rest beast call (CR ≤1, simple task) |
| **Core Infusion** | Forge Master | Craft re-roll while wielding infused gear |
| **Conjure Flora** | Verdant Animist | Bonus-action coordinated seedling lash |
| **Anatomy Lore** | Giant Killer | Colossal hit — Str save or speed halved |
| **Eldritch Combat** | Battlemage | Once/short rest free touch spell on melee hit |
| **Curse Channeling** | Hexblade | Mark kill — heal or next-attack advantage |
| **Blood Ritual** | Mooncursed | Witnesses share half temp HP for 1 hour |
| **Dark Fortitude** | Gravetouched | Poison resistance while below half HP |

All twelve retain `draft: true` and prestige prerequisite blurbs.

### 2. Cosmology — World of Aethel extract gap

| Item | Result |
|------|--------|
| **I–VI stub** | `worldSections[]` gains draft `I-VI` card citing extract placeholder line |
| **Viewer** | World tab buttons show † on draft sections; default opens I–VI stub |
| **XIV banner** | Superseded-by-Dungeon-Guide copy preserved separately from generic draft extract |

### 3. Session — loot handoff banner copy

| Surface | Change |
|---------|--------|
| `SessionTracker.tsx` | Banner states item count, crafted/dropped source, Scene notes destination, and manual inventory note |

### 4. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 10 edits.

---

## Files touched (wave 10)

- `src/data/feats.js` — 12 prestige draft feat effect enrichments
- `src/data/cosmology-lore.json` — World of Aethel I–VI extract-gap stub
- `src/components/CosmologyViewer.tsx` — world section draft † markers + banner split
- `src/components/SessionTracker.tsx` — loot handoff banner clarity
- `tools/find_thin_prestige_feats.py` — thin draft feat scanner
- `tools/list_prestige_effect_lengths.py` — effect length listing helper
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 10 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — morning snapshot + wave 10 paragraph

---

## Wave 11 — class draft L11–20 polish (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Director drafts OK (`draft: true`).

### 1. Prestige draft feat scan

| Check | Result |
|-------|--------|
| `tools/find_thin_prestige_feats.py` | **0 thin candidates** — all 53 prestige draft feats already enriched (waves 8–10) |

### 2. Class draft level enrichment (5 thin entries)

Fallback per protocol: enriched Oracle / Paladin / Mage milestones in `class-draft-levels.js`:

| Class | Level | Change |
|-------|-------|--------|
| **Oracle** | 11 | Charge cap 7 — combat start charges = Charisma mod (min 3, max 7) |
| **Oracle** | 13 | Tier II second pick — second Mystery option; swap after short rest |
| **Oracle** | 17 | Grand Revelation foreshadow — trance reveals trigger; once/long rest failed check → success |
| **Paladin** | 16 | Oath Revelation (13th-tier) — add spell; once/long rest Smite applies rider without slot |
| **Mage** | 12 | Skill tree tier III — tradition capstone node; +1 school spell prepared per long rest |

All five retain `draft: true` via `class-level-utils.js`.

### 3. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 11 edits.

---

## Files touched (wave 11)

- `src/data/class-draft-levels.js` — 5 Oracle/Paladin/Mage draft milestone enrichments
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 11 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — morning snapshot + wave 11 one-liner

---

## Wave 12 — lint fixes + session initiative sort (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion.

### 1. ESLint warnings cleared

| File | Fix |
|------|-----|
| `CharacterBuilder.tsx:567` | `eslint-disable-next-line react-hooks/exhaustive-deps` — omit `abilities` so racial ASI re-applies only on race/method/array change, not every manual score edit |
| `druid-shapeshifting.js:382` | Named `druidShapeshifting` const + default export (was anonymous object) |

### 2. Session — initiative sort controls (content gap)

| Surface | Change |
|---------|--------|
| `SessionTracker.tsx` Round/Turn | **Sort initiative** — persist combatant order by `compareInitiativeOrder`, reset turn to 0 |
| `SessionTracker.tsx` Round/Turn | **Roll all** — d20 + Dex for every combatant, sort, reset to round 1 / turn 0 |
| Help copy | Tie-break reminder + when to use Sort vs Roll all |

### 3. Build health

```bash
npx tsc --noEmit
npm run build
```

| Check | Result |
|-------|--------|
| **`npx tsc --noEmit`** | **Pass** (exit 0, ~12s) |
| **`npm run build`** | **Pass** (exit 0, ~41s) — compiled, lint/types OK, static export 4 routes; wave 11b ESLint warnings cleared |

---

## Files touched (wave 12)

- `src/components/CharacterBuilder.tsx` — exhaustive-deps intentional disable
- `src/data/druid-shapeshifting.js` — named default export
- `src/components/SessionTracker.tsx` — Sort initiative + Roll all buttons
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 12 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 12 append (opening brief preserved)

---

## Wave 13 — encounters search + Umbrin picker + export fields (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion.

### 1. EncountersBrowser — search polish

| Surface | Change |
|---------|--------|
| Search input | Matches tier name, floors, description, gate boss — not just havens/POIs |
| Cross-tier chips | When query matches any tier, **Matches:** row offers one-click tier jump |
| Clear control | X button clears search without losing tier selection |
| Tier meta hit | Boss/name/description match shows full haven + POI lists for that tier |

### 2. CharacterBuilder — Umbrin in People picker

| Surface | Change |
|---------|--------|
| Sort | **Umbrin** pinned first (★ in dropdown); remaining peoples keep ingest order |
| Search | Filter input — name, lineage, trait, or language (e.g. Murkish → Umbrin) |

### 3. Export JSON — subclass fields always present

| Field | Change |
|-------|--------|
| `sacredOath` / `druidCircle` / `oracleMystery` / `oracleCurse` | Already in payload — unchanged |
| `secondaryClass` / `secondaryLevel` | Always emitted (empty / undefined when single-class); matches `normalizeCharacter` shape |

### 4. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 13 edits (~12s).

---

## Files touched (wave 13)

- `src/components/EncountersBrowser.tsx` — cross-tier search, tier meta match, clear button
- `src/components/CharacterBuilder.tsx` — Umbrin pin + People search; export payload secondary fields
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 13 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 13 append (morning brief preserved)

---

## Wave 14 — bestiary filters + session handoff tick + search shortcut (2026-07-29 PM)

**Worker:** UX polish overnight pass  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **MonstersLibrary** | Search matches CR (`cr 5` prefix), type, zone; clear (X) on search; **Clear filters** when any dropdown active |
| **GeneratorsPanel → Session** | Shared `goToSession()` in `page.tsx` bumps `sessionHandoffTick`; `SessionTracker` re-applies encounter handoff on tick (Generators / Encounters / Items) |
| **Header** | `/` focuses tab search (skips when typing in inputs); placeholder + `kbd` hint |
| **Typecheck** | `npx tsc --noEmit` — exit 0 (~13s) |

---

## Files touched (wave 14)

- `src/components/MonstersLibrary.tsx` — CR/type/zone search polish, clear search + filters
- `src/app/page.tsx` — `sessionHandoffTick` + shared `goToSession()`
- `src/components/SessionTracker.tsx` — `handoffTick` prop + apply on navigation
- `src/components/Header.tsx` — `/` keyboard shortcut + hint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 14 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 14 append

---

## Wave 15 — sheet print identity + session crowd UX + idempotent handoff (2026-07-29 PM)

**Worker:** High-ROI overnight pass  
**Commit:** none (per owner request)

| Item | Result |
|------|--------|
| **CharacterSheet print** | Header identity strip: secondary class L#, Oath, Circle, Mystery, Curse when set — print-friendly gray text |
| **SessionTracker crowd UX** | All/Allies/Foes filter at ≥7 combatants; foes auto-collapse at ≥4 with expand toggle; active-hidden hint |
| **Handoff idempotency** | `takeEncounterHandoff` / `takeLootHandoff` keyed by `createdAt`; mount + `handoffTick` share refs — no double-consume |
| **Loot on tick** | Loot handoff now applies when already on Session tab (functional scene-notes append) |
| **Typecheck** | `npx tsc --noEmit` — exit 0 (~14s) |

---

## Files touched (wave 15)

- `src/components/CharacterSheet.tsx` — print identity strip
- `src/components/SessionTracker.tsx` — filter, foes collapse, idempotent handoffs
- `src/lib/session-handoff.ts` — `take*` helpers
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 15 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 15 append

---

## Wave 14b — draft feat scan + Oracle L1 consistency (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Director drafts OK (`draft: true`).

### 1. Draft feat thin-effect scan

| Check | Result |
|-------|--------|
| `tools/find_thin_draft_feats.py` | **0 thin candidates** — all draft feats have effect text ≥ 80 chars (prestige enrichments waves 8–10) |

### 2. Oracle mystery L1 enrichment (fallback — 3 thinnest vs Ancestor/Battle template)

| Mystery | L1 revelation | Change |
|---------|-----------------|--------|
| **Time** | Spiral Echo | Second passive (initiative-order floor); delayed effect covers spell/attack/condition; 1-tile move on resolution |
| **Shadow** | Umbral Cloak | +5% psychic resistance; Hush invisibility + first-from-concealment +25% psychic rider |
| **Flame** | Ember Mantle | Fire resistance clarified; mantle ignite adds 2-tile warm light + ally fear-save bonus |

All three mysteries retain `draft: true` via `draftMysteryRevelations()`.

### 3. Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 14b edits (~12s).

---

## Files touched (wave 14b)

- `src/data/oracle-mysteries.js` — Time / Shadow / Flame L1 revelation consistency
- `tools/find_thin_draft_feats.py` — all-draft feat thin scanner (new)
- `tools/oracle_l1_lengths.py` — L1 description length helper (new)
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 14b section

---

## Wave 15b — remaining Oracle L1 enrichment (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; `draft: true` retained via `draftMysteryRevelations()`.

### Oracle mystery L1 enrichment (6 remaining thin vs Time/Shadow/Flame wave 14b baseline)

Threshold: L1 description length &lt; 246 chars (Flame post-14b).

| Mystery | L1 revelation | Change |
|---------|-----------------|--------|
| **Battle** | Omen of the Host | +5% fear resistance; battle-oath adds +5% DR until next turn |
| **Bones** | Grave Attendant | +5% necrotic resistance; skeletal servant intercepts next single-target hit |
| **Cataclysm** | Tremor Sense | +5% bludgeoning resistance; tremor hits 2-tile area with partial-movement rider on save |
| **Dream** | Dreamer's Veil | Advantage vs sleep; ally's first concealment attack +25% psychic |
| **Life** | Bloom Ward | +5% necrotic/poison resistance; bloom range 3 tiles + fear-save petals on wilt |
| **Stars** | Starlight Mantle | +5% radiant resistance; illuminate allies gain +2 to hit on next attack |

All six mysteries retain `draft: true` via `draftMysteryRevelations()`.

**Enriched count:** 6

### Typecheck

```bash
npx tsc --noEmit
```

**Exit:** 0 — no TypeScript errors after wave 15b edits.

---

## Files touched (wave 15b)

- `src/data/oracle-mysteries.js` — Battle / Bones / Cataclysm / Dream / Life / Stars L1 revelation consistency
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 15b section

---

## Wave 16 — Spells Oracle UX + Paladin L3 oath enrichment (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion; append handoff only.

### 1. Build verification

| Check | Result |
|-------|--------|
| `npx tsc --noEmit` | **Exit 0** (~11s) — clean at wave start |
| `npm run build` | **Exit 0** (~47s) — static export OK; 2 unused eslint-disable warnings in SessionTracker (pre-existing) |

### 2. Spells Library — Oracle Revelation note (UX)

| Surface | Change |
|---------|--------|
| Class filter | Oracle labeled **Oracle (Revelations)** in dropdown |
| Banner | Violet callout when Oracle selected: not Weave; RC/Mystery path in Builder; list is thematic reference only |
| Stats line | Appends `(reference)` when Oracle filter active |
| `spell-utils.js` | Exported `REVELATION_CASTERS` + `isRevelationCaster()` for reuse |

### 3. Paladin draft oath L3 enrichment (3 vs Mercy template)

Mercy baseline: L3 smite + revelation with conditional rider (`Blessing of the Meek — heal + AC if HP < 50%`).

| Oath | L3 smite / revelation | Change |
|------|------------------------|--------|
| **Dominion** | Smite + Compelled Truth | Smite: liars in aura −1 saves; L3: 10-ft zone + psychic on failed Charisma save |
| **Silence** | Hush | If silent since combat start, target also suffers disadvantage on next attack |
| **Martyr King** | Smite + Noble Bearing | Smite: redirect 5 ally damage/round; L3: aura morale + temp HP on smite (half radiant) |

All three oaths retain `draft: true`.

**Enriched count:** 3

### 4. Post-edit typecheck

```bash
npx tsc --noEmit
npm run build
```

**Exit:** 0 — no TypeScript errors; production build OK after wave 16 edits.

---

## Files touched (wave 16)

- `src/data/spell-utils.js` — `isRevelationCaster`, exported `REVELATION_CASTERS`
- `src/components/SpellsLibrary.tsx` — Oracle (Revelations) label + banner
- `src/data/paladin-oaths.js` — Dominion / Silence / Martyr King L3 smite + revelation enrichment
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 16 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 16 append

---

**Midnight checkpoint:** [`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) — early-wake one-glance status (waves 1–16, build green, P0/P1=0).

---

## Wave 17 — SessionTracker lint + Paladin L3 + Spells clear-filters (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion; append handoff only.

### 1. SessionTracker — unused eslint-disable cleanup

| Surface | Change |
|---------|--------|
| Mount `useEffect` | Removed unused `react-hooks/exhaustive-deps` disable (wave 16 build warning) |
| Handoff tick `useEffect` | Removed unused disable — `[handoffTick]` satisfies exhaustive-deps |

### 2. Paladin draft oath L3 enrichment (3 vs Mercy template)

Mercy baseline: L3 smite + revelation with conditional rider (`Blessing of the Meek — heal + AC if HP < 50%`).

| Oath | L3 smite / revelation | Change |
|------|----------------------|--------|
| **Ancients** | Smite + Roots of Memory | Smite: roots until end of next turn on crit; fey/elementals disadvantage vs smite saves; L3: 10-ft burst + Str save restrain + origin lore |
| **Chain** | Smite + Linked Ward | Smite: redirect CHA mod (min 3) from bonded ally once/round; L3: reaction redirect 2× CHA mod; temp HP rider if paladin falls |
| **Grief** | Smite + Dirge | Smite: +1d8 vs killers-of-allies + Grief Mark; L3: 30-ft cone or single target, Wis save −2 attacks, undead 2d6 radiant |

All retain `draft: true`. Vengeance / Flame skipped (already enriched prior waves).

### 3. Spells Library — clear filters UX

| Surface | Change |
|---------|--------|
| Filter bar stats row | **Clear filters** ghost button when search/school/level/class active (matches MonstersLibrary pattern) |
| `hasActiveFilters` | Tracks non-default filter state; stats show `(filtered)` suffix |

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~10s)
npm run build      # exit 0 (~42s) — static export OK; no eslint-disable warnings
```

**Exit:** 0 — no TypeScript errors; production build clean after wave 17 edits.

---

## Files touched (wave 17)

- `src/components/SessionTracker.tsx` — remove 2 unused eslint-disable directives
- `src/data/paladin-oaths.js` — Ancients / Chain / Grief L3 smite + revelation enrichment
- `src/components/SpellsLibrary.tsx` — clear-filters button + `hasActiveFilters`
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 17 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 17 append

---

## Wave 18b — Oracle curse boon depth (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. `draft: true` retained on all nine draft curses.

### 1. Oracle curse spot-check (9 draft curses vs Spiral-Touched)

| Check | Result |
|-------|--------|
| **Boons I–V (L3/5/10/15/20)** | All 9 draft curses complete — no missing tiers |
| **Limitations** | All 9 have 3 limitations each (Spiral-Touched pattern) |
| **Thin boons** | 12 single-sentence boons found; **4 enriched** to ~2-sentence Spiral-Touched depth |

**Enriched (4):**

| Curse | Boon | Change |
|-------|------|--------|
| **Consumed** | Boon IV (L15) | Partial transformation — allies following within 1 tile share terrain passage |
| **Fate-Bound** | Boon I (L3) | Glimpse omen — must speak aloud; allies retain bonus on alternate path |
| **Haunted** | Boon II (L5) | Spirit intercept — attacker dread save rider on dissipating wail |
| **Soul-Cracked** | Boon II (L5) | Resonance shift — aura blank to divination until Revelation resolves |

**Remaining thin (8, deferred):** Burning Blood L5/L10/L20, False Life L20, Shattered Mind L3, Fate-Bound L20, Haunted L20, Consumed L20.

**Enrichment count:** 4

---

## Wave 18 — Paladin L3 + CraftingBuilder filters (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion; append handoff only.

### 1. Paladin draft oath L3 enrichment (2 vs Mercy template)

Mercy baseline: L3 smite + revelation with conditional rider (`Blessing of the Meek — heal + AC if HP < 50%`).

| Oath | L3 smite / revelation | Change |
|------|----------------------|--------|
| **Vengeance** | Mark of Retribution | L3: 30-ft Wis save mark; +1d8 smite vs marked; advantage on opportunity attacks until end of next turn |
| **Chains Broken** | Smite + Break Bonds | Smite: on hit target loses grapple/restraint until end of next turn; L3: touch or 30-ft ally ends restraint/grapple; magically bound allies gain +10 ft movement + escape advantage |

All retain `draft: true`. Flame skipped (L3 already has on-crit rider). **All 9 draft oaths now L3-enriched.**

### 2. CraftingBuilder — clear-filters + search polish

| Surface | Change |
|---------|--------|
| Components library | **Clear filters** when search/category/tier active; `(filtered)` count suffix; empty-state message |
| Component search | Haystack includes category, rarity, properties (parity with ItemsLibrary) |
| Recipe catalog | **Clear filters** when search/skill active; `(filtered)` count suffix |

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

**Exit:** 0 — no TypeScript errors after wave 18 edits.

---

## Files touched (wave 18)

- `src/data/paladin-oaths.js` — Vengeance / Chains Broken L3 smite + revelation enrichment
- `src/components/CraftingBuilder.tsx` — clear-filters UX + expanded component search
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–18 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 18 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 18 append

---

## Wave 19 — Oracle curse boon depth finish + ItemsLibrary filters (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. `draft: true` retained on all nine draft curses.

### 1. Oracle curse spot-check — 8 deferred boons enriched (wave 18b finish)

| Check | Result |
|-------|--------|
| **Thin boons (deferred)** | 8 single-sentence boons from wave 18b → **all enriched** to ~2-sentence Spiral-Touched depth |
| **Depth scan** | `tools/oracle_curse_boon_depth.py` — **0 draft boons under 2 sentences** |

**Enriched (8):**

| Curse | Boon | Change |
|-------|------|--------|
| **Burning Blood** | Boon II (L5) | Ignite blood — adjacent allies safe while ignited; Crown flame answers only to your will |
| **Burning Blood** | Boon III (L10) | Shard-fire ally buff — extend flare to 3 tiles for 1d4 burst via RC |
| **Burning Blood** | Boon V (L20) | Living pyre — allies gain fire resistance + bright-light reveal rider |
| **False Life** | Boon V (L20) | Death threshold — undead kinship + false divination results during feigned death |
| **Shattered Mind** | Boon I (L3) | Fragment bonus action — observers hear answers to unasked questions |
| **Fate-Bound** | Boon V (L20) | Prophetic outcome — must speak aloud; RC loss if prophecy fails by combat end |
| **Haunted** | Boon V (L20) | Spirit bind scout — 10-min task + whispered name rider on return |
| **Consumed** | Boon V (L20) | Full embodiment — allies +1 AC; suppression impossible while active |

All nine draft curses now have Spiral-Touched-parity boon depth across L3/5/10/15/20. All retain `draft: true`.

**Enrichment count:** 8 (12 total with wave 18b)

---

### 2. ItemsLibrary — clear-filters UX

| Surface | Change |
|---------|--------|
| Dropped / Crafted tabs | **Clear filters** button when search/rarity/category/tier active; `(filtered)` count suffix |

Parity with MonstersLibrary / SpellsLibrary / CraftingBuilder filter UX.

---

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

**Exit:** 0 — no TypeScript errors after wave 19 edits.

---

## Files touched (wave 19)

- `src/data/oracle-curses.js` — 8 deferred curse boon enrichments
- `src/components/ItemsLibrary.tsx` — clear-filters UX
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–19 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 19 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 19 append

---

## Wave 20 — class draft enrichments + Dungeon Guide search (overnight worker, 2026-07-29 PM)

**Protocol:** No commits; no mass deletion. Oracle curses and Paladin L3 deferred (already at depth). `draft: true` retained on all enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Enriched short L11–20 milestones in `class-draft-levels.js` to Oracle/Paladin parity depth (~80–120 chars):

| Class | Level | Change |
|-------|-------|--------|
| **Bard** | 11 | Crescendo die d10 — roll on Inspire Courage; add to ally attack/save within 1 round |
| **Cleric** | 16 | Domain capstone — Channel Divinity duplicates domain 6th-level spell; 30-ft resistance aura |
| **Monk** | 16 | Ki Chain cap 7 — full chain release refunds 1 Ki on next unarmed hit |
| **Shaman** | 11 | Flask Tier III — three concurrent flasks; spending no longer ends totem pulse |
| **Dragoon** | 16 | Apex Assault cooldown — 1 bonus-action recharge; first leap ignores difficult terrain |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Dungeon Guide — search/filter UX

| Surface | Change |
|---------|--------|
| Search bar | Filter tiers by name, boss, floors, description, havens, POIs |
| Mapped toggle | **Mapped tiers only** quick filter (T1–5) |
| Mechanics tab | Gate bosses and victory consequences respect active search |
| Clear filters | Parity with library filter UX; match count suffix |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–20**, build green.

### 4. Build

```bash
npm run build   # exit 0 (~45s) — compiled, lint/types OK, static export 4 routes
```

---

## Files touched (wave 20)

- `src/data/class-draft-levels.js` — Bard/Cleric/Monk/Shaman/Dragoon L11–20 enrichments
- `src/components/DungeonGuide.tsx` — search/filter + mapped toggle
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–20
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 20 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 20 append

---

## Wave 20b — ReputationPanel filter/search

**Status:** Shipped (no commit)

### 1. ReputationPanel — faction filter/search

| Surface | Change |
|---------|--------|
| Full editor mode | Search input (name / category / description) + category select + Clear |
| Draft factions | `draft` badge already present — verified on all draft-flagged factions |
| Compact mode | Unchanged — no filter chrome (non-zero factions only) |

Filter row appears only in `mode="full"` (Character Builder background editor). Empty-filter message when no matches.

### 2. Build

```bash
npx tsc --noEmit   # exit 0
```

**Exit:** 0 — no TypeScript errors after wave 20b edit.

---

## Files touched (wave 20b)

- `src/components/ReputationPanel.tsx` — faction search + category filter
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 20b section

---

## Wave 21 — class draft enrichments + header search help (2026-07-29 PM)

**Protocol:** No commits; no mass deletion. `draft: true` retained on all enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Enriched short L11–20 milestones in `class-draft-levels.js` to Oracle/Paladin parity depth (~80–120 chars):

| Class | Level | Change |
|-------|-------|--------|
| **Warrior** | 12 | Brutality Threshold — 100% max HP damage dealt unlocks Transcendent mutation tier for 3 rounds |
| **Wizard** | 16 | Arcane Tradition capstone — +1 tier school cast 1/long rest; 10-ft elemental resistance aura |
| **Thief** | 16 | Poison prep +1 — three toxins; Sneak Attack poison no longer costs bonus action |
| **Ranger** | 11 | Druidic Arrow combo — Hunter's Mark hit + slot for second radiant arrow (slot level d8) |
| **Tinker** | 16 | Third deployable slot — three gadgets; two activations share one bonus action |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Header search — shortcut help tooltip

| Surface | Change |
|---------|--------|
| Search bar | `?` (CircleHelp) hover/focus tooltip listing **`/`** focus and **Esc** clear & blur |
| Existing | `/` global focus and Esc clear already wired — tooltip documents both |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–21**, typecheck green.

### 4. Typecheck

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 21)

- `src/data/class-draft-levels.js` — Warrior/Wizard/Thief/Ranger/Tinker L11–20 enrichments
- `src/components/Header.tsx` — search shortcut help tooltip
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–21
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 21 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 21 append

---

## Wave 22 — class draft enrichments + Session empty state (2026-07-30)

**Protocol:** No commits; no mass deletion. `draft: true` retained on all enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Enriched short L11–20 milestones in `class-draft-levels.js` to Oracle/Paladin parity depth (~80–120 chars):

| Class | Level | Change |
|-------|-------|--------|
| **Bard** | 16 | Counter-Melody mastery — spend 1 Crescendo to redirect ally's failed spell/sonic save onto you with advantage |
| **Mage** | 18 | 9th-level slots — one 9th-tier Resonance slot; full-pool cost unless Archmage Reservoir unused |
| **Soldier** | 12 | Skill tree tier III — Formation/Overwatch capstone; Palisade +2 AC to allies in cover for 1 round |
| **Crimson Agent** | 12 | Skill tree tier III — Veinweave/Shadowblade capstone; Sneak Attack on Blood Mark refreshes one Veinweave charge |
| **Mirrorsage** | 18 | Focus Points +1 per battle — form shift no longer ends Echo Slot hold on prior spell |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Session — combatants empty state

| Surface | Change |
|---------|--------|
| Combatants list | Empty-state tip: **"Add saved character or foe."** when initiative table has zero rows |

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 22 append

---

## Wave 22b — prestige hallmark enrichments (overnight worker, 2026-07-30)

**Protocol:** No commits; no mass deletion. Aethel tone on thin hallmark arrays only.

### 1. Prestige hallmark enrichment (3 thin arrays)

Scanned `prestige-lorebook.json` — thinnest hallmark sets: **Beastmaster** and **Blademaster** (3 entries each); **Chronomancer** (4 entries, lowest average line length). One hallmark enriched per path:

| Prestige | Hallmark | Change |
|----------|----------|--------|
| **Beastmaster** (#2) | Primal Pack | Wild-tier pack binding across Aethel descent tiers; companions scale as pack kin |
| **Blademaster** (#3) | Blade Echo | Duelist flow echo — third strike grants free maneuver from muscle-memory rhythm |
| **Chronomancer** (#6) | Delay Action | Temporal Tower clockwork cadence; bank unused actions, spend when Weave rhythm owes a turn |

Entrance/unlock blurbs unchanged — hallmarks were the thin target.

### 2. Typecheck

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 22b)

- `src/data/prestige-lorebook.json` — Beastmaster, Blademaster, Chronomancer hallmark enrichments
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 22b section

---

## Wave 23 — class draft + prestige hallmark enrichments (overnight worker, 2026-07-30)

**Protocol:** No commits; no mass deletion; append handoff only. `draft: true` retained on all enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Wave 22 covered Bard/Mage/Soldier/Crimson Agent/Mirrorsage. This wave targets remaining thin canon-17 entries (Swashbuckler skipped — orphan):

| Class | Level | Change |
|-------|-------|--------|
| **Dragoon** | 12 | Skill tree tier III — Dragon Lancer/hero capstone; Wyvern's Flow Momentum refund; Apex Assault overflow +1d6 per stack above cap |
| **Monk** | 20 | Transcendent Flow — stance shift twice per round; max Ki Chain grants +1 temp Ki until end of turn |
| **Shaman** | 17 | Flask Tier IV — four concurrent flasks; spending triggers Totem Pulse on nearest active totem |
| **Cleric** | 18 | Divine Intervention — once/week prayer succeeds on nat 1; success restores one Channel Divinity |
| **Druid** | 11 | Arch Druid Forms — Dire Wolf, Earth Warden, Sky Serpent, circle arch shapes; Wild Shape CR = tier floor −1 (min CR 2); L11 removed from `class-details.js` so draft merge applies |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Next thinnest after Beastmaster/Blademaster/Chronomancer (wave 22b): **Berserker**, **Mooncursed**, **Battlemage** (4 entries each, lowest average line length). One hallmark enriched per path:

| Prestige | Hallmark | Change |
|----------|----------|--------|
| **Battlemage** (#1) | Battle Flow | Momentum stacks persist through short rests along Aethel descent tiers until spent or concentration breaks |
| **Berserker** (#2) | Sweeping Blow | Ritual cleave through two adjacent foes — knockback + Stagger until Frenzy ends |
| **Mooncursed** (#4) | Beast Within | Auto-transform at ≤25% HP for 60s; choose form if multiple unlocked, else bound curse form |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–23**, build green.

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~10s)
```

---

## Files touched (wave 23)

- `src/data/class-draft-levels.js` — Dragoon/Monk/Shaman/Cleric/Druid L11–20 enrichments
- `src/data/class-details.js` — Druid L11 removed (draft merge)
- `src/data/prestige-lorebook.json` — Battlemage, Berserker, Mooncursed hallmark enrichments
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–23
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 23 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 23 append

---

## Wave 24b — build checkpoint (overnight worker, 2026-07-30)

**Protocol:** No commits.

### Build

```bash
npm run build   # exit 0 (~47s)
```

Next.js 15.4.5 — compiled successfully; lint and typecheck passed; static pages generated and export completed (routes: /, /_not-found).

---

## Wave 24 — class draft + prestige hallmark + Umbrin lore tip (overnight worker, 2026-07-30)

**Protocol:** No commits; no mass deletion; append handoff only. `draft: true` retained on enriched milestones.

### 1. Class draft level enrichment (3 thin entries)

Class drafts still dominate thin backlog (~50 mech stubs vs ~15 prestige hallmark lines). Wave 23 covered Dragoon/Monk/Shaman/Cleric/Druid; this wave targets remaining L12 skill-tree stubs:

| Class | Level | Change |
|-------|-------|--------|
| **Ranger** | 12 | Skill tree tier III — Beastwarden or Stalker's Path capstone; Hunter's Mark d8; Favored Terrain bonus to allies within 10 ft |
| **Thief** | 12 | Skill tree tier III — Shadowblade or Poisoner capstone; Sneak Attack on poisoned target refreshes one toxin prep (once/target per short rest) |
| **Tinker** | 12 | Skill tree tier III — Siege Engineer or Anacite Savant capstone; deployables +2 HP threshold; first bomb +5 ft radius each encounter |

### 2. Prestige hallmark enrichment (2 thin arrays)

Next thinnest after wave 23: **Giant Killer** (all four hallmarks short), **Berserker** (Deathlust still thin after Sweeping Blow enrich).

| Prestige | Hallmark | Change |
|----------|----------|--------|
| **Giant Killer** (#1) | Kneecap Strike | Huge+ leg cripple on crit or ≥ half max HP strike — −15 ft move; second kneecap Prone |
| **Berserker** (#3) | Deathlust | Each Frenzy kill +1 round (max +3); boss kill resets one Reckless Charge |

### 3. CharacterBuilder — Obsidian Burn lore tip

When **Umbrin** is selected under People, one-line **Obsidian Burn (draft)** tip under race picker; **Lore (draft)** button opens COSMOLOGY tab via `onOpenLore` from `page.tsx`.

### 4. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–24**, build green.

### 5. Build

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 24 append

---

## Wave 25 — class draft + prestige hallmark enrichments (2026-07-30)

**Protocol:** No commits; no mass deletion; append handoff only. `draft: true` retained on enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Wave 24 covered Ranger/Thief/Tinker L12. Soldier/Crimson Agent/Mage/Warrior L12 were enriched in wave 22. This wave clears the remaining L12 skill-tree stubs plus Warrior capstone:

| Class | Level | Change |
|-------|-------|--------|
| **Bard** | 12 | Skill tree tier III — Virtuoso or Discord capstone; Counter-Melody +1 stack reserve; Song of Rest builds 1 Crescendo on ally HP recovery |
| **Mirrorsage** | 12 | Skill tree tier III — Light Weaver or Shattered One capstone; first witnessed spell echoes at half RP cost (min 1) |
| **Shaman** | 12 | Skill tree tier III — Theurgist or Bloodcaller capstone; totem placement releases flask mist in 10 ft (once/totem/encounter) |
| **Monk** | 12 | Skill tree tier III — Enlightened Master or Iron Fist capstone; stance entry +1 Ki Chain storage until shift |
| **Warrior** | 20 | Apex Form — fourth mutation slot 1/encounter per long rest; Brutality Threshold skips damage gate for Transcendent tier |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Prestige hallmark enrichment (2 thin arrays)

Next thinnest after wave 24 (Giant Killer/Berserker): **Echomancer**, **Gravetouched** (generic hallmark lines, unenriched).

| Prestige | Hallmark | Change |
|----------|----------|--------|
| **Echomancer** (#7) | Mirror Pulse | Echo retains original tier/school; redirect to second target within 30 ft |
| **Gravetouched** (#10) | Bone Shield | While active, Death Touch applies Vulnerable to necrotic until shield fades |

### 3. Midnight checkpoint

[`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) updated — waves **1–25**, build green.

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~9s)
```

---

## Files touched (wave 25)

- `src/data/class-draft-levels.js` — Bard/Mirrorsage/Shaman/Monk L12 + Warrior L20 enrichments
- `src/data/prestige-lorebook.json` — Echomancer, Gravetouched hallmarks
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–25
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 25 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — this wave 25 append

---

## Wave 26b — prestige hallmark enrichments (overnight worker, 2026-07-30)

**Protocol:** No commits; no mass deletion; append progress only. Aethel tone on thinnest unenriched hallmark lines (skip waves 22–25 targets).

### 1. Prestige hallmark enrichment (4 thin arrays)

Scanned `prestige-lorebook.json` — next four shortest hallmarks not enriched in waves 22–25:

| Prestige | Hallmark | Change |
|----------|----------|--------|
| **Verdant Animist** (#16) | Bloom Burst | 15 ft seedling detonation; lingering thorn/spore difficult terrain with reactive entry damage |
| **Chronomancer** (#6) | Rewind | Prior-round action/save reversal via Temporal Tower cadence; Fatigue accrual cap |
| **Chronomancer** (#6) | Time Rip | Aethel timeline aging — AC/Dex save penalty; construct/undead force-damage fallback |
| **Gravetouched** (#10) | Death Touch | Tier-floor necrotic on hit; Wither halves healing until end of next turn |

Entrance/unlock blurbs unchanged — hallmarks were the thin target.

### 2. Build

```bash
npx tsc --noEmit
```

---

## Files touched (wave 26b)

- `src/data/prestige-lorebook.json` — Verdant Animist, Chronomancer (Rewind/Time Rip), Gravetouched hallmark enrichments
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 26b section

---

## Wave 26 — class draft + prestige hallmark enrichments (2026-07-30)

**Protocol:** No commits; no mass deletion; append handoff only. `draft: true` retained on enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Wave 25 cleared remaining L12 skill-tree stubs. This wave targets the thinnest non-ASI milestones still under ~60 chars:

| Class | Level | Change |
|-------|-------|--------|
| **Cleric** | 11 | Destroy Undead (CR 2) — Turn destroys CR 2 or lower on failed save; sanctified ash lingers 1 round as holy focus |
| **Cleric** | 12 | Channel Divinity (3/rest) — third use per short rest; first Channel each encounter gains +10 ft radius on domain option |
| **Shaman** | 13 | Second active totem slot — two totems concurrently; placing second triggers weak pulse on first (once/encounter) |
| **Shaman** | 18 | Totem duration +1 round — totems persist one extra round; natural expiry releases stored flask mist in 5 ft burst |
| **Thief** | 17 | Death Blossom (Shadowblade) — once/short rest, Sneak Attack on poisoned target detonates toxin stacks in 10 ft radius |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Prestige hallmark enrichment (2 thin arrays)

Wave 26b (parallel) covered Verdant Animist/Chronomancer/Gravetouched. This wave picks next thinnest: **Bloodbound**, **Mooncursed**.

| Prestige | Hallmark | Change |
|----------|----------|--------|
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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 26 append

---

## Wave 27 — class draft + prestige hallmark enrichments (2026-07-30)

**Protocol:** No commits; no mass deletion; append handoff only. `draft: true` retained on enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Wave 26 cleared Cleric/Shaman/Thief milestones. This wave targets the five shortest remaining non-ASI stubs:

| Class | Level | Change |
|-------|-------|--------|
| **Dragoon** | 11 | Extra Attack — second strike when you take the Attack action; Wyvern's Flow leap-attacks count as one attack for Extra Attack sequencing (once/turn) |
| **Mage** | 7 | 4th-level slots — gain one 4th-tier Resonance slot; overcast from this tier costs +1 RP beyond base (min 2 RP total) |
| **Mage** | 11 | 5th-level slots — gain one 5th-tier Resonance slot; tradition spells at this tier may be prepared without slot cost once per long rest |
| **Mage** | 13 | 6th-level slots — gain one 6th-tier Resonance slot; casting your school's signature spell at this tier does not trigger Burnout on success |
| **Mage** | 15 | 7th-level slots — gain one 7th-tier Resonance slot; allies within 10 ft gain advantage on saves vs. your school's element when you cast at this tier |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Skipped recently enriched (waves 24–26: Giant Killer, Berserker, Echomancer, Gravetouched, Bloodbound, Mooncursed, Verdant Animist, Chronomancer). Next thinnest:

| Prestige | Hallmark | Change |
|----------|----------|--------|
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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 27 append

---

## Wave 27b — SessionTracker Clear foes (overnight worker, 2026-07-30)

**Protocol:** No commits; append progress only.

### 1. SessionTracker — Clear foes button

| Surface | Change |
|---------|--------|
| Combatants toolbar | **Clear foes** — removes all `isEnemy` combatants; allies remain on table |
| Turn index | Clamped with `% allyCount` after clear; resets to 0 if no allies |
| Crowd UX | Collapses foes section; switches filter from Foes → All when applicable |
| Button state | Disabled when zero foes; tooltip explains allies are kept |

### 2. Sort / Roll all — verified unchanged

| Control | Behavior |
|---------|----------|
| **Sort initiative** | `sortInitiative()` — re-sorts by `compareInitiativeOrder`, resets turn to 0 |
| **Roll all** | `rollAllInitiative()` — d20 + Dex per combatant, sort, round 1 / turn 0 |

Both remain wired in Round/Turn card; no logic changes this wave.

### 3. Typecheck

```bash
npx tsc --noEmit   # exit 0 (~10s)
```

---

## Files touched (wave 27b)

- `src/components/SessionTracker.tsx` — Clear foes button + `clearFoes()` handler
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 27b section

---

## Wave 28 — class draft + prestige hallmark enrichments (2026-07-30)

**Protocol:** No commits; no mass deletion; append handoff only. `draft: true` retained on enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Wave 27 cleared Dragoon/Mage slot milestones. This wave targets the five shortest remaining non-ASI stubs:

| Class | Level | Change |
|-------|-------|--------|
| **Mage** | 17 | 8th-level slots — gain one 8th-tier Resonance slot; overcast costs +2 RP and requires concentration check (DC 15 + tier) or triggers Burnout |
| **Crimson Agent** | 7 | Sneak Attack (4d6) — advantage or ally within 5 ft; Blood Marked targets take +1d6 and refresh mark duration by 1 round |
| **Crimson Agent** | 11 | Sneak Attack (5d6) — advantage or ally within 5 ft; Veinweave charges spent on Sneak Attack skip bonus action (once/turn) |
| **Thief** | 11 | Sneak Attack (6d6) — advantage or ally within 5 ft; poisoned targets take +1d6 and refresh one toxin prep on hit |
| **Monk** | 11 | Extra Attack (unarmed) — second unarmed strike on Attack action; Flurry of Blows counts as one attack for sequencing (once/turn) |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Skipped recently enriched (waves 24–27: Hexblade, Blademaster, Warlock, Giant Killer, Berserker, Echomancer, Gravetouched, Bloodbound, Mooncursed). Next thinnest:

| Prestige | Hallmark | Change |
|----------|----------|--------|
| **Wyrmslayer** (#18) | Drakebane Arsenal | Forged wyrmslayer gear ignores dragon resistances; crit strips one resistance category until end of next turn |
| **Soulrender** (#14) | Soul Harvest | Absorb souls within 30 ft for charges (max tier floor + 2); charges fuel Agony Lance and Spectral Ward without slots |
| **Storm Lord** (#15) | Static Field | 15 ft charged zone shocks at turn start (tier floor d6); Voltyros-aligned foes save at disadvantage on entry |

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 28 append

---

## Wave 29 — class draft + prestige hallmark enrichments (2026-07-30)

**Protocol:** No commits; no mass deletion; append handoff only. `draft: true` retained on enriched milestones.

### 1. Class draft level enrichment (5 thin entries)

Wave 28 cleared Mage/Crimson Agent/Thief/Monk stubs. This wave targets the five shortest remaining non-ASI stubs:

| Class | Level | Change |
|-------|-------|--------|
| **Soldier** | 11 | Extra Attack (crossbow volley) — second shot on Attack action with crossbow; Overwatch reactions skip Extra Attack sequencing (once/turn) |
| **Soldier** | 16 | Overwatch zone expands to 4×4 — 4-tile square within range; zone entry provokes reaction shots at advantage; Palisade allies gain half cover |
| **Mirrorsage** | 11 | Echo Slot Expansion III — max 6 witnessed spells; releasing echo at half Resonance cost no longer ends Mirror Beast shift (once/encounter) |
| **Shaman** | 16 | Spirit Cache — store two flask/totem effects between rests; spending cached effect triggers Totem Pulse without placing new totem (once/encounter) |
| **Tinker** | 15 | Danger Close — bombs never harm allies; friendly fire redirects as 5 ft push and grants allies +1 AC until next turn |

All five retain `draft: true` via `class-level-utils.js`.

### 2. Prestige hallmark enrichment (3 thin arrays)

Skipped recently enriched (waves 24–28). Next thinnest non-recent paths: **Forge Master**, **Sapper**.

| Prestige | Hallmark | Change |
|----------|----------|--------|
| **Forge Master** (#8) | Relic Imbuement | Imbue one weapon/armor per long rest with 1st-tier spell rider; effect persists until destroyed or re-forged |
| **Sapper** (#13) | Field Scanner | Bonus action pulse reveals traps/secret doors within 30 ft through 1 ft walls; marked hazards visible to allies 1 minute |
| **Sapper** (#13) | Tripwire Arsenal | Deploy two tripwires per short rest; triggered traps apply effect in 10 ft radius and grant one Demolition Pack charge (max 3) |

### 3. Continuity quick scan

[`CONTINUITY_REPORT.md`](../../src/data/CONTINUITY_REPORT.md) — wave 29 stamp appended; P0/P1 clear; no new P2 blockers.

### 4. Build

```bash
npx tsc --noEmit   # exit 0 (~7s)
```

---

## Files touched (wave 29)

- `src/data/class-draft-levels.js` — Soldier L11/L16, Mirrorsage L11, Shaman L16, Tinker L15 enrichments
- `src/data/prestige-lorebook.json` — Forge Master Relic Imbuement, Sapper Field Scanner/Tripwire Arsenal hallmarks
- `src/data/CONTINUITY_REPORT.md` — wave 29 continuity stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–29
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 29 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 29 append

---

## Wave 29b — GeneratorsPanel spark copy + clear (2026-07-30)

**Protocol:** No commits; append progress only.

### 1. GeneratorsPanel — last spark polish

| Surface | Change |
|---------|--------|
| **Last spark tracking** | Hook, POI, haven, people, and loot generators set `lastSpark` on roll |
| **Copy last spark** | Clipboard button when any spark is active — copies most recent result only |
| **Clear sparks** | Clears accumulated site sparks + loot; resets lore tags and `lastSpark` |

Toolbar sits below tier picker so loot-only rolls still expose copy/clear.

### 2. Typecheck

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 29b)

- `src/components/GeneratorsPanel.tsx` — `lastSpark`, copy/clear spark toolbar
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 29b section

---

## Wave 30 — class draft + prestige hallmark enrichments (2026-07-30)

**Protocol:** No commits; append progress only.

### 1. Class draft level enrichment (5 thin entries)

Wave 29 cleared Soldier L11/L16, Mirrorsage L11, Shaman L16, Tinker L15. This wave targets the five shortest remaining non-ASI stubs flagged at wave 29 close:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Soldier** | 18 | Formation Lock extends to 5-tile radius — allies in zone gain +2 AC and cannot be moved against their will; enemies lose one movement action; Palisade deploys inside zone cost no action (once/encounter) |
| **Mirrorsage** | 16 | Mirror Beast second shift per fight — change form once/encounter without Focus; second shift retains Echo Slot hold on prior form's last witnessed spell |
| **Tinker** | 18 | Anacite Drone second upgrade module — two concurrent modules; free module switch once/turn; shared HP pool with +2 destruction threshold |
| **Crimson Agent** | 16 | Veinweave mastery — three concurrent charges; spending on Sneak Attack/Blood Mark no longer ends Stealth stance; refresh one charge when Blood Marked target drops to 0 HP (once/encounter) |
| **Crimson Agent** | 18 | Blood Mark detonation chains — Marked foe at 0 HP splashes half Sneak Attack dice to nearest enemy within 15 ft; chain preserves mark duration (once/encounter) |

All five retain `draft: true`.

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

**Protocol:** No commits; append progress only.

### 1. Class draft level enrichment (5 thin entries)

Wave 30 cleared Soldier L18, Mirrorsage L16, Tinker L18, Crimson Agent L16/L18. This wave targets the five shortest remaining non-ASI stubs:

| Class | Level | Enrichment |
|-------|-------|------------|
| **Tinker** | 11 | Flask/bomb capacity +1 — maintain four concurrent flasks or bombs; Dual Drone Protocols fields two Anacite Drones concurrently with independent module slots (shared deploy action economy once/turn) |
| **Soldier** | 13 | Second palisade deploy per encounter — Palisade Tier II grants +3 AC (was +2) and 15 HP threshold before destruction; deploying both palisades links them — allies moving between linked segments ignore difficult terrain |
| **Soldier** | 17 | Overwatch Advance — after a successful Overwatch reaction shot, shift 1 tile without provoking opportunity attacks; Palisade allies in your new tile gain half cover until start of your next turn |
| **Dragoon** | 18 | Dragonflight range doubled once per short rest — Wyvern's Flow leap-attacks and Apex Assault may extend to double normal range; first leap each encounter ignores opportunity attacks |
| **Monk** | 18 | Diamond Soul — advantage on all saves while unarmored and not wielding a shield; when you succeed on a save you would have failed, regain 1 Ki (once/encounter) |

All five retain `draft: true`.

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 31 append

---

## Wave 32 — class draft clearance + prestige hallmark enrichments (2026-07-30)

**Protocol:** No commits; append progress only.

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 32 append

---

## Wave 33a — prestige hallmark enrichments (2026-07-30)

**Protocol:** No commits; append progress only.

### 1. Prestige hallmark enrichment (12 thin entries — pool cleared)

Re-read `prestige-lorebook.json` before write; sibling had already enriched Hexblade Hex Mark, Storm Lord Stormstep, Verdant Animist Wild Synergy, and others. **12** hallmarks remained under 80 chars — all enriched this wave (priority trio first, then next shortest):

| Prestige | Hallmark | Notes |
|----------|----------|-------|
| **Bloodbound** (#4) | Crimson Domination | Priority — blood-scent charm/dominate thrall with Intimidation advantage vs. allies |
| **Giant Killer** (#9) | Hunter's Mark | Priority — Large+ mark with crit range and tier-scaled damage |
| **Wyrmslayer** (#18) | Fearless Roar | Priority — fear immunity + ally save/resistance aura |
| **Mooncursed** (#12) | Lycan Form | Form-specific bonuses (werewolf/werebear/wererat) + Curse Surge hybrid tail |
| **Battlemage** (#1) | Momentum Surge | Stack spend for force or action-cost reduction; concentration loss clears Momentum |
| **Beastmaster** (#2) | Pack Coordination | Multi-companion bonus-action command + Pack Tactics advantage |
| **Blademaster** (#3) | Precision Flow | Crit DC chain + Parry Counter reset on third crit |
| **Wyrmslayer** (#18) | Scalebreaker Technique | AC sunder vs. dragon-kin + Vulnerable rider |
| **Berserker** (#5) | Frenzy | Tier-scaled rage damage, damage resistance, Stagger immunity |
| **Giant Killer** (#9) | Anchor Chain | Rune-harpoon tether grounding Large+ flyers |
| **Wyrmslayer** (#18) | Draconic Lore Mastery | Free-action wyrm ID + first-attack advantage |
| **Bloodbound** (#4) | Mistform | 0 HP mist escape, teleport, stabilize at 1 HP |

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

- `src/data/prestige-lorebook.json` — 12 hallmark enrichments (Bloodbound×2, Giant Killer×2, Wyrmslayer×3, Mooncursed, Battlemage, Beastmaster, Blademaster, Berserker)
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 33a section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 33a append

---

## Wave 33b — prestige hallmark enrichments (overnight worker, 2026-07-30)

**Protocol:** No commits; no mass deletion; append progress only. Aethel tone on thinnest unenriched hallmark lines. Skipped Bloodbound / Giant Killer / Wyrmslayer (reserved for sibling wave 33a).

### 1. Prestige hallmark enrichment (12 thin arrays)

Scanned `prestige-lorebook.json` — 24 hallmarks under 80 chars before this wave. Enriched 12 later-alphabet paths to avoid 33a collision:

| Prestige | Hallmark | Enrichment |
|----------|----------|------------|
| **Echomancer** (#7) | Echo Channel | Witness-and-copy enemy/monster ability for 2 rounds at your tier; Mirror Crystal required; once/short rest per unique ability |
| **Echomancer** (#7) | Reflected Pain | Caster takes psychic backlash = half spell damage taken (min tier floor); Mirror Pulse ready adds school-weakness rider |
| **Echomancer** (#7) | Reverb Core | Store one self-cast spell (max tier = half level); release next turn as bonus action at original tier, no somatic |
| **Forge Master** (#8) | Smith's Temper | Armor penalty −1 (min 0); +2 max durability; ignore first sunder/rust point each encounter |
| **Forge Master** (#8) | Forge Focus | 1-minute forge meditation restores all equipped gear; clears one minor curse or rust from a single piece |
| **Hexblade** (#11) | Hex Mark | Stacking Hex (max 3) on bound-weapon hits — tier floor necrotic per stack, −1 next save; 3-stack removal triggers capstone backlash |
| **Gravetouched** (#10) | Grim Grasp | Kills block revive/regen/undead raise 24h; corpse is desecrated ground; Bone Shield extends to allies' kills within 15 ft |
| **Soulrender** (#14) | Agony Lance | 60 ft necrotic beam + 2-round Agony DoT; −2 Con/Wis saves while DoT; costs 1 soul charge or slot |
| **Soulrender** (#14) | Spectral Ward | Spend 1–2 soul charges for ally temp HP (tier floor × charges) or redirect one hit to self at half damage |
| **Storm Lord** (#15) | Arc Surge | Chain lightning jumps within 15 ft; +tier floor per jump; Voltyros-aligned double-hit counts as two jumps |
| **Storm Lord** (#15) | Stormstep | Bonus action 30 ft dash to visible foe; path shockwave — tier floor d6 lightning, save or Dazed |
| **Verdant Animist** (#16) | Wild Synergy | +1 spell DC and conjuration damage per active seedling (max +3); Bloom Burst +5 ft radius per seedling |

Entrance/unlock blurbs unchanged — hallmarks were the thin target.

### 2. Remaining thin stub counts

| Pool | Before wave 33b | After |
|------|-----------------|-------|
| Prestige hallmarks (&lt;80 chars) | 24 | **12** |

Deferred (33a / later waves): Bloodbound Crimson Domination & Mistform, Giant Killer Hunter's Mark & Anchor Chain, Wyrmslayer Fearless Roar / Scalebreaker / Draconic Lore, Mooncursed Lycan Form, Battlemage Momentum Surge, Beastmaster Pack Coordination, Blademaster Precision Flow, Berserker Frenzy.

---

## Files touched (wave 33b)

- `src/data/prestige-lorebook.json` — Echomancer (Echo Channel, Reflected Pain, Reverb Core), Forge Master (Smith's Temper, Forge Focus), Hexblade Hex Mark, Gravetouched Grim Grasp, Soulrender (Agony Lance, Spectral Ward), Storm Lord (Arc Surge, Stormstep), Verdant Animist Wild Synergy hallmarks
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 33b section

---

## Wave 34 — thin-depth closure + Oracle Tier I + coffee refresh (2026-07-30)

**Protocol:** No commits; no mass deletion; append progress only.

### 1. Thin-depth milestone confirmed

| Pool | Status |
|------|--------|
| Class draft (non-ASI, &lt;70 chars) | **0** |
| Prestige hallmarks (&lt;80 chars) | **0** |
| ASI placeholders (&lt;70 chars) | 34 (expected) |

### 2. Oracle mystery Tier I enrichment (3 thin options)

| Mystery | Revelation |
|---------|------------|
| **Bones** | Marrow Drain — 2d6 necrotic touch-heal; undead +50% and HP regen blocked |
| **Shadow** | Shadow Step — silent teleport; +25% concealment attack bonus |
| **Stars** | Guiding Bolt — 2d6 radiant; star-mark ally buff |

### 3. Coffee review refresh

Downgraded prestige hallmarks; elevated Oracle full trees, Paladin revelations, L11–20 author review, Umbrin lore promote, Resonance multiclass draft.

### 4. Build

```bash
npm run build   # exit 0
```

---

## Files touched (wave 34)

- `src/data/oracle-mysteries.js` — Bones/Shadow/Stars Tier I enrichments
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–34
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 34 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list + wave 34 append
- `src/data/CONTINUITY_REPORT.md` — wave 34 continuity stamp

---

## Wave 34b — Paladin L5 oath revelation enrichment (overnight worker, 2026-07-30)

**Protocol:** No commits; append progress only. `draft: true` retained on all draft oaths.

### 1. Paladin draft oath L5 spot-check (4 vs Mercy template)

Mercy baseline: L5 revelation with aura-tied ally benefit (`Ward of Shelter — allies +2 DR, resist fear`).

| Oath | L5 revelation | Change |
|------|---------------|--------|
| **Ancients** | Primal Ward | Allies in aura gain resistance to one elemental type (choose at cast); fey/elementals −1 on saves vs. smites while ward persists |
| **Flame** | Zealot's Flame | +1d6 fire on ignited attacks; purge one disease from self on hit; undead in aura take 1d6 radiant each turn |
| **Grief** | Last Rites | Touch or 30 ft stabilize; +2 death saves and necrotic resistance 1 hour; undead within 10 ft save or turned |
| **Martyr King** | Royal Decree | 30-ft command — failed Wis save kneels or moves toward you; allies in aura +1 morale saves until end of next turn |

All four oaths retain `draft: true`. Five other draft oaths (Vengeance, Dominion, Silence, Chain, Chains Broken) already at Mercy-parity L5 depth — deferred.

**Enriched count:** 4

### 2. Typecheck

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 34b)

- `src/data/paladin-oaths.js` — Ancients / Flame / Grief / Martyr King L5 revelation enrichment
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 34b section

---

## Wave 35b — continuity stamp (2026-07-30)

**Protocol:** No commits; append progress only. Continuity re-scan post wave 34b; no content edits.

### 1. Continuity re-scan (post wave 34b)

| Target | Result |
|--------|--------|
| **Umbrin / no Drow-Lolth IP** | **Pass** — product path clean; legacy migration in `character-storage.js` only |
| **Hybrid-B in player UI** | **Pass** — internal docs / `resonance-economy.js` header only |
| **Wave 34b surfaces** | **Pass** — Paladin Ancients/Flame/Grief/Martyr King L5 revelations enriched; all retain `draft: true` |
| **17 classes / Bloodbound / Oracle RC** | **Pass** — unchanged |
| **Build** | `npx tsc --noEmit` **exit 0** (~9s) |

**Verdict:** **Green** — P0/P1 clear; no new P2 blockers.

### 2. ASI placeholder clarification (`class-draft-levels.js`)

**34** entries labeled "Ability Score Improvement" (typically L14 + L19 per class) are **intentional** ability score increase placeholders — standard milestone rows, **not** thin-content debt and **not** enrichment targets. Non-ASI stub count remains **0**.

| Pool | Count | Status |
|------|-------|--------|
| Class draft (non-ASI, &lt;70 chars) | **0** | Cleared (wave 32) |
| Prestige hallmarks (&lt;80 chars) | **0** | Cleared (waves 33a/33b) |
| ASI placeholders (&lt;70 chars) | **34** | **Expected — intentional ASI rows** |

---

## Files touched (wave 35b)

- `src/data/CONTINUITY_REPORT.md` — wave 35 continuity stamp + gate status line
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 35b section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 35b append

---

## Wave 35c — author draft enrichments (Oracle Tier I + Paladin L9) (2026-07-30)

**Protocol:** No commits; append progress only. `draft: true` retained on all draft mysteries and oaths.

### 1. Oracle mystery Tier I enrichment (6 thin options)

Depth scan (`tools/oracle_tier1_lengths.py`) — six thinnest Tier I siblings enriched to Ancestor/Battle depth:

| Mystery | Revelation | Change |
|---------|------------|--------|
| **Battle** | Vanguard's Step | Move without provoking + ally DR + opportunity attack advantage |
| **Cataclysm** | Gale of Unmaking | 1d6 bludgeoning wind line, push, movement penalty, debris terrain |
| **Life** | Thorned Shelter | AC/DR/healing buff + thorn retaliation on first melee attacker |
| **Stars** | Fate's Glimpse | Ally reroll +2; oracle gains Revelation save advantage on success |
| **Stars** | Clarity | Condition cleanse + saves + reveal shapeshifted/invisible nearby |
| **Time** | Moment's Pause | Action loss + initiative penalty + reaction lock on failed save |

**Enriched count:** 6 (9 cumulative with wave 34: Marrow Drain, Shadow Step, Guiding Bolt).

### 2. Paladin draft oath L9 enrichment (3 vs Mercy template)

Mercy baseline L9: `Channel Life — transfer HP from self to ally` (44 chars).

| Oath | L9 revelation | Change |
|------|---------------|--------|
| **Grief** | Memorial Flame | 30-ft light; reveal undead; +2 death saves; undead disadvantage on attacks |
| **Dominion** | Law's Weight | 20-ft zone; lawbreakers save or slow, −2 AC, no haste/dash |
| **Ancients** | Echo of Ages | Aura advantage vs charm/frightened; fey/elementals hesitate on failed Wis save |

All retain `draft: true`. Five other draft oaths at or above Mercy L9 depth — deferred.

**Enriched count:** 3

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 35c)

- `src/data/oracle-mysteries.js` — 6 Tier I revelation enrichments
- `src/data/paladin-oaths.js` — Grief / Dominion / Ancients L9 revelation enrichment
- `tools/oracle_tier1_lengths.py` — new depth scan helper
- `tools/paladin_l9_lengths.py` — new L9 length scan helper
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–35c checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 35c section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list + wave 35c append

---

## Wave 36b — continuity stamp + build (2026-07-30)

**Protocol:** No commits; append progress only. Continuity re-scan post wave 35c; no content edits.

### 1. Continuity re-scan (post wave 35c)

| Target | Result |
|--------|--------|
| **Umbrin / no Drow-Lolth IP** | **Pass** — product path clean; legacy migration in `character-storage.js` only |
| **Hybrid-B in player UI** | **Pass** — internal docs / `resonance-economy.js` header only |
| **Wave 35c surfaces** | **Pass** — Oracle 6 Tier I + Paladin Grief/Dominion/Ancients L9 enriched; all retain `draft: true` |
| **17 classes / Bloodbound / Oracle RC** | **Pass** — unchanged |
| **Thin-depth debt** | **Pass** — class drafts **0** non-ASI stubs; prestige hallmarks **0** under 80 chars; **34 ASI placeholders** intentional |

**Verdict:** **Green** — P0/P1 clear; no new P2 blockers.

### 2. Build

```bash
npm run build   # exit 0 (~71s)
```

---

## Files touched (wave 36b)

- `src/data/CONTINUITY_REPORT.md` — wave 36 continuity stamp + gate status line
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 36b section

---

## Wave 36 — Oracle Tier I thin batch (2026-07-30)

**Protocol:** No commits; append progress only. `draft: true` retained on all draft mysteries.

### 1. Oracle mystery Tier I enrichment (9 thin options)

Depth scan (`tools/oracle_tier1_lengths.py`) — nine thinnest remaining Tier I siblings (≤126 chars) enriched to Ancestor/Battle depth:

| Mystery | Revelation | Change |
|---------|------------|--------|
| **Dream** | Slumber Glimpse | Action loss + initiative/reaction penalties; +2 to hit on next attack vs target |
| **Flame** | Purging Flame | 1d8 + CHA heal; undead equal fire + ash debuff on failed save |
| **Time** | Echo Strike | Weapon/touch echo at half damage; RC refund on echo dropping below half HP |
| **Shadow** | Fear's Whisper | Fear + reaction lock + ally crit bonus vs feared |
| **Battle** | Host's Cry | Damage/DR buff + ally kill heal + RC refund during cry |
| **Cataclysm** | Shardburst | 1d6 bludgeoning burst with range, movement penalty, wall-prone rider |
| **Life** | Overflowing Light | 2d6 + CHA heal; temp HP overflow; condition cleanse on fade |
| **Life** | Resonant Seed | Zone heal/condition cleanse + undead radiant/movement penalty |
| **Shadow** | Psychic Lash | 1d8 + CHA psychic; concealment riders + Dread + reaction lock |

**Enriched count:** 9 (18 cumulative with waves 34 + 35c). **Remaining:** 0 at ≤126 chars; 9 mid-tier (133–168 chars).

### 2. Paladin draft oath L9 enrichment

Mercy baseline L9: 44 chars. **0** draft oaths below Mercy depth — no changes.

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 36)

- `src/data/oracle-mysteries.js` — 9 Tier I enrichments
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–36 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 36 append

---

## Wave 37 — Oracle Tier I mid-tier batch (2026-07-30)

**Protocol:** No commits; append progress only. `draft: true` retained on all draft mysteries.

### 1. Oracle mystery Tier I enrichment (9 mid-tier options)

Depth scan (`tools/oracle_tier1_lengths.py`) — nine remaining mid-tier Tier I siblings (133–168 chars) enriched to Ancestor/Battle depth:

| Mystery | Revelation | Change |
|---------|------------|--------|
| **Time** | Borrowed Beat | Move 2 tiles or Tier I Revelation before next enemy; no provoke; +2 initiative both |
| **Battle** | Mark of the Doomed | Crit rider +1d6; mark strips concealment |
| **Bones** | Ashen Shroud | Necrotic resist + fear debuff; anti-raise corpses on fade |
| **Cataclysm** | Fault Line | 1d4 bludgeoning + wall-prone; structure crack rider |
| **Dream** | Mirage | Failed save strikes mirage; duplicate free move 1 tile/round |
| **Bones** | Bone Whisper | Active truth + undead save-or-stun via Pale Ledger |
| **Dream** | False Memory | Failed save initiative/reaction penalties + +2 to hit rider |
| **Flame** | Passion's Rush | 1d6 fire line + movement penalty; ally damage/DR buff |
| **Flame** | Wrathful Brand | Ally heal + target save-or-hit debuff from embers |

**Enriched count:** 9 (27 cumulative — **complete**). **Remaining:** 0 at ≤126 chars; 0 mid-tier (133–168 chars).

### 2. Paladin draft oath L9 enrichment

Mercy baseline L9: 44 chars. **0** draft oaths below Mercy depth — no changes.

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 37)

- `src/data/oracle-mysteries.js` — 9 Tier I mid-tier enrichments
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–37 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 37 append

---

## Wave 38b — continuity stamp (2026-07-30)

**Protocol:** No commits; append progress only. Continuity re-scan post wave 37; no content edits.

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

### 2. Coffee review refresh (`OVERNIGHT_HANDOFF.md`)

Oracle Tier I depth pass **27/27 complete**; Tier II/III still **author-draft review** — coffee list intro + row #1 updated; opening brief unchanged.

---

## Files touched (wave 38b)

- `src/data/CONTINUITY_REPORT.md` — wave 38 continuity stamp + gate status line
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 38b section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + wave 38b append

---

## Wave 38 — Oracle Tier II thin batch (2026-07-30)

**Protocol:** No commits; append progress only. `draft: true` retained on all draft mysteries.

### 1. Oracle mystery Tier II enrichment (9 thin options)

Depth scan (`tools/oracle_tier2_lengths.py`) — thinnest Tier II sibling per draft mystery (≤130 chars) enriched to Ancestor Spirit Walk / Echo Armor depth:

| Mystery | Revelation | Change |
|---------|------------|--------|
| **Battle** | Divine Fury | 2-round fury; crit Fear rider; bonus-action second attack |
| **Bones** | Ledger's Command | Commanded undead +10% damage, +5% DR, intercept rider |
| **Cataclysm** | Storm Crown | 2d6 per turn; save-or-hit debuff; ally storm protections |
| **Dream** | Unreality | Vanish-on-hit once/short rest + Dread rider |
| **Flame** | Undying Ember | 2d6 adjacent fire; ally heal scatter |
| **Life** | Verdant Pulse | Healing received buff; combat stabilize pulse |
| **Shadow** | Mind Spike | 2d8 + CHA; Dread; feared-target RC refund |
| **Stars** | Constellation Mark | +2 to hit; crit radiant + concealment reveal |
| **Time** | Paradox Skin | Slow resist; ally time/aging save absorb |

**Enriched count:** 9 (9/27 cumulative). **Remaining thin:** **5** at ≤130 chars.

### 2. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 38)

- `src/data/oracle-mysteries.js` — 9 Tier II enrichments
- `tools/oracle_tier2_lengths.py` — Tier II depth scan helper (new)
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–38 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 38 append

---

## Wave 39 — Oracle Tier II thin debt cleared + Tier III start (2026-07-30)

**Protocol:** No commits; append progress only. `draft: true` retained on all draft mysteries.

### 1. Oracle mystery Tier II enrichment (5 remaining thin options)

Final ≤130-char batch — Radiant Path, Rotting Touch, Field Command, Night's Embrace, Nightmare Lash enriched to Ancestor Spirit Walk / Echo Armor depth.

**Enriched count:** 14 (14/27 cumulative). **Remaining thin:** **0** at ≤130 chars.

### 2. Oracle mystery Tier III enrichment (5 shortest options)

Pre-wave scan: **0 thin at ≤130**. Enriched five shortest capstones (Concord Alignment, Song of Mending, Hush Descends, Threshold Collapse, First Flame Convergence).

**Enriched count:** 5 (5/9 cumulative). **Remaining thin:** **0** at ≤130 chars; **4** remain for author tone pass.

### 3. Build

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 39)

- `src/data/oracle-mysteries.js` — 5 Tier II + 5 Tier III enrichments
- `tools/oracle_tier3_lengths.py` — Tier III depth scan helper (new)
- `src/data/CONTINUITY_REPORT.md` — wave 39 stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–39
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 39 append

---

## Wave 40 — Oracle Tier III complete + Tier II mid-tier batch (2026-07-30)

**Protocol:** No commits; append progress only. `draft: true` retained on all draft mysteries.

### 1. Oracle mystery Tier III enrichment (4 remaining capstones)

Final batch — Fury of the Host, Unfinished Chorus, Spiral Convergence, Seal's Fracture enriched to Bloodline Convergence / First Flame Convergence depth.

**Enriched count:** 9 (9/9 cumulative — **complete**). **Remaining thin:** **0** at ≤130 chars.

### 2. Oracle mystery Tier II enrichment (5 mid-tier options)

Post-thin scan — five shortest remaining draft Tier II options (132–136 chars pre-wave) enriched to Ancestor Spirit Walk / Echo Armor depth: Crown's Burn, Death's Threshold, Garden of Restoration, Upheaval, Temporal Rift.

**Enriched count:** 19 (19/27 cumulative). **Remaining thin:** **0** at ≤130 chars; **8** mid-tier options remain (139–160 chars).

### 3. Build

```bash
npm run build   # exit 0
```

---

## Files touched (wave 40)

- `src/data/oracle-mysteries.js` — 5 Tier II + 4 Tier III enrichments
- `src/data/CONTINUITY_REPORT.md` — wave 40 stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–40
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 40 append

---

## Wave 41 — Oracle Tier II mid-tier complete (2026-07-30)

**Protocol:** No commits; append progress only. `draft: true` retained on all draft mysteries.

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
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + wave 41 append

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
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 42 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + this wave 42 append

---

## Wave 42b — continuity stamp + build (2026-07-30)

**Protocol:** No commits; append progress only. Continuity re-scan post wave 42; no content edits.

### 1. Continuity re-scan (post wave 42)

| Target | Result |
|--------|--------|
| **Umbrin / no Drow-Lolth IP** | **Pass** — product path clean; legacy migration in `character-storage.js` only |
| **Hybrid-B in player UI** | **Pass** — internal docs / `resonance-economy.js` header only |
| **Wave 42 surfaces** | **Pass** — Paladin 8 L13/L17 revelation enrichments + 2 `finalOathGift`; all retain `draft: true` |
| **17 classes / Bloodbound / Oracle RC** | **Pass** — unchanged |
| **Thin-depth debt** | **Pass** — class drafts **0** non-ASI stubs; prestige hallmarks **0** under 80 chars; **34 ASI placeholders** intentional |

**Verdict:** **Green** — P0/P1 clear; no new P2 blockers.

### 2. Build

```bash
npm run build   # exit 0 (~54s)
```

---

## Files touched (wave 42b)

- `src/data/CONTINUITY_REPORT.md` — wave 42 continuity stamp + gate status line
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 42b section

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

All retain `draft: true`. **Running total:** **0** draft L13/L17 below Mercy depth; **0** below enriched tier (131 chars).

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

Mercy retains `finalOathGiftDraft: true`. **Running total:** **10/10** gifts at depth (226–304 chars).

### 3. UMBRIN_LORE.md clarity polish

Light copy pass — clearer section headers, tightened prose, removed EverQuest reference (replaced with generic archetype note). No new cosmology; Obsidian Burn / Umbra cult / Choir orthodoxy unchanged.

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — coffee list refresh + wave 43 append

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 44 append (opening/coffee untouched)

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

Path A step 5 expanded: L1 revelation block, Patron/Prophecy trigger, Tier I charge costs at L3, optional L1 unlock hint check.

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

## Wave 46b — COLLABORATOR_DAY1 refresh (2026-07-30)

**Worker:** Overnight wave 46b  
**Commit:** none (per owner request)

Refreshed [`COLLABORATOR_DAY1.md`](./COLLABORATOR_DAY1.md) for new helpers: **Umbrin** product race, **Resonance** (not Hybrid-B in UI), Oracle **Paths + RC** vs Weave **RP**, **playtest smoke** pass criteria, **draft flags**, **Director OK gate**, **OVERNIGHT_HANDOFF** pointer for morning owner.

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

**Running totals:** **5/10** enriched; **5 remain** under 100 chars (Shaman L20, Dragoon L20, Mirrorsage L19, Thief L20, Soldier L20 — 75–83 chars, L19–20 capstones). All retain `draft: true`. Oracle + Paladin depth passes **complete** (draft for author).

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

## Wave 48b — Druid hero/arch form trait enrichments (2026-07-30)

**Worker:** Overnight wave 48b  
**Commit:** none (per owner request)

### 1. Druid shapeshifting trait enrichment (3 stubbiest lines)

Scanned `druid-shapeshifting.js` hero + arch forms — three shortest trait lines (13 chars each) enriched with Aethel tone; no `draft` flags added (forms were not draft).

| Form | Tier | Trait | Change |
|------|------|-------|--------|
| **Sky Serpent** | Arch (L11–20) | Flight 80 ft. | Sky Coil Flight — Weave updrafts between descent tiers; hover without losing reactions |
| **Tempest Raptor** | Hero (Circle of the Storm) | Flight 60 ft. | Stormwing Flight — Circle storm-blood lift; advantage on wind/lightning saves while airborne |
| **Frost Wyrmling** | Hero (Circle of Winterfang) | Cold immunity | Rimeheart Immunity — cold immune; breath/claw frost ignore resistance once per target per transformation |

### 2. Typecheck

```bash
npx tsc --noEmit
```

---

## Files touched (wave 48b)

- `src/data/druid-shapeshifting.js` — Sky Serpent, Tempest Raptor, Frost Wyrmling trait enrichments
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 48b section

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

Refreshed [`OVERNIGHT_HANDOFF.md`](./OVERNIGHT_HANDOFF.md) opening status bar + coffee section and [`OVERNIGHT_STATUS_MIDNIGHT.md`](./OVERNIGHT_STATUS_MIDNIGHT.md) for waves **1–48**:

| Item | Status |
|------|--------|
| Oracle revelations | All tiers + L12/18/20 depth **complete** — draft for author tone review |
| Paladin oaths | L3–L20 depth **complete** — draft for author tone review |
| Class-draft non-ASI | **0 thin** (waves 46–47; 10/10 enriched) |
| Prestige hallmarks | **0 thin** (waves 33a/33b) |
| Umbrin / Resonance / 17 classes | Locked; product-path clean |
| P0 / P1 | **0 / 0** |
| Build | **`npm run build` green** |

**Coffee primary:** author tone review Oracle/Paladin/Umbrin; **secondary:** L11–20 author tables.

---

## Files touched (wave 48)

- `src/data/CONTINUITY_REPORT.md` — wave 48 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–48 checkpoint
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — opening status bar + coffee refresh
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 48 section

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 49 append (opening/coffee untouched)

---

## Wave 49b — SessionTracker rest tip (2026-07-30)

**Worker:** Overnight wave 49b  
**Commit:** none (per owner request)

### 1. Rest economy one-liner (Party Resonance)

Party Resonance already had a short rest tip; refined to match per-row **Retune** / **Full** labels and Oracle RC wording:

| Control | Effect |
|---------|--------|
| **Retune** (short) | ¼ max RP (Weave casters) |
| **Full** (long) | Restore Resonance to max |
| **Oracle** | RC +1 on short · full RC on long |
| **Long rest** | Also +8h on horn clock |

### 2. Typecheck

```bash
npx tsc --noEmit
```

---

## Files touched (wave 49b)

- `src/components/SessionTracker.tsx` — rest tip Retune/Full + Oracle RC clarity
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 49b section

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 50a append (opening/coffee untouched)

---

## Wave 50b — Druid hero/arch trait enrichments (2026-07-30)

**Worker:** Overnight wave 50b  
**Commit:** none (per owner request)

### 1. Druid shapeshifting trait enrichment (9 mid-list hero/arch lines)

Scanned `druid-shapeshifting.js` hero + arch forms — skipped shortest stub (**Dire Wolf · Bite: 2d6 piercing**, reserved for sibling 50a); enriched nine mid-list lines with Aethel/circle tone:

| Form | Tier | Trait | Change |
|------|------|-------|--------|
| **Earth Warden** | Arch (L11–20) | Stone Resistance: resist nonmagical B/P/S | earth-warden hide drinks tier-stone impacts like riverbed gravel |
| **Shadow Lynx** | Arch (L11–20) | Blink (reaction): teleport 30 ft. when hit | Shadow Blink — arch lynx dissolves into tier-shadow; muffled footfalls |
| **Mooncursed** | Hero (Circle of the Moon) | Lunar Rage: +1d8 damage under full moon | Moon-circle blood howls; silvered foes still resist as normal |
| **Tempest Raptor** | Hero (Circle of the Storm) | Lightning Claw: 2d6 lightning | Stormtalon Claw — storm-blood arcs; wet targets +1d4 lightning once/transformation |
| **Thunderhorn Stag** | Hero (Circle of the Storm) | Charge: 2d8 thunder + Con save or deafened | Thunder Charge — storm-circle horns crack the air; deafened foes can't hear ally calls |
| **Snow Leopard** | Hero (Circle of Winterfang) | Frost Walk: ignore ice/snow penalties | Winterfang pads grip glacier stone; never slip on rime or slush |
| **Carrion Rat King** | Hero (Circle of the Rotshaper) | Immune to disease and poisoned | Rotshaper Immunity — carrion crown tolerates Aethel blight and venom |
| **Insect Broodmother** | Hero (Circle of the Rotshaper) | Spawn 1d4 insect swarms on transform | Brood Burst — hatchlings pour from decay-tier burrows at your feet |
| **Blazewood Stag** | Hero (Circle of the Ashen Grove) | Burning Charge: +2d6 fire on horn charge | Ashen Grove embers trail the antlers through smoke and ash |

**Running totals:** **17/42** hero/arch traits enriched (waves 48b–50b); **30 remain** under 60 chars (39 → 30 this wave).

### 2. Typecheck

```bash
npx tsc --noEmit   # exit 0 (~8s)
```

---

## Files touched (wave 50b)

- `src/data/druid-shapeshifting.js` — 9 hero/arch trait enrichments
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 50b section

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 51 append

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — opening/coffee refresh + wave 52 append
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–52 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 52 section

---

## Wave 52b — Druid base-form trait enrichments (2026-07-30)

**Worker:** Overnight wave 52b  
**Commit:** none (per owner request)

### 1. Druid shapeshifting trait enrichment (5 stubbiest base-form lines)

Scanned `druid-shapeshifting.js` **BASE_DRUID_FORMS** — skipped hero/arch (complete per wave 51); enriched five shortest base trait lines with Aethel/wild tone:

| Form | Tier | Trait | Change |
|------|------|-------|--------|
| **Panther Form** | Base (L1–10) | +4 Stealth | Shadow Pelt — panther-form fur drinks light along tier-shadow and moonlit stone |
| **Hawk Form** | Base (L1–10) | Flight 60 ft. | Hawkwing Flight — base hawk form rides Weave updrafts between Aethel descent ledges |
| **Panther Form** | Base (L1–10) | 60 ft. darkvision | Night Eyes — panther-form sight pierces undercroft gloom without torchlight |
| **Bear Form** | Base (L1–10) | +20 HP temporary buffer | Thick Hide Buffer — bear-form bulk absorbs blows like tier-rooted oak against wild impacts |
| **Wolf Form** | Base (L1–10) | +10 ft. movement speed | Pack Pace — wolf-form stride cuts Aethel wild undergrowth and lower-tier trails |

**Running totals:** **5/14** base traits enriched (wave 52b); **9 remain** under 60 chars.

### 2. Typecheck

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 52b)

- `src/data/druid-shapeshifting.js` — 5 base-form trait enrichments
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 52b section

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 53 append

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 54 append

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — opening/coffee refresh + wave 55 append
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–55 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 55 section

---

## Wave 55b — Prestige unlock/entrance blurbs (3 shortest) (2026-07-30)

**Worker:** Overnight wave 55b  
**Commit:** none (per owner request)

### 1. Prestige unlock/entrance enrichment (3 shortest unlock strings)

Scanned `prestige-lorebook.json` — three shortest unlock/entrance blurbs enriched with Aethel tone; both fields updated per path:

| Path | Original (chars) | Change |
|------|------------------|--------|
| **Blademaster** (#3) | Defeat a master duelist without taking more than one hit. (57) | Aethel trial ring; Weave reads clean parry cadence as Blademaster proof |
| **Berserker** (#5) | Enter a berserker state and defeat 10 foes solo during a ritual combat trial. (77) | Ritual combat Frenzy along Aethel descent tiers; ten solo kills; unbroken rage proof |
| **Wyrmslayer** (#18) | Slay a CR+3 dragon or greater wyrm with a weapon you forged or modified personally. (83) | Personal wyrmslayer steel; CR+3 dragon kill across Aethel descent tiers; scaled-blood oath |

**Running totals:** **3/18** unlock/entrance blurbs enriched; **15 remain** (next shortest: Hexblade #11 at 84 chars).

### 2. Typecheck

```bash
npx tsc --noEmit   # exit 0
```

---

## Files touched (wave 55b)

- `src/data/prestige-lorebook.json` — 3 unlock/entrance enrichments (Blademaster, Berserker, Wyrmslayer)
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 55b section

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
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 60 append

---

## Wave 61 — Class-draft L11–20 gaps + Overcast Burnout hint stub (2026-07-30)

**Worker:** Overnight wave 61  
**Commit:** none (per owner request)

### 1. Class-draft L11–20 gap fill (Mirrorsage / Mage / Bard)

Filled missing non-ASI draft milestones (all retain `draft: true`; scan **0 thin** under 100 chars):

| Class | Levels | Milestone |
|-------|--------|-----------|
| **Mirrorsage** | L13 | Witnessed Cadence — echoed release chains RP discount; shift-safe |
| **Mirrorsage** | L15 | Mirror Lattice — one witnessed spell per school; school swap shift-safe |
| **Mirrorsage** | L17 | Adaptive Resonance — witnessed-school echo discount + opposition ignore |
| **Mage** | L16 | Arcane Bulwark — concentration save below half pool regains 1d4 RP |
| **Bard** | L13 | Versatile Performance mastery — Crescendo skills + Counter-Melody range |
| **Bard** | L15 | Inspiring Leader cadence — 2+ Crescendo spend grants temp HP aura |
| **Bard** | L17 | Legendary refrain — Hero Path verse as reaction on ally failed save |

**Note:** Wizard L11/13/15/17/20 remain rulebook canon in `class-details.js` (tier bands); draft file covers ASI + enriched L16/L18 only.

### 2. Overcast Burnout trigger stub (Mage L17 draft)

| Surface | Change |
|---------|--------|
| **`resonance-economy.js`** | `overcastBurnoutHintAfterCast()` — post-cast RP &lt; 25% max and/or Mage L17+ T8+ overcast → concentration DC 15 + tier hint |
| **SessionTracker** | **Apply cast spend** sets `burnoutCastHint`; amber **Overcast check** line under RP row; clears on Overcast **Clear** |

### 3. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~11s)
npm run build      # exit 0 (~40s)
```

---

## Files touched (wave 61)

- `src/data/class-draft-levels.js` — Mirrorsage L13/L15/L17, Mage L16, Bard L13/L15/L17
- `src/data/resonance-economy.js` — `overcastBurnoutHintAfterCast()` helper
- `src/components/SessionTracker.tsx` — post-cast Burnout concentration hint UI
- `src/data/CONTINUITY_REPORT.md` — wave 61 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–61 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 61 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 61 append

---

## Wave 62 — Session Ethos picker + Druid L15 arch attunement badge (2026-07-30)

**Worker:** Overnight wave 62  
**Commit:** none (per owner request)

### 1. Session Ethos row picker (affinity smoke)

| Surface | Change |
|---------|--------|
| **`resonance-economy.js`** | `PLAYER_ALIGNMENTS` — nine ethos strings for Builder + Session |
| **SessionTracker** | Ally combatant row: compact LG/NG/…/CE pills; sets `alignment` at table for overcast affinity without re-adding from Builder; shows live −1/+1 RP hint when school selected |

### 2. Druid L15 arch-form attunement Session badge

| Surface | Change |
|---------|--------|
| **`druid-shapeshifting.js`** | `hasArchFormAttunement()`, `ARCH_ATTUNEMENT_MAX` (2), `isFreeArchAttunementSwap()` |
| **SessionTracker** | Wild Shape header badge **Arch attuned X/2** at L15+; Shift+click arch form buttons to pin attunement; swap between attuned forms while transformed skips use once/encounter (`archAttunementSwapUsed`; resets on short/long rest) |

### 3. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~13s)
npm run build      # exit 0 (~43s)
```

---

## Files touched (wave 62)

- `src/data/resonance-economy.js` — `PLAYER_ALIGNMENTS`
- `src/data/druid-shapeshifting.js` — arch attunement helpers
- `src/components/SessionTracker.tsx` — Ethos picker + arch attunement badge/UX
- `src/data/CONTINUITY_REPORT.md` — wave 62 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–62 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 62 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 62 append

---

## Wave 63 — PLAYTEST_SMOKE Burnout stretch + class-draft L13/L15/L17 gaps (2026-07-30)

**Worker:** Overnight wave 63  
**Commit:** none (per owner request)

### 1. PLAYTEST_SMOKE stretch (Burnout + Ethos + arch attunement)

| Surface | Change |
|---------|--------|
| **`PLAYTEST_SMOKE.md`** | Optional stretch rows: **Overcast Burnout hint** (Mage L17+ tier 8+, post-cast RP &lt; 25% → Overcast check line); **Ethos row** affinity smoke; **Druid arch attunement** L15 Shift+click one-liner |

### 2. Class-draft L11–20 gaps (Cleric / Monk / Ranger / Dragoon / Tinker)

| Class | Levels added |
|-------|--------------|
| **Cleric** | L13 (4th-level slots), L15 (Destroy Undead CR 3), L17 (Blessed Strikes) |
| **Monk** | L13 (Stance resonance), L15 (Ki Echo), L17 (Perfect Stillness) |
| **Ranger** | L13 (4th-level slots), L15 (Vanish), L17 (Feral Senses) |
| **Dragoon** | L13 (Momentum cap +1), L15 (Dragon's Eye mastery), L17 (Lancer's Apex foreshadow) |
| **Tinker** | L13 (Remote Detonation mastery), L17 (Overcharge protocol) — L15 already present |

All entries `draft: true` via `draftFeature()`; Aethel tone; aligned with existing class-path mechanics.

### 3. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~8s)
npm run build      # exit 0 (~40s)
```

---

## Files touched (wave 63)

- `src/data/class-draft-levels.js` — 14 new draft milestones (5 classes)
- `docs/mechanics/PLAYTEST_SMOKE.md` — Burnout + Ethos + arch attunement stretch rows
- `src/data/CONTINUITY_REPORT.md` — wave 63 stamp + status line
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — waves 1–63 checkpoint
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — wave 63 section
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 63 append

---

## Wave 64 — Shaman Session totem tracker + class-draft scan (2026-07-30)

**Worker:** Overnight wave 64 (retry)  
**Commit:** none (per owner request)

### 1. Session Shaman totem stub

| Surface | Change |
|---------|--------|
| **`SessionTracker.tsx`** | Shaman allies at L6+ can place/recall **Spirit**, **Echo**, **Divining**, or **Blight** totems. The control persists per Session combatant; long rest clears placements. |
| **Level gates** | L6 exposes one active totem (Totem Pulse source); L13 exposes two active slots with an explicit **draft** label. |
| **Scope boundary** | The tracker records presence only. Path effects, duration, targeting, damage, and pulse resolution remain GM/table-facing; nothing is promoted to canon. |

### 2. L11–20 class scan

**Paladin**, **Wizard**, and **Warrior** already have L13/L15/L17 entries in `class-details.js` (canon), so no duplicate `draft: true` features were added over rulebook content.

### 3. Build hygiene

```bash
npx tsc --noEmit   # exit 0 (~10s)
npm run build      # exit 0 (~41s)
```

---

## Files touched (wave 64)

- `src/components/SessionTracker.tsx` — persisted Shaman totem placement/recall stub
- `src/data/CONTINUITY_REPORT.md` — wave 64 continuity stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — wave 64 midnight append
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 64 append
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 64 append

---

## Wave 65 — Shaman smoke coverage + hero-form trait depth (2026-07-30)

**Worker:** Overnight wave 65  
**Commit:** none (per owner request)

### 1. Shaman tracker smoke path

| Surface | Change |
|---------|--------|
| **`PLAYTEST_SMOKE.md`** | Added an optional-stretch row for L6 place/recall, L13 two-slot placement and third-slot enforcement, plus long-rest clearing. |
| **Scope boundary** | The row repeats that Totem Pulse and all per-totem effects, duration, targeting, and damage remain table/GM-resolved. No effect automation was added. |

### 2. Hero-form trait depth

| Surface | Change |
|---------|--------|
| **`druid-shapeshifting.js`** | Enriched 13 previously concise hero-form traits: Moon (3), Storm (2), Thorns (3), Winterfang (3), and Rotshaper (2). |
| **Mechanics** | Existing numeric values, ranges, action economy, and effects are unchanged; additions provide only descriptive context for already-listed traits. |

### 3. Validation

```bash
npx tsc --noEmit   # exit 0 (~11s)
```

---

## Files touched (wave 65)

- `src/data/druid-shapeshifting.js` — 13 hero-form trait depth enrichments
- `docs/mechanics/PLAYTEST_SMOKE.md` — Shaman L6/L13 placement and recall smoke row
- `src/data/CONTINUITY_REPORT.md` — wave 65 continuity stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — wave 65 midnight append
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 65 append
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 65 append

---

## Wave 66 — Burnout recovery exits + Items Library no-results polish (2026-07-30)

**Worker:** Overnight wave 66  
**Commit:** none (per owner request)

### 1. Burnout cast-hint recovery

| Surface | Change |
|---------|--------|
| **`SessionTracker.tsx`** | Clears the transient `burnoutCastHint` during Short Rest, Long Rest, and direct **Full** Resonance restore. |
| **Existing Overcast control** | **Clear** already reset the hint; it remains unchanged and completes the four recovery exits. |
| **Scope boundary** | Burnout calculation, badge threshold, and draft consequence copy are untouched. No per-totem behavior was added. |

### 2. Items Library zero-results state

| Surface | Change |
|---------|--------|
| **`ItemsLibrary.tsx`** | Replaces the blank catalog column at zero matches with a tab-aware explanation and in-place **Clear all filters** action. |
| **Behavior** | Search/filter rules, item data, selected-item pane, and crafting flow are unchanged. |

### 3. Validation

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~47s)
```

---

## Files touched (wave 66)

- `src/components/SessionTracker.tsx` — Burnout cast-hint recovery exits
- `src/components/ItemsLibrary.tsx` — actionable no-results state
- `src/data/CONTINUITY_REPORT.md` — wave 66 continuity stamp
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — wave 66 midnight append
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 66 append
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 66 append

---

## Wave 67 — Session continuity glossary + library empty-state parity (2026-07-30)

**Worker:** Overnight wave 67  
**Commit:** none (per owner request)

### 1. Session persistence continuity

| Surface | Change |
|---------|--------|
| **`CONTINUITY_GLOSSARY.md`** | Added the Session tracker persistence table for `activeTotemIds`, `attunedArchFormIds`, `archAttunementSwapUsed`, `alignment` (Ethos row), and `burnoutCastHint`. |
| **Scope boundaries** | Totem placement remains table/GM-resolved; arch attunement and Burnout behavior retain their existing draft labels and recovery semantics. No totem effect automation or new rules were introduced. |
| **Library convention** | Documented that Clear all filters affects discovery controls only and does not erase learned/favorite spell state, item data, or Session data. |

### 2. Spells / Bestiary zero-results parity

| Surface | Change |
|---------|--------|
| **`SpellsLibrary.tsx`** | Zero-result cards now offer **Clear all filters**. It resets search, class/school/level filters, and the temporary All/Learned/Favorites view, without clearing the learned or favorite lists. |
| **`MonstersLibrary.tsx`** | Search now counts as an active filter for result metadata; zero-result cards offer **Clear all filters**, which resets the search plus every dropdown filter. |
| **Scope boundary** | Spell/monster data, card selection, favorites, and normal non-empty result rendering are unchanged. |

### 3. Validation

```bash
npx tsc --noEmit   # pending
npm run build      # pending
```

### Wave 78 validation update

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~46s)
```

### Wave 72 validation update

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~43s)
```

---

### Wave 70 validation update

`npx tsc --noEmit` **passed** (~8s) and `npm run build` **passed** (~41s).

**Clarification:** Eight concise cosmology labels were expanded (one export heading, four regional exports, one forbidden-schools heading, and two named schools); each remains under the X/XI draft presentation marker.

---

## Files touched (wave 67)

- `src/components/SpellsLibrary.tsx` — actionable empty state and complete discovery reset
- `src/components/MonstersLibrary.tsx` — search-aware filter state and actionable empty state
- `src/data/CONTINUITY_GLOSSARY.md` — Session persistence + library behavior continuity addendum
- `docs/mechanics/OVERNIGHT_STATUS_MIDNIGHT.md` — wave 67 midnight append
- `docs/mechanics/OVERNIGHT_PROGRESS.md` — this wave 67 append
- `docs/mechanics/OVERNIGHT_HANDOFF.md` — wave 67 append

---

### Wave 67 validation update

```bash
npx tsc --noEmit   # exit 0 (~10s)
npm run build      # exit 0 (~41s)
```

---

## Wave 68 — Recovery smoke coverage + Ashen Grove draft enrichment (2026-07-30)

**Worker:** Overnight wave 68  
**Commit:** none (per owner request)

### 1. Repeatable recovery smoke paths

| Surface | Change |
|---------|--------|
| **`PLAYTEST_SMOKE.md`** | Appended optional-stretch rows for Items, Spells, and Bestiary zero-result states. Each directs the tester to a guaranteed zero-match input, verifies **Clear all filters**, and names preserved state where relevant. |
| **Session Burnout** | Appended a single repeatable path that triggers the transient Overcast check, then verifies each requested recovery exit: **Short rest**, **Long rest (+8h)**, and direct row-level **Full** restore. |

### 2. Draft hero-form clarity

| Surface | Change |
|---------|--------|
| **`druid-shapeshifting.js`** | Marked Circle of the Ashen Grove’s Charbear and Blazewood Stag as draft, then enriched their six existing trait blurbs with descriptive context only. |
| **`ClassPathDisplay.tsx`** | Added a shared **Draft** badge for draft hero-path blocks; other hero paths render unchanged. |
| **Scope boundary** | No numeric values, areas, action economy, effects, unlocks, or other mechanics changed. No Oracle/Paladin/Umbrin prose review or totem automation was introduced. |

### 3. Validation

```bash
npx tsc --noEmit   # pending
npm run build      # pending
```

### Wave 68 validation update

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~49s)
```

---

## Wave 69 — Encounters filter recovery parity (2026-07-30)

**Worker:** Overnight wave 69  
**Commit:** none (per owner request)

### 1. Encounter search recovery

| Surface | Change |
|---------|--------|
| **`EncountersBrowser.tsx`** | Search now reports its tier-match count and offers **Clear filters** whenever a query is active. Tier matches remain selectable from the result row. |
| **Global zero results** | A query that matches no tier now renders an explicit recovery card with **Clear filters**, rather than relying on the search-icon control alone. |
| **Within-tier zero results** | Empty Safe Havens and Points of Interest cards now expose the same reset action when a query filtered their entries out. Unmapped-depth copy remains unchanged when no query is active. |
| **Generators** | Skipped: it has tier selection and output generators, but no filter-driven result set or corresponding empty state. |

### 2. Scope boundary

The remaining Druid hero-form trait batch was already completed in wave 65, and the only newly marked draft forms (Ashen Grove) received context enrichment in wave 68. No duplicate non-canonical content was introduced. Oracle, Paladin, Umbrin, and totem automation remain untouched.

### 3. Validation

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~48s)
```

---

## Wave 78 final ledger — Prestige thin batch + Myth & History draft flavor (2026-07-30)

**Worker:** Overnight wave 78  
**Commit:** none (per owner request)

Hexblade’s **Blade Hunger**, Storm Lord’s **Eye of the Tempest**, Verdant Animist’s **Living Terrain**, and Warlock’s **Pact Sigils** now have presentation-only draft flavor and the existing Builder/Character Sheet hallmark badge. World VII **Myth & History** is visibly draft while retaining its five source labels and adding one short Draft color line per label. No mechanics, prerequisites, capstones, chronology, people, places, dungeon facts, Oracle/Paladin/Umbrin review, totem automation, or 3D work changed.

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~46s)
```

---

## Wave 78 — Prestige thin batch + Myth & History draft flavor (2026-07-30)

**Worker:** Overnight wave 78  
**Commit:** none (per owner request)

### 1. Prestige draft provenance

| Surface | Change |
|---------|--------|
| **Hexblade / Storm Lord / Verdant Animist / Warlock** | Blade Hunger, Eye of the Tempest, Living Terrain, and Pact Sigils receive compact, presentation-only draft flavor. |
| **Builder + Character Sheet** | Existing indexed hallmark rendering now shows the small **draft** badge for each new entry. |
| **Mechanics boundary** | No numerical effect, requirement, eligibility, or capstone changed. |

### 2. Source-bounded cosmology draft flavor

| Surface | Change |
|---------|--------|
| **World VII — Myth & History** | The five existing extract labels remain unchanged; the section is visibly **Draft**, with one short Draft color line per label. |
| **Scope boundary** | No chronology, people, places, dungeon facts, or game rules changed. |

### 3. Validation

```bash
npx tsc --noEmit   # pending
npm run build      # pending
```

---

## Wave 77 — prestige provenance smoke + thin-copy pass (2026-07-30)

**Worker:** Overnight wave 77  
**Commit:** none (per owner request)

### 1. Draft-badge smoke coverage

`PLAYTEST_SMOKE.md` now gives a deterministic Builder → Sheet path for World VIII’s existing **Draft** marker and the first three prestige hallmark badges: Bloodbound’s **Bloodletting Strikes**, Forge Master’s **Ember Pulse**, and Hexblade’s **Doom Sigil**.

### 2. Next short prestige batch

| Path | Draft-marked hallmark enrichment |
|------|----------------------------------|
| **Sapper** | **Demolition Pack** and **Saboteur’s Toolkit** gain compact draft flavor and indexed draft badges. |
| **Soulrender** | **Echo of Death** gains compact draft flavor and an indexed draft badge. |

The existing Builder and Character Sheet badge rendering carries these three indices without component changes. No class eligibility, prerequisites, numerical effect, capstone, or other prestige mechanic changed.

### 3. Scope boundary

No Oracle/Paladin/Umbrin author review, totem automation, Dungeon Guide empty-state work, source promotion, or 3D client work was performed.

### Wave 77 validation update

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~45s)
```

---

## Wave 70 — Encounter smoke stretch + cosmology draft flavor (2026-07-30)

**Worker:** Overnight wave 70  
**Commit:** none (per owner request)

### 1. Floor Encounters recovery smoke

| Path | Deterministic input | Expected recovery |
|------|---------------------|-------------------|
| **Global zero results** | `zzzz-wave-70` | The match row reports zero tiers, the no-results card offers **Clear filters**, and reset restores the selected tier plus its handoff control. |
| **Within-tier empty column** | T1 `Crystalfront` | Safe Havens stays populated; Points of Interest renders its local no-match copy and **Clear filters**. Reset restores both columns without changing the selected tier. |

### 2. Fresh draft cosmology enrichment

| Surface | Change |
|---------|--------|
| **World section X — Economy & Trade** | Marked the presentation draft and expanded the brief regional-export labels with market-travel flavor only. Existing goods and locations are unchanged. |
| **World section XI — Magic Systems** | Marked the presentation draft and expanded the short forbidden-school labels with atmospheric context only. Spell access, costs, restrictions, and rules are unchanged. |
| **Scope boundary** | No Oracle/Paladin/Umbrin tone review, totem automation, mechanics, or source canon promotion. |

### 3. Validation

```bash
npx tsc --noEmit   # exit 0
npm run build      # pending
```

---

### Wave 74 validation update

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~48s)
```

---

## Wave 71 — Draft badge consistency + cosmology trade flavor (2026-07-30)

**Worker:** Overnight wave 71  
**Commit:** none (per owner request)

### 1. Ashen Grove draft status follows the character

| Surface | Change |
|---------|--------|
| **Builder** | Circle selector calls out Ashen Grove as `(draft)`; the selected-circle notice, hero-form heading, and each draft form show **Draft**. |
| **Character Sheet** | Selected draft circle gains a shared **Draft** badge and names its draft hero forms explicitly. |
| **Session** | Hero-form picker and active-form readout retain the draft marker so table play does not hide Builder’s status. |
| **Data boundary** | `hasDraftHeroFormsForCircle()` and the form payload carry existing source status only; no unlock, trait, value, or action behavior changed. |

### 2. Source-bounded World X flavor

| Extract label | Draft presentation-only context |
|---------------|---------------------------------|
| **Divine Essence** | Adds a merchant’s glow/resonance inspection before a bargain, without changing its stated barter, relic, or ritual use. |
| **Shard Markets** | Adds awnings, ward-lanterns, and public scales as market atmosphere, without changing Naegul’s protection or the no-theft rule. |

### 3. Scope and validation

No Oracle/Paladin/Umbrin tone review, totem automation, source promotion, or mechanics change.

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~50s)
```

---

## Wave 72 — Ashen Grove persistence smoke + legends draft flavor (2026-07-30)

**Worker:** Overnight wave 72  
**Commit:** none (per owner request)

### 1. Persisted Ashen Grove draft smoke

| Surface | Check |
|---------|-------|
| **Builder → Sheet → Session** | New optional stretch creates or loads an Ashen Grove Druid, confirms circle/form markers, saves and refreshes before inspecting Sheet, then adds the same saved Druid to Session to check picker and active-form markers. |
| **Leak guard** | The same path verifies a non-Ashen circle does not inherit Ashen Grove or hero-form draft status. |

### 2. Source-bounded legend presentation

| Surface | Change |
|---------|--------|
| **World XIII — Legends & Songs** | The existing three extract labels remain verbatim. Section XIII is visibly draft, and each receives one short “Draft color” presentation blurb. |
| **Scope boundary** | No historical event, NPC, rule, unlock, value, or gameplay behavior was added or changed. |

### 3. Validation

```bash
npx tsc --noEmit   # pending
npm run build      # pending
```

---

### Wave 75 validation update

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~46s)
```

## Wave 73 — Appendix draft flavor + Dungeon Guide empty state (2026-07-30)

**Worker:** Overnight wave 73  
**Commit:** none (per owner request)

### 1. Source-bounded appendix presentation

| Surface | Change |
|---------|--------|
| **World XV — Appendices** | The existing four extract labels remain intact. The section is visibly **Draft**, and each label receives one short presentation-only color line. |
| **Scope boundary** | No chronology, lineage, dungeon-reference, calendar fact, rule, unlock, value, or gameplay behavior changed. |

### 2. Dungeon Guide filtered-details recovery

| Surface | Change |
|---------|--------|
| **Tier Details** | A zero-match search or mapped-only combination now shows a dedicated empty state instead of a stale, non-matching tier. |
| **Recovery** | The empty state provides one-click **Clear filters** to restore the tier navigator. |

### 3. Validation

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~47s)
```

---

## Wave 74 — Dungeon Guide overview recovery smoke (2026-07-30)

**Worker:** Overnight wave 74  
**Commit:** none (per owner request)

### 1. Overview zero-result recovery

| Surface | Change |
|---------|--------|
| **Dungeon Guide → Overview** | A zero-match tier grid now renders an in-place recovery card with **Clear filters**, rather than passive no-results copy. |
| **State boundary** | Reset clears only the tier search and mapped-only toggle; selected tier and encounter data remain intact. |

### 2. Playtest stretch

| Path | Expected |
|------|----------|
| **Overview zero-result recovery** | The deterministic `zzzz-wave-74` query renders the recovery card; reset restores all ten tier cards and preserves the selected tier. |

### 3. Scope boundary

No cosmology or prestige flavor was added because the remaining fresh world sections are either source-gap placeholders, mechanics, or explicitly superseded. No Oracle/Paladin/Umbrin tone review, totem automation, or 3D work.

### 4. Validation

```bash
npx tsc --noEmit   # pending
npm run build      # pending
```

---

## Wave 75 — Dungeon Guide paired recovery smoke (2026-07-30)

**Worker:** Overnight wave 75  
**Commit:** none (per owner request)

### 1. Recovery parity

| Surface | Change |
|---------|--------|
| **Tier Details + Overview smoke** | Added one deterministic `zzzz-wave-75` path that applies both an impossible query and **Mapped tiers only**, verifies each dedicated zero-result card, then checks reset preserves the selected tier. |
| **Mechanics → Victory Consequences** | A query that empties the existing consequence rows now renders an explicit no-match explanation with **Clear filters**, rather than a heading with a blank list. Reset clears only search state and returns all ten rows. |

### 2. Scope boundary

No cosmology or prestige flavor was added because no fresh usable non-mechanical source labels were identified. No source fact, mechanics, Oracle/Paladin/Umbrin review, totem automation, or 3D work changed.

### 3. Validation

```bash
npx tsc --noEmit   # pending
npm run build      # pending
```

---

## Wave 76 — Races draft color + prestige hallmark provenance (2026-07-30)

**Worker:** Overnight wave 76  
**Commit:** none (per owner request)

### 1. Source-bounded draft flavor

| Surface | Change |
|---------|--------|
| **World VIII — Races of Aethel** | The five existing extract labels remain intact. The section is visibly **Draft**, and each label receives one short presentation-only color line. |
| **Scope boundary** | No ancestry, origin, location, ability, rule, or gameplay fact changed. |

### 2. Prestige provenance

| Surface | Change |
|---------|--------|
| **Bloodbound / Forge Master / Hexblade** | Three compact hallmark enrichments are explicitly draft: Bloodletting Strikes, Ember Pulse, and Doom Sigil. |
| **Builder + Character Sheet** | A small **draft** badge appears only beside the flagged hallmark, keeping author-pending prose separate from existing prestige content. |
| **Mechanics boundary** | Existing mechanical claims, class eligibility, requirements, and capstones remain unchanged. |

### 3. Validation

```bash
npx tsc --noEmit   # exit 0
npm run build      # exit 0 (~48s)
```

---

### Wave 78 append-only validation ledger

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Commit: none.

---

## Wave 79 — wave 78 badge smoke + short prestige capstones (2026-07-30)

**Shipped:**

- **PLAYTEST_SMOKE coverage:** Added deterministic Builder → Sheet checks for wave 78’s **Blade Hunger**, **Eye of the Tempest**, **Living Terrain**, and **Pact Sigils** hallmark badges, plus the four draft capstone badges below.
- **Short-capstone draft batch:** Scanned all 18 prestige capstones; the four shortest candidates — **Gravetouched**, **Warlock**, **Battlemage**, and **Hexblade** — now have expanded draft presentation prose. `draftCapstone` lets Builder and Sheet label precisely those capstones with the existing compact **draft** treatment.
- **Scope preserved:** No eligibility, prerequisite, numerical resolution, capstone behavior, Oracle/Paladin/Umbrin review, totem automation, cosmology, dungeon facts, or 3D work changed.

**Validation:** pending wave 79.  
**Commit:** none.

### Suggested wave 80

Run the two wave 79 Builder → Sheet provenance paths in-browser. If both badge groups persist, scan the remaining undrafted prestige capstones for a second bounded batch; otherwise fix only a reproducible badge-propagation defect.

### Wave 79 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). Commit: none.

---

## Wave 80 — second prestige capstone draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. All new prestige prose remains explicitly draft.

### Delivered

| Surface | Result |
|---|---|
| **Capstone scan** | Ranked the 14 undrafted capstones by existing text length. The next four were **Sapper** (111), **Forge Master** (114), **Bloodbound** (116), and **Echomancer** (118 characters). |
| **`prestige-lorebook.json`** | Each selected capstone now has bounded presentation flavor plus `draftCapstone: true`; the pre-existing Builder and Sheet badge path therefore marks only these four records. |
| **`PLAYTEST_SMOKE.md`** | Added Wave 80’s deterministic Builder → Sheet provenance check for the four new capstone badges, with an explicit no-resolution/no-automation boundary. |

### Scope boundary

- No capstone numerical resolution, eligibility, prerequisite, feat, or class behavior changed.
- No Oracle, Paladin, or Umbrin author-tone work occurred.
- No totem automation, cosmology/dungeon facts, 3D/client work, source promotion, commit, or deletion occurred.

### Remaining queue

**10** prestige capstones remain without `draftCapstone`. Next shortest candidates: Wyrmslayer (118; tie behind lower-numbered Echomancer), Verdant Animist (121), Mooncursed (122), and Giant Killer (126).

### Validation

Pending Wave 80 validation.

### Wave 80 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~47s). Commit: none.

---

## Wave 81 — third prestige capstone draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. All new prestige prose remains explicitly draft.

### Delivered

| Surface | Result |
|---|---|
| **Capstone scan** | Ranked the 10 undrafted capstones by existing text length. The next four were **Wyrmslayer** (118), **Verdant Animist** (121), **Mooncursed** (122), and **Giant Killer** (126). |
| **`prestige-lorebook.json`** | Each selected capstone now has bounded presentation flavor plus `draftCapstone: true`; the shared Builder and Sheet branch marks only these four additional records. |
| **`PLAYTEST_SMOKE.md`** | Added Wave 81’s deterministic Builder → Sheet provenance check for the four new capstone badges, with an explicit no-resolution/no-automation boundary. |

### Scope boundary

- No capstone numerical resolution, eligibility, prerequisite, feat, or class behavior changed.
- No Oracle, Paladin, or Umbrin author-tone work occurred.
- No totem automation, cosmology/dungeon facts, 3D/client work, source promotion, commit, or deletion occurred.

### Remaining queue

**6** prestige capstones remain without `draftCapstone`. Run the Wave 81 Builder → Sheet provenance path, then rescan the six remaining records before choosing the next bounded batch.

### Validation

Pending Wave 81 validation.

### Wave 81 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~43s). Commit: none.

---

## Wave 82 — fourth prestige capstone draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. All new prestige prose remains explicitly draft.

### Delivered

| Surface | Result |
|---|---|
| **Capstone rescan** | Ranked the six undrafted capstones by existing text length. The next four were **Soulrender**, **Blademaster**, **Berserker**, and **Storm Lord**. |
| **`prestige-lorebook.json`** | Each selected capstone now has bounded presentation flavor plus `draftCapstone: true`; the shared Builder and Sheet branch marks only these four additional records. |
| **`PLAYTEST_SMOKE.md`** | Added Wave 82’s deterministic Builder → Sheet provenance check for the four new capstone badges, with an explicit no-resolution/no-automation boundary. |

### Scope boundary

- No capstone numerical resolution, eligibility, prerequisite, feat, or class behavior changed.
- No Oracle, Paladin, or Umbrin author-tone work occurred.
- No totem automation, cosmology/dungeon facts, 3D/client work, source promotion, commit, or deletion occurred.

### Remaining queue

**2** prestige capstones remain without `draftCapstone`: **Beastmaster** and **Chronomancer**. Suggested Wave 83: draft-enrich those final two and run their Builder → Sheet provenance path.

### Validation

Pending Wave 82 validation.

### Wave 82 validation update

`npx tsc --noEmit` passed (~12s) and `npm run build` passed (~42s). Commit: none.

---

## Wave 83 — final prestige capstone draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. All new prestige prose remains explicitly draft.

### Delivered

| Surface | Result |
|---|---|
| **Capstone rescan** | The final two undrafted capstones were **Beastmaster** and **Chronomancer**. |
| **`prestige-lorebook.json`** | Both capstones now have bounded presentation flavor plus `draftCapstone: true`; the existing shared Builder and Sheet branch exposes their compact draft badges. |
| **`PLAYTEST_SMOKE.md`** | Added Wave 83’s deterministic Builder → Sheet provenance check for both final capstone badges, with an explicit no-resolution/no-automation boundary. |
| **Completion scan** | All **18/18** prestige paths now carry `draftCapstone: true`; **0** capstones remain undrafted. |

### Scope boundary

- No capstone numerical resolution, eligibility, prerequisite, feat, or class behavior changed.
- No Oracle, Paladin, or Umbrin author-tone work occurred.
- No totem automation, cosmology/dungeon facts, 3D/client work, source promotion, commit, or deletion occurred.

### Suggested Wave 84

Optional small lane only: record the completed 18/18 capstone draft pass in the morning handoff after author review is scheduled. Do not promote, resolve, or automate capstones.

### Validation

Pending Wave 83 validation.

### Wave 83 validation update

`npx tsc --noEmit` passed and `npm run build` passed (build ~47s). The JSON scan confirms `18/18` `draftCapstone: true`; **0** remain undrafted. No commit created.

---

## Wave 84 — prestige presentation handoff + unmapped-depth draft extract (2026-07-30)

**Protocol:** No commits; no mass deletion. New dungeon copy is explicitly draft and presentation-only.

### Delivered

| Surface | Result |
|---|---|
| **Morning handoff** | Recorded Wave 83’s completed prestige presentation pass for author scheduling: **18/18** `draftCapstone` records, **0** undrafted. |
| **`floor-encounters.json`** | Expanded only the existing T6–T10 tier, haven, POI, gate, and boss labels with survivor-rumor draft flavor. Each tier has a source-bound `draftNote`; no route, hazard, map, encounter, reward, or rule was added. |
| **`EncountersBrowser.tsx`** | Renders a compact **Draft extract** badge and the tier’s scope note, so the unmapped-depth content is visibly provisional rather than looking authoritative. |

### Scope boundary

- No prestige capstone or hallmark mechanics, eligibility, prerequisites, or promotion changed.
- No Oracle, Paladin, or Umbrin author-tone work occurred.
- No feat/item mechanics were touched: their available draft entries include unresolved rules text and are not safe for a flavor-only pass.
- T6–T10 remain unmapped; their source labels and existing survivor-rumor framing bound the new presentation copy.

### Remaining queue

- Prestige capstones: **0/18** undrafted.
- Prestige hallmarks: **0/18** lacking the existing draft treatment.
- Dungeon mapping: **5/10** mapped; T6–T10 remain intentionally provisional.

### Validation

Pending Wave 84 validation.

### Wave 84 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~50s). No commit created.

### Wave 84 hallmark completion update

The targeted length scan confirms all **18/18** prestige paths contain hallmarks. It found **0** under 80 characters and two draft entries under 100 characters: Sapper **Saboteur’s Toolkit** (92) and Soulrender **Echo of Death** (97). Both now have longer presentation-only draft copy; their existing `draftHallmarkIndices` positions are unchanged. A final validation rescan follows.

### Wave 84 final validation

`npx tsc --noEmit` and `npm run build` passed (build ~47s). Final scan: **18/18** paths with hallmarks, **0** under 80, **0** under 100; **18/18** draft capstones and **0** undrafted. No commit created.

---

## Wave 85 — unmapped-depth visibility smoke + feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New feat prose is explicitly draft and bounded to existing rules text.

### Delivered

| Surface | Result |
|---|---|
| **`DungeonGuide.tsx`** | T6–T10 now expose their existing `draftNote` in Tier Details with a visible **Draft extract** badge and warning panel. The note participates in the existing guide search haystack. |
| **`PLAYTEST_SMOKE.md`** | Added one reproducible T6–T10 visibility path plus a Builder feat-provenance pass. Both name the presentation-only boundary. |
| **`feats.js` + Builder** | Replaced four generic descriptions—Acrobatic Mastery, Arcane Armor, Arcane Flexibility, Arcane Pulse—with bounded draft copy and a per-entry `draft` flag. Builder renders a compact badge for those flags. |

### Scope boundary

- T6–T10 remain `mapped: false`; no routes, hazards, maps, rewards, encounter resolution, or dungeon procedures were added.
- Feat prerequisites and effect strings remain unchanged; the companion does not automate the selected feat effects.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, source promotion, 3D/client work, commit, or deletion occurred.

### Validation

Pending Wave 85 validation.

### Wave 85 validation update

`npx tsc --noEmit` passed (~10s) and `npm run build` passed (~43s). No commit created.

---

## Wave 86 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Arcane Recall**, **Arcane Transfusion**, **Armor Crusher**, and **Battle Awareness** with draft presentation copy and set `draft: true`. The existing shared Builder badge now visibly identifies all four records. |
| **`PLAYTEST_SMOKE.md`** | Added a type-filtered Builder path that checks every Wave 86 badge, description, prerequisite, and unchanged effect field. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **84** `General feat from the Decennium Descent compendium.` descriptions remain.
- The existing short-effect scan now reports **8** draft feats under 80 effect characters; this is expected because the effects are source fields intentionally left unchanged, not thin descriptions.

### Validation

Pending Wave 86 validation.

### Wave 86 scan correction

The exact generic-placeholder scan reports **112** remaining `General feat from the Decennium Descent compendium.` descriptions. The earlier **84** figure was not a completed scan and is superseded by this count.

### Wave 86 validation update

`npx tsc --noEmit` passed (~7s) and `npm run build` passed (~47s). The exact generic-placeholder scan reports **112** remaining; `find_thin_draft_feats.py` reports **8** short source-effect strings across draft feats. No commit created.

---

## Wave 87 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Battlefield Commander**, **Battlefield Tactician**, **Beast Whisperer**, **Berserker Rage**, **Bleeding Edge**, **Blood Magic**, **Brace for Impact**, and **Break Line** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **104** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

Pending Wave 87 validation.

### Wave 87 validation update

`npx tsc --noEmit` passed (~8s) and `npm run build` passed (~41s). The exact generic-placeholder scan reports **104** remaining. No commit created.

---

## Wave 88 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Bull Rush**, **Channeled Flow**, **Cleaving Momentum**, **Climb Anywhere**, **Close Quarters Combat**, **Cold Reader**, **Combat Intuition**, and **Combat Slide** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **96** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

Pending Wave 88 validation.

### Wave 88 validation update

`npx tsc --noEmit` passed and `npm run build` passed (~44s). The exact generic-placeholder scan reports **96** remaining. No commit created.

---

## Wave 89 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Concentrated Will**, **Counterspell Adept**, **Crippling Strike**, **Cultural Expert**, **Danger Sense**, **Diligent Researcher**, **Disarming Blow**, and **Disguise Expert** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **88** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

Pending Wave 89 validation.

### Wave 89 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **88** remaining. No commit created.

---

## Wave 90 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Dispel Precision**, **Double Tap**, **Draw Cut**, **Dungeon Cartographer**, **Echo Spell**, **Efficient Caster**, **Empowered Summoning**, and **Energy Sink** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **80** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

Pending Wave 90 validation.

### Wave 90 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **80** remaining. No commit created.

---

## Wave 91 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Ether Anchor**, **Exploit Weakness**, **Field Medic**, **Field Surgeon**, **Flash Cast**, **Fleet of Foot**, **Forensic Investigator**, and **Foresight Surge** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **72** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

Pending Wave 91 validation.

### Suggested wave 92

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

---

### Wave 93 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **56** remaining. No commit created.

### Wave 91 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **72** remaining. No commit created.

---

## Wave 92 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Herbalist**, **Illusionist’s Trick**, **Inspiring Presence**, **Intuitive Reflex**, **Jack of All Trades**, **Librarian's Eye**, **Lingering Magic**, and **Lock Savant** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **64** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

Pending Wave 92 validation.

### Suggested wave 93

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Wave 92 validation update

`npx tsc --noEmit` and `npm run build` passed (build ~44s). The exact generic-placeholder scan reports **64** remaining. No commit created.

---

## Wave 93 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Lunge**, **Magical Fortitude**, **Mana Burn**, **Mental Buffer**, **Mental Fortress**, **Merchant’s Guile**, **Mirror Cast**, and **Mystic Focus** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **56** `General feat from the Decennium Descent compendium.` descriptions remain.

### Validation

Pending Wave 93 validation.

### Suggested wave 94

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add the matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

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

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Ritual Channeler**, **Rogue’s Escape**, **Runic Scholar**, **Runic Shield**, **Savage Momentum**, **Shattering Smash**, **Shield Bash**, and **Shield Expert** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: pending Wave 96 validation; expected **32** `General feat from the Decennium Descent compendium.` descriptions.

### Validation

Pending Wave 96 typecheck and build.

### Suggested wave 97

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). The exact generic-placeholder scan reports **32** remaining. No commit created.

---

## Wave 97 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Silent Casting**, **Silent Movement**, **Silver Tongue**, **Skill feats1. Master Tracker**, **Spell Deflection**, **Spell Reservoir**, **Spell Scribe**, and **Spellweave** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: pending Wave 97 validation; expected **24** `General feat from the Decennium Descent compendium.` descriptions.

### Validation

Pending Wave 97 typecheck and build.

### Suggested wave 98

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Validation update

`npx tsc --noEmit` passed. `npm run build` passed (build ~41s). The exact generic-placeholder scan reports **24** remaining. No commit created.

---

## Wave 98 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Steady Hands**, **Still Casting**, **Stubborn Resolve**, **Sure Shot**, **Tactical Flanker**, **Tactical Insight**, **Target Mark**, and **Temporal Flux** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **Display label** | Normalized the malformed Wave 97 label **Skill feats1. Master Tracker** to the clearly matching source title **Master Tracker**; its prerequisite and effect remain unchanged. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: expected **16** `General feat from the Decennium Descent compendium.` descriptions.

### Validation

Pending Wave 98 typecheck and build.

### Suggested wave 99

Select the next eight exact generic placeholder feats only after confirming each description can remain bounded to its existing prerequisite and effect fields; add matching compact Builder provenance smoke, rerun the exact-placeholder scan, and preserve the draft badge. Do not rewrite source effect strings or reopen the author-tone lanes.

### Validation update

`npx tsc --noEmit` passed (~7s) and `npm run build` passed (~41s). The exact generic-placeholder scan reports **16** remaining. No commit created.

---

## Wave 99 — generic feat draft batch (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the generic descriptions for **Tenacity**, **Tinker Adept**, **Tough as Nails**, **Trap Sense**, **Twin Cast**, **Unshakeable**, **Unstoppable Force**, and **Versatile Artisan** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row covering all eight badges, descriptions, prerequisites, unchanged effect fields, and the non-automated selection boundary. |

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Remaining queue

- Exact generic placeholder scan: **8** remaining canonical feat records. The raw literal scan also finds the pre-existing duplicate `master_tracker` record, which is excluded because Wave 98 normalized the matching visible Master Tracker record.

### Validation

Pending Wave 99 typecheck and build.

### Suggested wave 100

Finish the final eight canonical exact generic placeholders with the same bounded draft presentation, compact type-filtered Builder provenance, and rescan. Preserve source prerequisite/effect strings and do not reopen author-tone lanes.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The canonical exact generic-placeholder scan reports **8** remaining; the raw literal search returns **9** because it includes the pre-existing duplicate `master_tracker` record. No commit created.

---

## Wave 100 — final generic feat presentation pass (2026-07-30)

**Protocol:** No commits; no mass deletion. New prose is explicitly draft and bounded to existing feat fields.

### Delivered

| Surface | Result |
|---|---|
| **`feats.js` + Builder** | Replaced the final eight exact generic descriptions for **Versatile Grip**, **Volley**, **Weapon Finesse**, **Weapon Mastery**, **Whip Control**, **Whirlwind Striker**, **Wilderness Chef**, and **Wilderness Walker** with bounded draft presentation copy and set `draft: true`. The existing shared Builder badge visibly identifies all eight records. |
| **Duplicate placeholder repair** | The raw-search exception is confirmed: `master_tracker` and `skill_feats1_master_tracker` are separate records with the same name, prerequisite, and effect. The former still held a **Skill** placeholder, so it now carries the same bounded draft presentation and badge; neither record was deleted, merged, retyped, or otherwise mechanically changed. |
| **`PLAYTEST_SMOKE.md`** | Added one compact type-filtered Builder provenance row for the final eight and an author-decision check for the duplicate Master Tracker records. |

### Remaining queue

- Exact generic placeholder scan: **0** remaining `General feat from the Decennium Descent compendium.` descriptions.
- Author follow-up: decide whether the duplicate `master_tracker` / `skill_feats1_master_tracker` records should coexist and which type/identity is canonical. This pass intentionally leaves both intact.

### Scope boundary

- Each description is derived only from that feat’s existing prerequisite and effect text.
- No prerequisite, effect string, feat selection behavior, or automation changed.
- No Oracle, Paladin, or Umbrin author-tone review, totem automation, T6–T10 mapped content, commit, or deletion occurred.

### Validation

Pending Wave 100 typecheck and build.

### Suggested wave 101

Close the feat presentation lane with the author’s Master Tracker deduplication decision, then move to the highest-value remaining TTRPG companion gap backed by existing source material—prefer a bounded generator or encounter/dungeon playtest pass over new author-tone prose.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). The exact generic-placeholder scan reports **0** remaining; no commit created.

---

## Wave 101 — Session rest feedback (2026-07-30)

**Protocol:** No commits; no mass deletion. This is a Session UX correction only.

### Delivered

| Surface | Result |
|---------|--------|
| **Horn clock** | The time-only button now reads **Advance +8h**, avoiding the false impression that it applies a Long Rest. |
| **Party Resonance** | Short/Long Rest leave a transient, accessible summary that names the affected ally count and existing recovery/reset outcomes. |
| **Smoke** | Added deterministic checks separating clock advance from Short/Long Rest behavior. |

### Scope boundary

- No recovery values, resource rules, rest automation, encounter content, or inventory behavior changed.
- No Oracle, Paladin, or Umbrin author-tone review, T6–T10 mapped content, deletion, or commit occurred.
- `master_tracker` and `skill_feats1_master_tracker` remain a morning **ASK OWNER** canonical-record decision; neither was changed.

### Validation

Pending Wave 101 typecheck and build.

### Suggested wave 102

Manually smoke the updated rests, then address one source-bounded Encounter Library playtest friction point without adding encounter tables.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). No commit created.

---

## Wave 102 — Floor Encounter selection handoff + rest smoke stretch (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Floor Encounters → Session** | The tier-level handoff now states that it sends the default site and fallback haven. Each existing Safe Haven and Point of Interest can send its own selected source entry, so the GM no longer has to accept the first entry in a tier to stage a specific location. |
| **Session handoff boundary** | A selected POI replaces only `Site`; a selected haven replaces only `Fallback haven`. Tier, floors, gate boss, draft warning, and the complementary default entry remain unchanged. No encounter content or resolution was added. |
| **Rest-smoke clarity** | Added a deterministic smoke row distinguishing the time-only clock advance from short- and long-rest feedback, including the ally-count and horn-advance assertions. |

### Scope boundary

- No encounter tables, T6–T10 mapped dungeon material, recovery mechanics, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- `master_tracker` and `skill_feats1_master_tracker` remain a morning **ASK OWNER** decision; neither record changed.

### Validation

Pending Wave 102 typecheck and build.

### Suggested wave 103

Browser-smoke the selected-site and selected-haven Session handoffs alongside the rest-feedback row. If all three pass, take one narrow source-bounded Generator usability pass that reuses existing outputs only; otherwise fix only the demonstrated handoff or feedback regression.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~47s). No commit created.

---

## Wave 103 addendum — Generator pack handoff guardrails

**Waves:** 1–103 done · **Commit:** none  
**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~47s).

Generator Session handoff now requires an already displayed pack, then sends that exact source-backed output. Changing tiers clears the prior pack and disables the handoff until the new tier is built, avoiding stale text paired with new tier metadata. Copying a spark and queuing a pack provide compact success/recovery feedback; no output tables or content were added.

**Smoke pending:** run the appended browser checks for a non-default POI, non-default haven, pack-first/tier-change behavior, and copy feedback.

**Suggested wave 104:** complete those browser smokes, then address only a demonstrated Session handoff friction using existing data. Keep the Master Tracker duplicate decision for the owner; no author-tone or mapped-depth work.

---

## Wave 104 — Bestiary selected-foe Session handoff (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Bestiary → Session** | A selected Bestiary detail can now use **Add foe in Session**. The existing stat block’s name, listed HP, CR, and zone are staged, then Session opens and adds one editable foe. |
| **Session confirmation** | A compact red banner confirms the source name and HP, then directs the GM to adjust initiative, HP, and conditions in the existing Combatants controls. No combat resolution was automated. |
| **Smoke** | `PLAYTEST_SMOKE.md` includes a deterministic one-foe handoff check that confirms source fields and the editable-table boundary. |

### Scope boundary

- No monster, loot, generator, or encounter tables were added or changed.
- No T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- `master_tracker` and `skill_feats1_master_tracker` remain a morning **ASK OWNER** decision; neither record changed.

### Validation

Pending Wave 104 typecheck and build.

### Suggested wave 105

Browser-smoke the selected Bestiary foe, Wave 102 POI/haven, and Wave 103 Generator paths. If all pass, inspect saved-character refresh/import discoverability in Session only; preserve existing storage format and do not add automated inventory or encounter resolution.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). The existing non-fatal `SessionTracker` exhaustive-deps warnings remain; no commit created.

---

## Wave 105 addendum — Session saved-character refresh discoverability

**Waves:** 1–105 done · **Commit:** none  
**Validation:** pending.

Session now explains that it reads the browser’s existing saved-character list, that adding a hero copies it into the current encounter, and that later character changes remain in Characters. The card identifies each available hero by class and level, exposes a count, and provides an accessible **Refresh saved list** result. Its empty state gives the actual recovery path—**CHARACTERS → SAVE → SESSION → Refresh saved list**—and explicitly avoids claiming that Session imports JSON.

The smoke guide adds saved-list return, refresh-feedback, and no-Session-import boundary checks. No storage semantics, character payload, inventory automation, encounter resolution, or content tables changed.

### Wave 105 validation complete

`npm run build` passed (~44s) with the two existing non-fatal `SessionTracker` exhaustive-deps warnings. `npx tsc --noEmit` then passed (~9s); its initial concurrent run raced Next’s `.next` generation and was rerun after the build. No commit created.

---

## Wave 106 — Spell cast-preview Session handoff (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Spells → Session** | Every existing Spell Library card can now use **Preview in Session**. The handoff preserves that spell’s existing reference fields—name, school, tier, casting time, range, and duration—and opens Session. |
| **Session confirmation** | An indigo arrival banner confirms the selected reference and directs the player to choose a caster and use the existing spell lookup / Overcast controls. |
| **Resolution boundary** | The preview does not choose a caster, deduct RP, add a combatant, change any saved character, or resolve a cast. |
| **Smoke** | The smoke guide now tests preview arrival and the manual-resolution boundary; Wave 105 saved-list refresh coverage remains in place. |

### Scope boundary

- Oracle remains Revelation Charges rather than Weave RP; its existing spell-list reference warning is unchanged.
- No character-storage schema, inventory automation, encounter resolution, source tables, T6–T10 mapped dungeon material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.

### Validation

Pending Wave 106 typecheck and build.

### Suggested wave 107

When browser attachment is available, smoke saved-character refresh and spell preview alongside the pending Bestiary, selected POI/haven, and Generator paths. Otherwise, address one narrow source-bounded Session usability gap without changing storage or automating table resolution.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~54s). The two existing non-fatal `SessionTracker` exhaustive-deps warnings remain. No commit created.

---

## Wave 107 — Items reference-preview Session handoff (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Items → Session** | Selected dropped and crafted item details now use **Preview in Session**, staging the existing name, rarity, tier, category, source type, and description before opening Session. |
| **Session confirmation** | A teal arrival banner presents that reference data and makes the GM-facing boundary explicit. |
| **Resolution boundary** | The preview does not write Scene notes, add inventory, add a combatant, change saved data, alter resources, or resolve acquisition, crafting, or use. |
| **Smoke** | `PLAYTEST_SMOKE.md` now provides a deterministic item-preview arrival check plus the manual-resolution and no-auto-inventory assertions. |

### Scope boundary

- No item, loot, crafting, encounter, or dungeon source tables changed.
- No inventory or RP-spend automation, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- `master_tracker` and `skill_feats1_master_tracker` remain a morning **ASK OWNER** decision; neither record changed.

### Validation

`npx tsc --noEmit` passed. `npm run build` pending.

### Suggested wave 108

Browser-smoke the Wave 107 item reference-preview alongside the still-pending saved-character, spell, Bestiary, selected POI/haven, and Generator paths when attachment is available. Otherwise, inspect the two existing non-fatal `SessionTracker` hook warnings and only make a minimal dependency-safe correction if behavior can remain unchanged.

### Validation update

`npm run build` passed (~41s); `npx tsc --noEmit` passed (~10s). The build retains the two existing non-fatal `SessionTracker` exhaustive-deps warnings for `applyPendingHandoffs`; no behavior refactor was made. No commit created.

---

## Wave 109 — hidden active-turn recovery (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Combatants visibility** | When the current turn is hidden by the existing Allies/Foes filter or collapsed crowded-foe view, **Show active turn** reveals that same highlighted combatant with one action. |
| **State boundary** | The recovery changes only display controls: it selects the active side and expands foes when needed. It does not change initiative values/order, turn/round progress, combatant data, or any table resolution. |
| **Smoke** | `PLAYTEST_SMOKE.md` adds deterministic filtered-ally and collapsed-foe paths. |

### Scope boundary

- No character storage, inventory automation, RP/cast automation, encounter resolution, source tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` hook warnings remain intentionally deferred.

### Suggested wave 110

Browser-smoke the consolidated Session-handoff suite plus this active-turn recovery if attachment becomes available. Otherwise, take only another narrow state-preserving Session friction gap.

### Validation

Pending Wave 109 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~41s). Production build repeats only the two intentional non-fatal `SessionTracker` exhaustive-deps warnings; no commit created.

---

## Wave 111 — Character Sheet printable draft-badge parity (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Printable Sheet provenance** | Prestige hallmark and capstone draft markers now reuse the shared printable **Draft** badge, so their print-preview status matches other Sheet draft callouts. |
| **Smoke** | `PLAYTEST_SMOKE.md` adds a narrow onscreen-to-print-preview check using existing prestige paths; Wave 110’s Session rows remain available for browser verification. |

### Scope boundary

- No prestige data, prerequisite, capstone, selection, storage, Session, inventory, RP/cast, or encounter behavior changed.
- No content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 112

Browser-smoke Waves 109–111 when attachment is available. Otherwise, take only one small state-preserving Session or Builder clarity pass; do not refactor the handoff hooks or enter author-review lanes.

### Validation

Pending Wave 111 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 112 — Session dismissal confirmation (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Dismiss-all feedback** | Closing two or more local Session arrival notices now gives an accessible confirmation with the dismissed count and a named state-preservation boundary. |
| **Arrival freshness** | Any later existing handoff clears that old confirmation, leaving the active arrival banner as the current status. |
| **Smoke** | `PLAYTEST_SMOKE.md` adds deterministic stacked-dismissal feedback and new-arrival reset checks. |

### Scope boundary

- No handoff payload, Scene notes, combatants, initiative, turn/round, tier, horn time, resources, storage, inventory, RP/cast, or encounter resolution behavior changed.
- No content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 113

Browser-smoke Waves 109–112 if attachment becomes available. Otherwise, take one small, state-preserving Session or Builder clarity pass using existing outputs only.

### Validation

Pending Wave 112 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 123 — Hero-path reference clarity + Cosmology smoke (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

- **Existing-state path clarity:** `ClassPathDisplay` now exposes a reference-boundary note when a selected class has no existing hero-path entries. Builder and Sheet/print opt in only when a class is present, and existing arch-path cards remain unchanged.
- **Smoke:** `PLAYTEST_SMOKE.md` appends one focused hero-path blank-area check and reaffirms the Wave 122 pre-selection Cosmology **Draft extract** picker notice and † marker.
- **Coffee queue:** The handoff explicitly lists Master Tracker canonical identity, Oracle/Paladin/Umbrin tone, Resonance multiclass draft, and Drow → Umbrin re-ingest for author review. No decision was made overnight.

### Scope boundary

No hero-path, class, progression, save, Resonance, Cosmology, dungeon, Session, inventory/RP/cast automation, encounter, or source-table rule changed. No content tables, T6–T10 mapped material, author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain deferred.

### Suggested wave 124

Browser-smoke the focused Wave 123 Builder/Sheet/print and Cosmology rows when available. Otherwise, make only one confirmed existing-state Builder/Sheet clarity repair; do not reopen author-review lanes, Session hooks, inventory automation, or dungeon design.

### Validation update

`npx tsc --noEmit` passed; `npm run build` passed in ~41s. Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 122 — Cosmology draft-extract visibility + Wave 121 smoke (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

- **Cosmology:** The World of Aethel and First Song pickers now show a visible **Draft extract** notice whenever their existing sections contain draft records. Existing draft sections retain their † picker marker and their per-section provenance note.
- **Smoke:** `PLAYTEST_SMOKE.md` adds one compact path for the new Cosmology notice plus Wave 121’s feat no-match recovery and saved/blank People & traits Sheet-print states.

### Scope boundary

No cosmology, dungeon, feat, people, lineage, trait, class, Resonance, storage, Session, inventory/RP/cast automation, encounter, or source-table rule changed. No content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred. The existing `SessionTracker` hook warnings remain deferred.

### Suggested wave 123

Browser-smoke Wave 122 when attachment is available. Otherwise, keep the overnight lane to one confirmed existing-state Builder or Sheet clarity gap; do not reopen Session hooks, author-tone work, inventory automation, or unmapped dungeon design.

### Validation

`npx tsc --noEmit` passed. `npm run build` passed in ~42s; production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` warnings. No commit created.

---

## Wave 121 final append — Hero-state clarity + morning prep (2026-07-30)

**Delivered:** A Feats name search makes the no-result recovery reachable without changing selection state. Sheet/print now reports only saved people/lineage and existing sourced trait names, with blank/unresolved state explicit. The handoff closes with the Master Tracker, author-tone, and Resonance multiclass owner checklist.

**Boundary:** No source data, rules, automation, author-tone review, mapped T6–T10 material, deletion, or commit occurred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (~51s); only the two deferred `SessionTracker` hook warnings remain.

---

## Wave 121 — Hero-state clarity + morning prep (2026-07-30)

### Delivered

| Surface | Result |
|---|---|
| **Builder Feats** | Added a name search alongside the existing type filter. A zero-result combination now gives a clear, non-mutating recovery message. |
| **Printable Sheet** | Added a **People & traits** summary driven only by the saved people/lineage and existing race source data; blank or unresolved saved state stays explicit. |
| **Morning handoff** | Appended a compact owner checklist for the Master Tracker duplicate, Oracle/Paladin/Umbrin tone review, and the Resonance multiclass draft. |
| **Smoke** | Appended existing-state Builder → save → Sheet/print and zero-result filter checks. |

### Scope boundary

- No people, trait, feat, class, Resonance, character-storage, Session, inventory/RP/cast, encounter, cosmology, or dungeon source rule changed.
- No content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 122

Browser-smoke the Wave 121 rows when available. Otherwise, keep work to one narrow existing-label draft-marker consistency pass in Cosmology/Dungeon; do not reopen author review, owner decisions, Session hooks, or automation.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~51s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 120 — Oracle Mystery and Curse recorded-state parity (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Builder → Paths** | An Oracle with blank existing `oracleMystery` and/or `oracleCurse` state now explicitly says **No Oracle Mystery recorded** / **No Oracle's Curse recorded**, preserves the L1 timing, and makes clear that no corresponding selection is saved. |
| **Character Sheet / print** | The existing missing-Mystery and missing-Curse callouts now use matching recorded-state language while retaining their existing required-at-L1 markers, **Draft** badges, and Character Builder recovery direction. |
| **Smoke** | `PLAYTEST_SMOKE.md` appends a blank-both and one-recorded-selection Builder → save → Sheet/print path. |

### Scope boundary

- No Mystery or Curse data, Oracle rules, revelations, boons, class features, character-save shape, or progression behavior changed.
- No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 121

Browser-smoke the Wave 118–120 recorded-state Builder → save → Sheet/print rows when attachment is available. Otherwise, defer further Oracle presentation work until author review rather than extending this lane.

### Validation

Pending Wave 120 `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~49s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 119 — Sacred Oath recorded-state parity (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Builder → Paths** | A Paladin with existing blank `sacredOath` state now explicitly says **No Sacred Oath recorded**, preserves the L3 timing, and makes clear that no oath selection is saved yet. |
| **Character Sheet / print** | The existing missing-oath callout now uses the same recorded-state language while retaining its L3 requirement and Character Builder recovery direction. |
| **Smoke** | `PLAYTEST_SMOKE.md` appends L1 blank and L3 required Builder → save → Sheet/print checks. |

### Scope boundary

- No oath data, oath rules, class features, character-save shape, or progression behavior changed.
- No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 120

Browser-smoke the Wave 118 Ethos and Wave 119 Sacred Oath blank → save → Sheet/print paths when attachment is available. Otherwise, take one similarly narrow existing-state Builder clarity gap, preferably Oracle Mystery / Curse empty-state parity without changing Oracle rules or tone.

### Validation

Pending Wave 119 `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~55s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 118 — Ethos recorded-state parity (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Builder → Ethos** | When existing `selectedAlignment` state is blank, Builder now explains that no ethos is recorded and identifies its existing save/spell-cost-preview use. |
| **Character Sheet / print** | The identity-badge row now explicitly shows **Ethos not recorded** for a blank saved value, replacing it with the existing selected value after save. |
| **Smoke** | `PLAYTEST_SMOKE.md` appends blank-state and selected-state Builder → save → Sheet/print checks. |

### Scope boundary

- No ethos options, spell-cost calculation, character-save shape, class, feature, or Resonance behavior changed.
- No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 119

Browser-smoke Waves 116–118 when attachment is available. Otherwise, take only one further source-bounded Builder clarity gap backed by existing saved state.

### Validation

Pending Wave 118 `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` passed. `npm run build` passed in ~42s; production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings. No commit created.

---

## Wave 117 — Sheet prestige-path intent parity (2026-07-30, final append)

**Delivered:** The Character Sheet’s existing selected-prestige panel now repeats the Builder intent boundary: the saved choice records a path intention and grants neither prerequisites nor features. Existing requirements and **Draft** provenance remain unchanged; `PLAYTEST_SMOKE.md` adds Builder → Sheet → print coverage.

**Boundary:** No prestige source data, prerequisite, feature, class, Resonance, save rule, Session behavior, automation, encounter resolution, content table, T6–T10 mapped material, author-tone lane, deletion, or commit changed.

**Suggested wave 118:** Browser-smoke Wave 117 when attachment is available. Otherwise, take only one narrow, source-bounded Builder clarity gap using existing saved state.

**Validation:** `npx tsc --noEmit` passed; `npm run build` passed in ~41s. The build reports only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 117 — Sheet prestige-path intent parity (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Character Sheet** | The existing selected-prestige panel now repeats the Builder boundary: it records path intent only and grants neither prerequisites nor features. The existing requirements and draft badges remain unchanged. |
| **Smoke** | `PLAYTEST_SMOKE.md` appends a Builder → Sheet → print check for that saved selection and its unchanged provenance. |

### Scope boundary

- No prestige source data, prerequisite, feature, class, Resonance, or character-storage rule changed.
- No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 118

Browser-smoke Wave 117’s Builder → Sheet → print path when attachment is available. Otherwise, take one narrow, source-bounded Builder clarity improvement consuming existing state only; leave progression, automation, Session hooks, and author-review lanes untouched.

### Validation

Pending Wave 117 `npx tsc --noEmit` and `npm run build`.

---

## Wave 116 — Prestige-path intent clarity (2026-07-30, append checkpoint)

**Delivered:** Class-tab Arch-path selection now records player intent only, directs players to existing requirements and draft markers on **Paths**, and grants neither prerequisites nor features.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~49s); only the two deferred `SessionTracker` exhaustive-deps warnings remain. No commit created.

**Suggested wave 117:** Browser-smoke Waves 114–116 when attachment is available; otherwise retain the narrow, source-bounded Builder clarity lane.

---

## Wave 116 — Prestige-path intent clarity (2026-07-30, final append)

**Delivered:** Class-tab Arch-path selection now says that it records intent only, directs players to **Paths** for existing requirements and draft markers, and does not grant prerequisites or features. `PLAYTEST_SMOKE.md` has the focused Class → Paths check.

**Boundary:** No prestige/class/Resonance/save-data rule, Session behavior, source table, T6–T10 map, automation, author-tone lane, deletion, or commit changed. The two existing `SessionTracker` hook warnings remain deferred.

**Validation:** `npx tsc --noEmit` and `npm run build` passed (build ~49s); only the two existing `SessionTracker` exhaustive-deps warnings remain.

**Suggested wave 117:** Browser-smoke Waves 114–116 when attachment is available; otherwise retain the narrow source-bounded Builder clarity lane.

---

## Wave 116 — Prestige-path intent clarity (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Class → Arch path** | A selected path now explicitly records player intent only, sends the player to **Paths** for its requirements and draft markers, and clarifies that selection grants neither prerequisites nor features. |
| **Smoke** | `PLAYTEST_SMOKE.md` adds a focused Class → Paths verification using an existing prestige path. |

### Scope boundary

- No prestige source data, prerequisite, feature, class, Resonance, or character-storage rule changed.
- No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 117

Browser-smoke Wave 114–116’s Builder → Sheet → print and prestige-path continuity when attachment is available. Otherwise, make only a similarly narrow, source-bounded Builder clarity improvement that consumes existing state.

### Validation

`npx tsc --noEmit` and `npm run build` passed (build ~49s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 115 — printable Sheet multiclass and feature provenance (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Multiclass Sheet print** | The existing draft RP merge callout is print-kept as one legible block. A recorded secondary class with no eligible second Weave pool now carries the same explicit no-pool boundary onto the Sheet and its print view. |
| **Feature draft legend print** | `LevelFeatureList` now supplies print-safe text and badge styling for its draft-milestone legend and each draft feature marker. |
| **Smoke** | `PLAYTEST_SMOKE.md` appends focused eligible-merge, non-Weave-secondary, and level-feature legend print-preview checks. |

### Scope boundary

- No class, feature, multiclass, Resonance, or character-storage rule changed.
- No Session behavior, inventory/RP/cast automation, encounter resolution, content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 116

Run the Wave 114–115 Builder-to-Sheet print checks when browser attachment is available. Otherwise, inspect only a confirmed remaining Builder clarity gap from the handoff using existing saved state; leave Session hooks and author-review lanes closed.

### Validation

Pending Wave 115 `npx tsc --noEmit` and `npm run build`.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~48s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 114 — Builder secondary-class clarity + printable feat provenance (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

| Surface | Result |
|---|---|
| **Secondary class** | Builder now identifies a selected secondary class that is saved but cannot contribute a second eligible Weave pool; eligible pairs retain the existing draft RP merge calculation. |
| **Draft feat provenance** | Draft badges now persist from a feat card to Builder’s Chosen feats list and to the printable Character Sheet. |
| **Smoke** | `PLAYTEST_SMOKE.md` appends focused non-Weave-secondary, merge-panel, and print-preview checks. |

### Scope boundary

- No feat/class/Resonance source data, progression rule, character-storage schema, Session behavior, inventory/RP/cast automation, or encounter resolution changed.
- No content tables, T6–T10 mapped material, Oracle/Paladin/Umbrin author-tone review, deletion, or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 115

Browser-smoke Wave 114 and the pending Wave 109–113 Session rows if attachment becomes available. Otherwise, take only one narrow saved-state presentation or print clarity pass; do not reopen Session filter recovery or hook dependency work.

### Validation

Pending Wave 114 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~42s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Wave 113 — Session filtered-table recovery (2026-07-30)

### Delivered

| Surface | Result |
|---|---|
| **Empty filter state** | A populated Session table now explains when the selected Allies/Foes display filter has no matching rows. |
| **View recovery** | **Show all combatants** returns the existing rows by resetting display state only and expanding the existing foes view. |
| **Smoke** | `PLAYTEST_SMOKE.md` adds empty-Foes-view and field-preservation checks. |

### Scope boundary

- No combatant, initiative, turn/round, Scene notes, tier, horn time, resources, handoff, or storage data changed.
- No inventory, RP/cast, or encounter automation; content tables; T6–T10 mapped material; Oracle/Paladin/Umbrin author-tone review; deletion; or commit occurred.
- The two existing `SessionTracker` `applyPendingHandoffs` warnings remain intentionally deferred.

### Suggested wave 114

Browser-smoke Waves 109–113 if attachment becomes available. Otherwise, take one small, confirmed state-preserving Session or Builder presentation gap using existing outputs only.

### Validation

Pending Wave 113 typecheck and build.

### Validation update

`npx tsc --noEmit` and `npm run build` passed (build ~46s). Production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.
---

## Rulebook wave — Umbrin migration authorized (2026-07-30)

**Delivered:** The editable rulebook source is `rulebook_output.txt`. Its Peoples chapter and language/ability-summary references now migrate **38** Drow-era occurrences to **Umbrin**, including the race heading, traits, variants, Murkish language, **Umbrin Magic**, and **Obsidian Highborn**. The rewritten chapter keeps its mechanical intent while replacing legacy external naming; the Calan'thir / First Choir **Obsidian Burn** account is explicitly marked for author review and grants no mechanic.

**Consistency check:** The companion's active data has no Drow-era product string. `character-storage.js` retains legacy aliases only for load-time migration to Umbrin. `UMBRIN_LORE.md` now accurately records that the rulebook migration has begun while the origin theology stays provisional.

**Validation:** No companion code or active data changed, so no typecheck/build was required.

**Next:** Reconcile this extract with the full rulebook document when available, then take one bounded Oracle mystery or Paladin oath promotion without removing its `draft: true` marker until author approval.

---

## Rulebook wave — Oath of Grief tone pass (2026-07-30)

**Source check:** `rulebook_output.txt` remains the editable living rulebook extract. `decennium descent player rulebook.docx` is present, but was not edited here; the approved Umbrin Peoples material still needs an intentional docx synchronization pass.

**Delivered:** `src/data/paladin-oaths.js` received a bounded, non-mechanical prose pass for the draft **Oath of Grief**. Its theme, summary labels, conduct clauses, and provenance now frame grief as remembrance and the duty of passage. Existing effects, numbers, revelation spells, and `draft: true` status remain unchanged.

**Validation:** Pending `npx tsc --noEmit` and `npm run build` because companion JavaScript data changed.

**Next:** Author-review the Oath of Grief mechanics and revelation wording for promotion, then sync owner-approved Umbrin Peoples copy into the docx.

### Validation update

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two intentionally deferred `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — controlled docx sync assessment + Oath of the Chain (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

- **Docx assessment:** `decennium descent player rulebook.docx` is present and `python-docx` is available. No binary edit was made because the available safe edit path cannot perform a paragraph-scoped replacement with a reviewable backup and post-save comparison. The document remains unchanged; `rulebook_output.txt` is still the living Umbrin extract.
- **Paladin prose:** Draft **Oath of the Chain** now uses bounded rulebook voice for its theme and conduct clauses. The existing mechanics, values, revelation spells, oathbreaker text, final gift, and `draft: true` marker are unchanged.

### Handoff

Treat docx synchronization as a discrete guarded operation: make a backup, reconcile only confirmed Peoples paragraphs, generate a replacement text extract, and compare its Umbrin chapter against `rulebook_output.txt`. Do not promote Oath of the Chain until its existing rules text receives author review.

### Validation

Pending `npx tsc --noEmit` and `npm run build` because `paladin-oaths.js` changed.

### Validation update

`npx tsc --noEmit` and `npm run build` passed. Production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — guarded Umbrin docx sync (2026-07-30)

### Delivered

- **Backup:** Created `decennium descent player rulebook.pre-umbrin-backup.docx` beside the source before mutation.
- **Targeted migration:** The player rulebook's Peoples chapter and seven related source references now replace Drow-era product copy with **Umbrin**, **The Murk**, **Murkish**, **Umbrin Magic**, and **Obsidian Highborn**. The pre-approved, non-mechanical Obsidian Burn author-review note is included.
- **Verification:** The docx reopens cleanly with `python-docx`. A full post-save scan returns zero whole-word Drow references; the unrelated “drowsy” text is retained.

### Boundary

No mechanics, application code, active companion data, Oracle/Paladin draft text, mapped T6–T10 material, inventory/RP/cast automation, Session behavior, or commit changed. Only the three obsolete Drow external-name-list paragraphs were cleared as part of the precise approved chapter migration.

### Next

Author-review the Obsidian Burn theology and provide Umbrin naming examples. Any subsequent Oracle mystery prose pass must retain `draft: true`.

---

## Rulebook wave — Cataclysm Oracle mystery tone pass (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

- **Bounded Cataclysm prose:** `src/data/oracle-mysteries.js` now gives the draft Cataclysm mystery's profile and existing **The Unbound Wound** capstone a compact rulebook-voice presentation.
- **Rules preserved:** Charge costs, ranges, areas, durations, damage, immunity, Exhaustion, patron, and all other Revelation mechanics are unchanged.
- **Draft preserved:** Cataclysm continues to inherit `draft: true` from `draftMysteryRevelations`; no content was promoted to canon.

### Author queue

- Review Cataclysm's full draft mystery tree before promotion.
- Decide Obsidian Burn theology and provide Umbrin naming examples; neither was expanded or invented in this pass.

### Validation

Pending `npx tsc --noEmit` and `npm run build`.

### Cataclysm spot-check update

`rulebook_output.txt` confirms Cataclysm’s source theme, area-damage/battlefield-control role, and feared/suspect reputation. Because the rulebook provides a full Revelation tree only for Ancestor, it cannot promote or fully validate Cataclysm’s draft tree; no contradiction was found.

### Validation update

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## DM XP / encounter audit (2026-07-30)

- Added [`BALANCE_DM_XP.md`](./BALANCE_DM_XP.md): a source-bound audit of XP, CR, Floor Encounters, Bestiary, and Session handoffs.
- The available rulebook extract is Oracle-only; it supplies no XP award/progression table or CR/encounter budget. Existing XP thresholds, Bestiary XP/CR display, CR-to-tier filtering, and gate-boss HP remain unverified companion behavior.
- Top follow-ups: ingest the missing XP/CR chapters before building a calculator; then add source-cited encounter budgeting and a Session XP ledger/write-back. T6–T10 remain unmapped; no encounter tables or rules were invented.

---

## Player rules / class balance audit (2026-07-30)

### Delivered

- Added `docs/mechanics/BALANCE_PLAYER_CLASSES.md`: method, all 17 selectable class snapshots, L1/L5/L10 HP and normalized DPR assumptions, Resonance/RC fairness notes, outlier risks, playtest priorities, and explicit data-only limitations.
- Retained the source boundary: Fighter is archive-only, Swashbuckler is an orphan/non-selectable reference, and Hybrid-B multiclass RP is approved canon.
- No class mechanics, draft labels, rules, source data, or player-facing lore were changed.

### Highest-risk playtests

1. Mirrorsage copy eligibility and action/resource caps.
2. Oracle Revelation Charge recovery against draft Mystery/Curse action-denial and prevention effects.
3. Paladin aura/Oath value versus Soldier and Warrior.
4. Warrior/Dragoon burst and resource/action economy.
5. Tinker deployable count, damage, and board-control economy.

### Source reconciliation needed

The rulebook table and companion entries disagree about armor/proficiency data for Crimson Agent, Dragoon, Mirrorsage, Oracle, and Tinker. Most high-impact abilities also lack finalized numeric, targeting, duration, recharge, or stacking rules, so this is an honest risk audit rather than a numerical pass/fail result.

---

## Rulebook wave — final five-profile tone pass (2026-07-30)

### Delivered

| Surface | Result |
|---|---|
| **Battle + Bones Mysteries** | Replaced only theme, combat role, and reputation with bounded rulebook prose: Battle treats command as service to the line; Bones treats the dead as an account owed care, not ownership. |
| **Oath of Dominion** | Reframed the existing theme and conduct clauses around public responsibility, truthful judgment, and authority that cannot serve itself. |
| **Oath of Flame** | Reframed the existing theme and conduct clauses around restrained purification, protection of the innocent, and renewal after the fire. |
| **Oath of the Ancients** | Reframed the existing theme and conduct clauses around living memory, restraint before irreparable harm, and humility toward old pacts. |

### Scope boundary

- Battle and Bones retain their patrons, full Revelation trees, values, costs, ranges, durations, damage, progression, and shared `draft: true` provenance.
- The three Oaths retain every smite, aura, signature power, revelation spell, oathbreaker entry, final gift, selection rule, numeric field, and explicit `draft: true`.
- No Obsidian Burn theology, Umbrin names, promotion, deletion, or commit occurred.

### Continuity and handoff

The verified five-profile tone-pass queue is **complete: 0 remaining**.

**Next suggestion:** Await Umbrin lore author decisions, then perform the independent curse-tone review. Before a new prose wave, use the coffee checklist to verify visible draft status, no author-only lore leakage, and no mechanics drift.

### Validation

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Continuity stamp — locked Umbrin geography (2026-07-30)

**Delivered:** Locked Proposal 1 across `UMBRIN_LORE.md`, the UTF-16LE `rulebook_output.txt` extract, and the editable player-rulebook docx: **The Murk**, **Blackglass Reach**, **Veyr-Obsid**, and **the Quiet Deep**. The rulebook now also states the transactional, non-redemptive alliance posture.

**Safety:** `decennium descent player rulebook.pre-geography-20260730.docx` was created before editing. No companion data or mechanics changed, no draft flag changed, and no Master Tracker or Resonance decision was made. Typecheck/build were not required; no commit or deletion occurred.

---

## Midnight coffee-prep decision pack (2026-07-30)

**Protocol:** Owner-authorized rulebook documentation; no commit, no mass deletion, and append-only logs.

**Delivered:** Added [`AUTHOR_REVIEW_QUEUE.md`](./AUTHOR_REVIEW_QUEUE.md) with actionable owner cards for provisional Obsidian Burn theology, owner-supplied Umbrin naming examples, Master Tracker's duplicate records, the Resonance multiclass draft, and explicit draft-to-approved candidate lists.

**Verified:** The duplicate feat records remain separate and untouched: `master_tracker` / **Master Tracker** / `Skill`, and `skill_feats1_master_tracker` / **Master Tracker** / `General`. Oracle Mystery/Oath tone passes plus all nine draft curse profile passes are complete, but their draft state is unchanged; Spiral-Touched remains rulebook-complete.

**Validation:** Documentation-only changes; build intentionally skipped. No commit or deletion occurred.

---

## Rulebook wave — Oracle curse tone pass (2026-07-30)

**Delivered:** All nine draft Oracle curse profiles—**Wound Eater**, **Soul-Cracked**, **Haunted**, **Tongues**, **Burning Blood**, **False Life**, **Shattered Mind**, **Consumed**, and **Fate-Bound**—now have bounded rulebook-voice blurbs and limitations in `src/data/oracle-curses.js`.

**Continuity:** This is presentation-only. IDs, names, curse effects, boon trees, unlock levels, values, costs, ranges, durations, damage, and every `draft: true` marker remain unchanged. **Spiral-Touched** remains the single rulebook-complete curse tree; the draft curse tone-pass queue is **0 remaining**.

**Author blockers:** Obsidian Burn theology, Umbrin names, the Master Tracker duplicate, and the Resonance multiclass draft still require author decisions. Review content individually before any `draft → approved` promotion.

**Validation:** Pending `npx tsc --noEmit` and `npm run build`; no commit or deletion occurred.

**Validation update:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Life + Stars Oracle mystery tone pass (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Life mystery:** The draft profile in `src/data/oracle-mysteries.js` now carries bounded rulebook voice for restoration that endures a hard fight, protective shelter, and the courage of preservation.
- **Stars mystery:** The draft profile now carries bounded rulebook voice for foresight that reveals a difficult path, marks an opening, and helps allies use a moment before it closes.
- **Rules preserved:** No Revelation, patron, cost, range, duration, damage, number, or progression field changed. Both mysteries remain `draft: true` through the shared draft helper.

### Boundary

No Obsidian Burn theology, Umbrin name, mechanic, promotion, deletion, or commit was added.

### Handoff

The previous handoff reported **8** untouched profiles. The current source/profile audit identifies **7** without a recorded tone pass: Oracle **Battle**, **Bones**, **Shadow**, and **Time**; Paladin **Oath of Dominion**, **Oath of Flame**, and **Oath of the Ancients**. Reconcile this one-profile discrepancy before closing the queue.

**Suggested next:** Tone-pass **Shadow** or **Time**, retaining `draft: true`, then author-review each completed tree before any promotion.

### Validation

Pending `npx tsc --noEmit` and `npm run build`; no commit created.

### Validation update

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Oath of Mercy + Oath of Vengeance tone pass (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Oath of Mercy:** `src/data/paladin-oaths.js` now gives Mercy bounded rulebook voice for shelter, healing, and the hard work of sparing life. Its conduct clauses define a protector's duty without changing its rules. The profile is explicitly retained as `draft: true`.
- **Oath of Vengeance:** The draft oath now speaks of disciplined pursuit, sworn judgment, and surrender that must be honored without forsaking allies.
- **Rules preserved:** Neither oath's smite, aura, signature power, revelation spells, oathbreaker material, final gift, numeric values, or level timing changed.

### Boundary

No Obsidian Burn theology, Umbrin names, mechanics, promotion, deletion, or commit was added. Both Oaths remain author-review drafts.

### Handoff

**8** untouched `draft: true` Oracle Mystery / Sacred Oath profiles remain after this two-profile pass. Take the thinnest remaining Oracle Mystery next, retaining `draft: true`, and review every completed tree before any promotion.

### Validation

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Oath of Chains Broken tone pass (2026-07-30)

**Protocol:** No commits; no mass deletion. Documentation entries are append-only.

### Delivered

- **Bounded oath prose:** `src/data/paladin-oaths.js` now gives the draft **Oath of Chains Broken** a concise rulebook-voice theme and three conduct clauses centered on breaking unjust bonds, resisting replacement tyranny, and protecting the newly free.
- **Rules preserved:** Smite, aura, signature power, revelation spells, oathbreaker material, final gift, numeric values, and level timing are unchanged.
- **Draft preserved:** The Oath remains explicitly `draft: true`; no content was promoted to canon.

### Source spot-check

Direct Cataclysm comparison against `rulebook_output.txt` is pending. No content was force-promoted.

### Author queue

- **14** untouched `draft: true` Oracle Mystery / Sacred Oath profiles remain after the four completed tone passes.
- Take **Oath of Silence** next for the smallest contained Paladin follow-up, or one complete Mystery profile; review any full tree before promotion.
- Obsidian Burn theology and Umbrin naming examples remain author-only decisions.

### Validation

Pending `npx tsc --noEmit` and `npm run build`.

---

## Rulebook wave — Oath of Silence + Dream mystery tone pass (2026-07-30)

**Delivered:** Draft **Oath of Silence** now has bounded rulebook voice for humility, restraint, and careful judgment; every mechanical field and its `draft: true` marker remain unchanged. Draft **Dream** received a thin profile pass for theme, combat role, and reputation only; its full Revelation tree, patron, costs, ranges, durations, and shared draft provenance are unchanged.

**Boundary:** No Obsidian Burn theology or Umbrin names were authored; neither profile was promoted, deleted, or committed.

**Author queue:** **12** untouched draft Mystery/Oath profiles remain. Suggested next bounded pass: **Oath of the Martyr King** (or one remaining Mystery profile), retaining `draft: true`.

**Validation:** `npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Oath of the Martyr King + Flame mystery tone pass (2026-07-30)

### Delivered

- **Bounded oath prose:** `src/data/paladin-oaths.js` now gives the draft **Oath of the Martyr King** a concise rulebook-voice theme and conduct clauses for stewardship, responsibility, and sacrifice freely borne before it is required of another.
- **Thin Mystery prose:** `src/data/oracle-mysteries.js` now gives draft **Flame** a concise rulebook-voice theme, combat role, and reputation centered on conviction, costly mercy, and decisive fire.
- **Rules preserved:** No oath or Mystery mechanics, revelations, patron, costs, ranges, durations, damage, values, or selection timing changed.
- **Draft preserved:** The Oath remains explicitly `draft: true`; Flame retains `draft: true` through the shared draft helper. Neither profile was promoted.

### Author queue

- **10** untouched `draft: true` Oracle Mystery / Sacred Oath profiles remain after the two completed profiles.
- Take **Oath of Mercy** or **Oath of Vengeance** next for another contained Paladin pass, or select one remaining Mystery profile; review any completed tree before promotion.
- Obsidian Burn theology and Umbrin naming examples remain author-only decisions.

### Validation

Pending `npx tsc --noEmit` and `npm run build`; no commit or deletion occurred.

### Validation update

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## Rulebook wave — Shadow + Time Oracle mystery tone pass (2026-07-30)

**Protocol:** Owner-authorized rulebook edits; no commit, no mass deletion, and documentation remains append-only.

### Delivered

- **Shadow mystery:** `src/data/oracle-mysteries.js` now gives the draft Shadow profile bounded rulebook voice for disciplined silence, concealment, and fear used to control an exposed foe.
- **Time mystery:** The draft Time profile now presents delay and reversal as careful intervention—creating a narrow opening for the party without pretending causality is consequence-free.
- **Rules preserved:** Only each profile's theme, combat role, and reputation changed. Patrons, Revelation trees, costs, ranges, durations, damage, numeric values, and all progression fields are unchanged. Both mysteries retain `draft: true` through the shared draft helper.

### Continuity and handoff

The Life + Stars source/profile audit established **7** untouched profiles. This two-profile pass reduces that reconciled queue to **5**: Oracle **Battle** and **Bones**; Paladin **Oath of Dominion**, **Oath of Flame**, and **Oath of the Ancients**.

**Suggested next:** Take **Bones** for the final remaining Oracle profile, retain `draft: true`, and author-review each completed full tree before any promotion. Obsidian Burn theology and Umbrin names remain author-only decisions.

### Validation

`npx tsc --noEmit` and `npm run build` passed. The production build repeats only the two existing non-fatal `SessionTracker` `applyPendingHandoffs` exhaustive-deps warnings; no commit created.

---

## DM XP / encounter audit (2026-07-30)

Added [`BALANCE_DM_XP.md`](./BALANCE_DM_XP.md). XP awards/progression and CR encounter budgets are absent from the available Oracle-only extract; the next dependency is source ingest, followed by a cited calculator and Session award ledger. No encounter rules were invented; T6–T10 remain unmapped.

---

## Combat simulation (2026-07-30)

Added [`BALANCE_COMBAT_SIM.md`](./BALANCE_COMBAT_SIM.md) plus runnable `scripts/combat-balance-sim.mjs`. The L3 Bloom proxy is too hot; the L8 Vaskor proxy is hard but survivable. Monster attacks, encounter budgets, and an XP-award formula remain the concrete blockers to a final balance verdict; no combat rules were invented.

---

## XP draft + Bloom retune wave (2026-07-30)

### Delivered

- **Draft XP section:** [`XP_ADVANCEMENT_CANON.md`](./XP_ADVANCEMENT_CANON.md) now appends **DRAFT — OWNER APPROVAL REQUIRED** with provisional CR→XP table (mirrors dominant Bestiary pattern), equal four-way party split, and easy/medium/hard/deadly budget sketch keyed to confirmed threshold gaps. Explicit implementation gate: not wired to Session, Builder, or encounter tooling.
- **Bloom retune:** `bestiary_data_full.json` draft `vine-maw` count **2 → 1** only; Spore Burst and other payloads unchanged.
- **Sim rerun:** `node scripts/combat-balance-sim.mjs` — Bloom **62.4 HP / 63.7%** L3 party loss (was 127.3%); Vaskor **115.2 HP / 46.8%** unchanged.
- **Docs stamped:** [`BALANCE_COMBAT_SIM.md`](./BALANCE_COMBAT_SIM.md), [`BALANCE_REPORT.md`](./BALANCE_REPORT.md), [`CONTINUITY_REPORT.md`](../src/data/CONTINUITY_REPORT.md).

### Owner queue

- **Yes/no on draft XP:** Accept CR→XP + equal split + budget sketch as playtest baseline, revise after rulebook ingest, or reject.
- **No companion promotion:** Draft XP must not migrate to Builder thresholds, Session awards, or encounter calculator until approved.

### Validation

Sim only; no commit, no localhost:8500 disruption.