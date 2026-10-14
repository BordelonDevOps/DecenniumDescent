# Character Generation & L1–20 Progression

**Current campaign-playtest use:** begin with the [reviewed creation and advancement foundation](CHARACTER_CREATION_PLAYTEST.md) and [17-class tables](CHARACTER_FOUNDATION_TABLES.md). This July guide documents the companion's older builder and saved-character interface. For the current authored rules, use the [17 class families and their Base, Arch and Hero schedules](CLASS_PLAYTEST_INDEX.md), [shared acquisition rules](CLASS_PLAYTEST_RULES.md), [Paladin Oaths and Oathbreakers](PALADIN_OATHS_AND_OATHBREAKERS.md), and [reviewed ordinary spells](SPELL_PLAYTEST_STARTER.md). The older prestige and level-table descriptions below do not add grants to those schedules. The companion has not yet been verified against the complete current packet; a displayed or saved choice alone does not prove it is legal under that packet.

**Product:** Decennium Descent companion (`DecenniumDescent-main`)  
**Audience:** Collaborators running playtest chargen and reviewing level progression  
**Terminology:** [`src/data/CONTINUITY_GLOSSARY.md`](../../src/data/CONTINUITY_GLOSSARY.md) · [`CONTINUITY_SOURCE_OF_TRUTH.md`](./CONTINUITY_SOURCE_OF_TRUTH.md)  
**Last updated:** 2026-07-29 (Worker B — chargen pass; Continuity overnight sync)

---

## Overview

The companion builds Aethel heroes in **Character Builder** → saves to localStorage → displays in **Character Sheet** → can be loaded into **Session Tracker** for combat notes. Progression data spans L1–10 rulebook canon in `class-details.js`, L11–20 **draft milestones** in `class-draft-levels.js`, and class-specific path modules (Oracle mysteries/curses, Paladin Sacred Oaths, Druid circles).

```
Origin (People, Class, Feats, Past)
  → Abilities & Level (scores, XP, L1–20)
  → Features (class levels, arch/hero paths, subclass pickers)
  → Weave tab (RP casters) OR Revelation UI (Oracle)
  → Appearance → Save / Export JSON → Sheet / Session
```

---

## End-to-end chargen flow

### 1. People (race & lineage)

| Step | UI tab | Data | Canon status |
|------|--------|------|--------------|
| Choose people | Origin → People | `builder-races.js` | Rulebook races |
| Lineage (subrace) | optional dropdown | `racial-variants.json` | Canon where listed |
| Ability score generation | Abilities column | Random 4d6 drop lowest · 27-point buy · standard array | Standard TTRPG methods |
| Racial ASI | auto-applied | Parsed from race; **OR** choices skipped until player picks | **ASK OWNER** if a subrace ASI choice UI is required at chargen |

**Save fields:** `race`, `subrace`, `abilities[]`

### 2. Class (17 canon base classes)

| Step | UI | Data source | Notes |
|------|-----|-------------|-------|
| Base class | Origin → Class **or** class summary in Features | `canon-classes.js` → `CANON_CLASSES` | **17 selectable classes only** |
| Arch / prestige path | Class tab + Features tab | `prestige.js` ← `prestige-lorebook.json` | Optional at chargen; normally L10+ unlock |
| Proficiencies | Proficiencies tab | `class-details.js` | Armor, weapons, tools, skills |

**Save fields:** `class`, `archClass`

**Optional multiclass (Weave RP only):**

| Step | UI | Save fields | Notes |
|------|-----|-------------|-------|
| Secondary class | Origin → Class → **Secondary class** dropdown | `secondaryClass` | Any of the 17 canon classes except primary; empty = single-class |
| Secondary level | **Secondary level** dropdown (L1–20) | `secondaryLevel` | Used with primary `level` for `mergeMulticlassMaxRp()` |

Formula: [`RESONANCE_CANON.md`](./RESONANCE_CANON.md) §7 — highest Weave caster pool + ⌈25% of secondary max⌉. Session Tracker reads the same fields when a saved PC is loaded.

**Manual JSON (no Builder):** add to export/save payload:

```json
{
  "class": "Wizard",
  "level": 10,
  "secondaryClass": "Cleric",
  "secondaryLevel": 6
}
```

Or use `classLevels: { "Wizard": 10, "Cleric": 6 }` — both shapes are parsed by `parseMulticlassLevels()` in `resonance-economy.js`. Oracle multiclass is not supported in RP math (Oracle uses RC, excluded from Weave pools).

**Not in picker (reference only):**

- **Fighter** — legacy compatibility alias only; prestige/save references map to **Warrior** where required.
- **Swashbuckler** — orphan entry in `class-details.js`; never exposed in UI.

### 3. Subclass / path picks (required for complete sheet)

| Class | Pick | Level | UI location | Save field | Canon vs draft |
|-------|------|-------|-------------|------------|----------------|
| **Oracle** | Mystery | L1 | Features | `oracleMystery` | Ancestor + **Shadow** approved; Spiral-Touched rulebook-complete; 8 others `draft: true` |
| **Oracle** | Oracle's Curse | L1 | Features | `oracleCurse` | Spiral-Touched rulebook-complete; 9 others `draft: true` |
| **Paladin** | Sacred Oath | L3 | Features | `sacredOath` | **Grief** approved; Mercy + 8 others `draft: true` (Mercy has rulebook prose, not promoted) |
| **Druid** | Circle | L2 | Features | `druidCircle` | 7 circles in `druid-shapeshifting.js` |

The builder surfaces **required** warnings (red) when these are missing at the appropriate level. Oracle Mystery + Curse are required as soon as Oracle is selected.

### 4. Feats

| Step | UI | Data |
|------|-----|------|
| Browse / take feats | Origin → Feats | `feats.js` |
| Prestige feat gating | Features → Arch path panel | Parsed from prestige `requirements` via `prestige-utils.ts` |

Feat names in prestige requirements are cross-checked against `feats.js` (0 missing names as of continuity pass). UI shows ✓/○ badges for prerequisite feats vs feats on the sheet.

### 5. Background & alignment

| Step | UI | Save field |
|------|-----|------------|
| Background | Origin → Past | `background` |
| Alignment | Abilities / meta | `alignment` |

### 6. Weave vs Revelation Caster

| Class type | Magic UI | Pool label | Spell lists on sheet |
|------------|----------|------------|----------------------|
| Wizard, Mage, Cleric, Druid, Bard, etc. | Weave tab | **Resonance Points (RP)** | `knownSpells`, `preparedSpells` |
| Oracle | Features tab (Mystery / Curse) | **Revelation Charges** (3 at L1, max 7) | None — Mystery Revelations only |
| Martial / third-caster | Weave tab optional browse | RP slider if applicable | Optional |

Oracle is excluded from `isSpellcasterClass()` in `spell-utils.js`.

### 7. Level & XP (L1–20)

| Step | UI | Data |
|------|-----|------|
| Level slider / XP input | Abilities column | Hardcoded XP thresholds (L1–20) |
| Class features by level | Features → LevelFeatureList | `class-details.js` + merged `class-draft-levels.js` |
| Arch / hero paths | Features → ClassPathDisplay | `class-paths.js` |

**L11–20 display:** Where the rulebook lacks per-level tables, `class-draft-levels.js` supplies milestones marked **Draft** in UI. Oracle and Paladin have L1–20 feature strings in `class-details.js` (rulebook-aligned prose; not all tiers have full mechanical trees in companion data).

### 8. Appearance

Stub mannequin / modular slots in `CharacterAppearance.tsx` — immersion and future engine handoff, not ripped MMO assets.

**Save field:** `appearance`

### 9. Save, export, sheet

| Action | Behavior |
|--------|----------|
| **Save** | `upsertCharacter()` → localStorage key `dd_characters` |
| **Export JSON** | Full payload including subclass ids, feats, spells, RP |
| **Sheet view** | `CharacterSheet.tsx` — print-friendly; shows warnings, prestige feat status, subclass blocks |
| **Session** | Saved characters can be added to combat; oath/circle/mystery/curse ids appear in notes when set |

**Normalized save shape:** `character-storage.js` → `normalizeCharacter()` — see glossary table for all fields.

---

## Canon vs draft — quick reference

| Content | Rulebook canon | Aethel draft (`draft: true`) |
|---------|----------------|------------------------------|
| 17 base classes | Classes Table in `canon-classes.js` | — |
| Oracle mysteries | Ancestor | Battle, Bones, Cataclysm, Dream, Flame, Life, Shadow, Stars, Time |
| Oracle curses | Spiral-Touched | Nine others |
| Paladin oaths | Mercy | Nine others |
| L1–10 class features | `class-details.js` (most classes) | See current roadmap/draft flags |
| L11–20 milestones | Oracle, Paladin, Druid (partial in class-details) | Most classes via `class-draft-levels.js` |
| Prestige paths (18) | `prestige-lorebook.json` prose | Unlock narratives are table guidance, not enforced in software |

UI shows **(draft)** or **Draft** badges; do not treat draft trees as final without author promotion.

---

## Prestige / arch paths

- **18 prestige paths** in `prestige-lorebook.json` (Battlemage, Beastmaster, Blademaster, …).
- Filtered by base class via `prestigeForBaseClass()` in `prestige.js`.
- Requirements string includes: base class (Lv 10+), **feat list**, skills, alignment, and narrative **unlock** condition.
- Companion **does not enforce** narrative unlocks or skill ranks — only surfaces requirements and missing feats for playtest planning.
- **Gravetouched** is prestige path #10 (`prestige-lorebook.json`), with base classes Cleric/Warrior/Crimson Agent (Lv 10+) already defined. It is **not** a Bloodbound prerequisite (Bloodbound = Crimson Agent or Thief Lv 10+ only; owner 2026-07-29). **Closed 2026-07-29 overnight** (was ASK OWNER #6, false escalation): it is a prestige-only path, not a future base class or alias — hero-path wiring may proceed against the existing prestige entry; individual feat blurbs may still be thin/draft pending author polish.

---

## ASK OWNER — do not invent policy

These items block full canon policy in code/docs. Escalate to the human author; do not add an 18th class, expose Fighter/Swashbuckler, or rewrite mystery/oath trees without sign-off.

| # | Topic | Current product stance | Status |
|---|-------|------------------------|--------|
| 1 | **Class roster** | Player Rulebook and companion both use **17 selectable base classes**. | **Resolved and aligned.** |
| ~~2~~ | ~~**Fighter chapter**~~ | Full chapter in rulebook; **not** in Classes Table. Warrior + Soldier cover martial roles. | **Resolved (owner 2026-07-29):** archive/reference only; not in builder. |
| ~~3~~ | ~~**Swashbuckler**~~ | Orphan in `class-details.js` only. | **Resolved (owner 2026-07-29):** hidden from picker for v1. |
| ~~4~~ | ~~**Gravetouched**~~ | Prestige #10; not in `CANON_CLASSES`; not a Bloodbound prereq. | **Closed (Director + Continuity, 2026-07-29 overnight):** false escalation — Gravetouched already has a full `prestige-lorebook.json` entry (base classes Cleric/Warrior/Crimson Agent, Lv10+). It is a prestige-only path, not a future base class or alias. Feat blurb text may stay draft/thin, but do not re-block hero-path wiring on this. |
| 5 | **Oracle / Paladin draft promotion** | 18 of 20 oath/mystery/curse trees marked draft. | Which docx extracts are ready to promote? |
| 6 | **L11–20 draft milestones** | `class-draft-levels.js` pending author review. | Replace with rulebook tables when available? |
| 7 | **Feat slots by level** | Builder does not auto-grant ASI/feats by level. | Enforce rulebook feat progression in UI? |
| 8 | **Racial ASI “OR” choices** | Skipped in auto-apply until manual scores. | Add explicit picker at chargen? |
| 9 | **Prestige narrative unlocks** | Display-only. | Should Session or Builder track unlock state? |
| ~~10~~ | ~~**Dungeon `entryClasses`**~~ | Placeholder in `dungeon-mechanics.json`. | **Draft-filled (Director default, 2026-07-29 overnight):** all 17 `CANON_CLASSES` eligible; per-tier `victoryConsequences` drafted from `floor-encounters.json` themes. Both `draft: true` — promote/revise if a rulebook Ch XII source is found. |

---

## Playtest chargen checklist

Use this when reviewing a hero before a session:

- [ ] **People:** race (+ lineage if used); abilities generated; racial ASI applied or noted
- [ ] **Class:** one of 17 canon classes; no Fighter/Swashbuckler in export JSON
- [ ] **Oracle only:** Mystery **and** Oracle's Curse selected (L1)
- [ ] **Paladin only:** Sacred Oath selected before L3 scenes
- [ ] **Druid only:** Circle selected before L2 Shapeshifting
- [ ] **Feats:** chosen feats listed; if arch path selected, prestige feat prerequisites visible (✓ on sheet)
- [ ] **Background & alignment** filled if table cares
- [ ] **Weave casters:** known/prepared spells sensible for level; RP slider set
- [ ] **Oracle:** no Weave spell list expected; Revelation Charge note on sheet
- [ ] **Level / XP:** matches intended tier (L10+ if prestige path selected)
- [ ] **Features tab:** L11–20 rows show **Draft** where expected — confirm with author if relying on draft text
- [ ] **Save + Export:** JSON includes `sacredOath`, `druidCircle`, `oracleMystery`, `oracleCurse`, `archClass`, `feats`, `resonancePoints`, and optional `secondaryClass` / `secondaryLevel` if multiclass
- [ ] **Sheet warnings:** no red “Required picks missing” banner
- [ ] **Print / Session:** sheet readable; Session notes include subclass ids when loaded

---

## Key files (Worker B scope)

| File | Role |
|------|------|
| `src/components/CharacterBuilder.tsx` | Full chargen UI |
| `src/components/CharacterSheet.tsx` | Print/export sheet |
| `src/components/ChargenWarnings.tsx` | Required/advisory pick banner |
| `src/components/PrestigeRequirements.tsx` | Prestige feat prerequisite display |
| `src/components/LevelFeatureList.tsx` | L1–20 features + Draft badges |
| `src/components/ClassPathDisplay.tsx` | Arch / hero path blocks |
| `src/lib/chargen-validation.ts` | Warning rules |
| `src/lib/prestige-utils.ts` | Feat parsing from prestige reqs |
| `src/lib/character-storage.js` | Save normalization |
| `src/data/canon-classes.js` | 17-class roster SOT |
| `src/data/class-details.js` | Proficiencies + level features |
| `src/data/class-draft-levels.js` | Draft L11–20 |
| `src/data/oracle-mysteries.js`, `oracle-curses.js` | Oracle paths |
| `src/data/paladin-oaths.js` | Sacred Oaths |
| `src/data/druid-shapeshifting.js` | Circles & forms |
| `src/data/prestige.js`, `prestige-lorebook.json` | Prestige paths |

**Out of scope (this pass):** SessionTracker deep rewrites, dungeon/encounter generators, bestiary cleanup.

---

## Validation

After changes to chargen components:

```bash
npx tsc --noEmit
```

Manual smoke: build Oracle (mystery + curse), Paladin L5 (oath), Druid L5 (circle), Warrior L12 with Blademaster arch — confirm warnings, sheet blocks, and export JSON fields.
