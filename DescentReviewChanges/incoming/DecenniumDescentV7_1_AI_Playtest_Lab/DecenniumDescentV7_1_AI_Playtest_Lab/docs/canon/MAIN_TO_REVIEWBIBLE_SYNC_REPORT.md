# Main → ReviewBible baseline sync report (§11)

**Date:** 2026-08-05  
**Direction:** **One-way** `DecenniumDescent-main` → `DescentReviewChanges/ReviewBible`  
**Policy after this sync:** Future canon revisions in **ReviewBible / DescentReviewChanges**; **no auto-promote** back to main.  
**Supersedes for this baseline only:** prior “ReviewBible always wins” when that would leave RB **missing** main companion baseline. Ongoing drift audits still prefer RB for books; companion data should now be **at least** main’s baseline, with RB-ahead files preserved.

---

## Spell catalogs (special case)

| Tree | Path | Count | Disposition |
|------|------|------:|-------------|
| Main | `src/data/spells.js` | **832** unique `SPELLS` keys (legacy schema) | **Not copied over RB** |
| ReviewBible | `ReviewBible/src/data/spells.js` | **848** unique spells (authoritative catalog header; 936 placements) | **Kept** — RB ahead |

Main and RB use **different schemas**; union-merge was **not** attempted this pass. Sync rule satisfied: RB retains **at least** baseline coverage and stays ahead on spells.

Related RB-only / RB-ahead spell surface also kept: `spell-placements.json`, `spell-utils.js`.

---

## Files copied main → ReviewBible (`src/data/`)

| File | Reason |
|------|--------|
| `feats.js` | Main larger / +2 IDs (`magic_initiate_sorcerer`, `magic_initiate_warlock`) |
| `canon-classes.js` | Main larger |
| `class-draft-levels.js` | Main larger |
| `class-hit-dice.js` | Main larger |
| `class-paths.js` | Main larger |
| `druid-shapeshifting.js` | Main larger |
| `oracle-mysteries.js` | Main larger |
| `prestige.js` | Main larger |
| `CONTINUITY_GLOSSARY.md` | Main larger |
| `CONTENT_GAPS.md` | Missing in RB |
| `content-gap-report.json` | Missing in RB |

**Not copied (ops / agent report):** `CONTINUITY_REPORT.md` — excluded as agent continuity report, not product companion data.

---

## Conflicts — kept ReviewBible (main not overwritten)

| File | Main bytes | RB bytes | Reason |
|------|----------:|---------:|--------|
| `spells.js` | 472415 | 1252459 | RB spell catalog ahead (848 vs 832) |
| `spell-utils.js` | 5933 | 8030 | RB larger |
| `spell-placements.json` | — | 143678 | RB-only |
| `resonance-economy.js` | 22435 | 24109 | RB larger |
| `dungeon-mechanics.json` | 9540 | 10309 | RB larger |
| `prestige-lorebook.json` | 35987 | 36133 | RB larger |
| `class-details.js` | 19221 | 19534 | RB larger |
| `class-core-mechanics.js` | — | 10715 | RB-only |
| `class-spell-progression.js` | — | 2661 | RB-only |

---

## Identical (hash match — no copy needed)

`backgrounds.js`, `builder-races.js`, `class-ceiling-caps.js`, `class-level-utils.js`, `cosmology-lore.json`, `crafting-recipes.json`, `floor-encounters.json`, `oracle-curses.js`, `paladin-oaths.js`, `races.js`, `racial-variants.json`, `reputation.js`, `t1-5-encounter-toolkit.json`, `t6-10-encounter-toolkit.json`

---

## Core Systems staging (related §5)

Staged (were root-only):

- `DescentReviewChanges/incoming/core-systems-bible-v1/Decennium_Descent_Core_Systems_Bible_v1.docx`
- `DescentReviewChanges/incoming/core-systems-bible-v1/Decennium_Descent_Core_Systems_Data_v1.json`

Authority note: [`CORE_SYSTEMS_AUTHORITY.md`](./CORE_SYSTEMS_AUTHORITY.md).

---

## Open follow-ups

1. Optional later: schema-aware **spell union** (import any main-only keys into RB catalog without demoting 848).
2. Owner promote Core Systems from `incoming/` into ReviewBible manuals lineup when ready.
3. Feat draft completion continues under `docs/feats/` — not blocked on sync.
