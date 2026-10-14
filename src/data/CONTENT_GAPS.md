> **Historical report (July 2026).** Some counts and completion claims below are superseded. Use [the October recovery audit](../../docs/audit/2026-10-08/AUDIT_REPORT.md) and [advancement matrix](../../docs/audit/2026-10-08/ADVANCEMENT_MATRIX.md) for the current source comparison. Original findings remain below for provenance.

# Decennium Descent — Content Gap Summary

**Audit date:** 2026-07-29 · **Continuity pass:** 2026-07-29 · **Canon:** rulebook / lorebook first · **Out of scope:** SWTOR assets, Unity client

Structured machine report: [`content-gap-report.json`](./content-gap-report.json) · Continuity audit: [`CONTINUITY_REPORT.md`](./CONTINUITY_REPORT.md)

---

## Top 10 high-priority gaps

1. **Feats compendium reconciliation** — 336 live vs 330-title doc; placeholder descriptions; root `game-data.js` / `additional-feats.js` unwired. *Sibling agent: feats ingest.*
2. **Cosmology First Song chapters** — Single blob + incomplete chapter index (IX–XII). *Split extract; draft synthesized nav.*
3. **Global header search** — Input is non-functional. *Client index over existing data only.*
4. **Reputation system** — Backgrounds store `startingReputation` only; rulebook Ch4 faction tracking not in Session/Characters. *Draft tracker from rulebook mechanics.*
5. **L11–20 class progressions** — `class-draft-levels.js` fills many classes with **`draft: true`** placeholders; Oracle/Paladin/Cleric upper tiers still thin. *Author review.*
6. ~~**Swashbuckler canonicality**~~ — **Resolved (owner final 2026-07-29):** not in Classes Table; orphan data in `class-details.js` only; hidden from builder/sheet pickers; stays orphan for v1.
7. ~~**Fighter (rulebook only)**~~ — **Resolved (owner final 2026-07-29):** full rulebook chapter but absent from Classes Table; not added to builder; Warrior/Soldier cover martial roles; archive/reference only for v1.
8. **Session shapeshift tracker** — Druid forms wired in Character Builder; bestiary filters / Session wild-shape tracking still unwired.
9. **Paladin oath docx parity** — Mercy oath fully from rulebook; 9 other oaths have draft revelation lists pending `Paladin_Oaths_*.docx` author review.
10. ~~**Oracle mystery tier bodies (9 of 10 in player rulebook)**~~ — **Partially resolved:** all 10 mysteries + 10 curses wired with full playable trees in `oracle-mysteries.js` / `oracle-curses.js`. **Ancestor + Spiral-Touched** rulebook canon; **Battle–Time mysteries + 9 curses** are Aethel draft (`draft: true`) pending author review.

**Resolved this audit:** Monk & Dragoon in Character Builder; **17-class Classes Table** wired via `canon-classes.js` (Swashbuckler orphan/hidden, Fighter excluded); Paladin Sacred Oaths module + UI; Druid shapeshifting ingest + UI; Druid/Oracle/Paladin class-paths; **Oracle mysteries + curses modules (10 each, Ancestor/Spiral-Touched canon, rest Aethel draft)** + Character Builder/Sheet pickers; dungeon `gateBosses` wired.

**Continuity pass (2026-07-29):** Oracle Weave tab corrected (Revelation Charges, not spell slots); Druid class-paths now list all 7 circles; Oracle L1 features aligned; Session notes include oath/circle/mystery/curse; prestige feat refs validated. See [`CONTINUITY_REPORT.md`](./CONTINUITY_REPORT.md). **Overnight queue:** [`docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md`](../docs/mechanics/OVERNIGHT_VAGUE_QUEUE.md).

**Rulebook prose "eighteen":** Confirmed book typo. **v1 ships 17 base classes per Classes Table** (`canon-classes.js`). Fighter and Swashbuckler stay archive/orphan — not selectable. Owner final 2026-07-29 — do not add an 18th class.

---

## What is in good shape

| Area | Live | Source | Status |
|------|------|--------|--------|
| Backgrounds | 20 | Rulebook Ch4 / `Backgrounds.docx` | ok |
| Prestige paths | 18 | `prestige-lorebook.json` / prestige docx | ok |
| Spells | 832 | School docx + rebalance MD | mostly ok |
| Crafting | 623 recipes | Validated xlsx | ok |
| Encounters / tiers | 10 tiers | `Floor Encounters.docx` | partial (narrative ok) |
| Monsters | 718 | `final_bestiary.xlsx` | ok (file outside `src/data/`) |
| Races + variants | 14 + 42 | Rulebook + racial feats doc | partial |

---

## Actionable next steps (by owner)

### Wire now (thin, no new lore)

- Move **bestiary** canonical JSON to `src/data/` via existing ingest script.
- Implement **header search** over ingested modules.
- **Session tracker:** Druid wild-shape uses + form CR filters (forms live in `druid-shapeshifting.js`).

### Sibling agents — draft allowed (`draft: true` in report)

- **Feats:** reconcile 330 compendium, remove placeholders.
- **Paladin oaths:** expand 9 oaths from `Paladin_Oaths_*.docx` (Mercy complete; others draft revelation lists).
- ~~**Oracle mysteries:** full tier I–III for 9 mysteries~~ — **Done (draft):** playable Aethel trees in `oracle-mysteries.js`; author review to promote from draft.
- ~~**Oracle curses:** full boon trees for 9 curses~~ — **Done (draft):** playable Aethel trees in `oracle-curses.js`; Spiral-Touched canon.
- **Cosmology:** per-chapter JSON from TXT extracts.
- **Reputation tracker** on saved characters (rulebook mechanics only).

### Author decision required

- ~~**Swashbuckler**~~ — resolved: orphan reference in `class-details.js`; not selectable.
- ~~**Fighter**~~ — resolved: not in Classes Table; archive/reference only; not in builder.
- **`class-draft-levels.js`** — approve or replace draft L11–20 milestones.

---

## Source doc inventory (repo root)

**Rulebook:** `decennium descent player rulebook.docx`, `rulebook_output.txt`

**Characters:** `Backgrounds.docx`, racial feats docx, prestige docx, Paladin docs (3), `Druid_Shapeshifting_System.docx`

**Feats:** 330 compendium + combat/magic/skill feat docx, `additional-feats.js`

**Spells:** 9 school docx + 9 rebalance/expanded MD, `class_spell_school_mapping.csv`

**Dungeon:** `Floor Encounters.docx`, floor encounter TXT extracts

**Bestiary:** `final_bestiary.xlsx`, `bestiary_data.json` (stale 50-row subset)

**Crafting:** `decennium_descent_crafting_recipes_validated.xlsx`

**Cosmology / world:** Cosmology docx + extracts, World of Aethel docx + extract

**Legacy (unwired):** `game-data.js`, `script.js`, `ENHANCED-FEATURES.JS`, `COSMOLOGY-VIEWER.JS`
