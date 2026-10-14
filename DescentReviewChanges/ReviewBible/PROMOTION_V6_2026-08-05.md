# DecenniumDescentv6 → ReviewBible promotion

**Date:** 2026-08-05  
**Owner order:** Promote DecenniumDescentv6 to ReviewBible only  
**Direction:** One-way into `DescentReviewChanges/ReviewBible/`  
**Main cutover:** **NOT done** — live main companion / `src/data/crafting-recipes.json` (623) unchanged

**Sources used:**
- `DecenniumDescentv6/` (primary)
- `DescentReviewChanges/incoming/DecenniumDescentv6/` (staged twin)
- Main MM Canon Rewrite Source Pack (merge baseline for ReviewBible MM)

---

## Verdict

V6 Consolidated is now the **assembled review-build** content for Player Rulebook v6, Core Systems (public v2 + Director v1), Crafting mechanical v4 (687) + public runtime (433), Feat Compendium / registry (335), and MM Source Pack (merged).  
**Main remains approved release** until an explicit cutover order.

---

## Crafting counts

| Layer | Path | Recipes | Notes |
|-------|------|--------:|-------|
| **Main live** | `src/data/crafting-recipes.json` | **623** | **Left unchanged** (no main cutover) |
| **RB archive** | `ReviewBible/archive/legacy/crafting-recipes-v1-623.json` | **623** | Archived pre-promote RB runtime |
| **RB mechanical SoT** | `ReviewBible/data/crafting/Decennium_Descent_Crafting_Bible_v4.json` | **687** | + 696 materials |
| **RB public runtime** | `ReviewBible/src/data/crafting-recipes.json` | **433** | V6 filtered public ingest |
| V6 director full craft JSON | `ReviewBible/data/director/…v4_Full_Internal.json` | (full internal twin) | Installed |

Migration notes also at `ReviewBible/docs/migrations/CRAFTING_V4_MIGRATION.md` (+ `.json`) and `ReviewBible/docs/crafting/CRAFTING_V4_REVIEWBIBLE_INSTALL_2026-08-05.md`.

---

## What was copied into ReviewBible

### Books — player (`books/player/`)
- `Decennium_Descent_Player_Rulebook_v6.docx` → also installed as primary alias `decennium descent player rulebook.docx`
- `Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`
- `Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx`
- `Decennium_Descent_Feat_Compendium_v1.docx`
- `Decennium_Descent_Monster_Manual_of_the_Known_Descent_v2.docx`

### Books — director (`books/director/`)
- `Decennium_Descent_Core_Systems_Bible_v1_Full_Director.docx`
- `Decennium_Descent_Crafting_Bible_v4_Full_Internal.docx`
- `Decennium_Descent_Directors_Sealed_Bestiary_v1.docx`

### Structured data
- Core Systems public v2 + Director v1 JSON under `data/public/`, `data/director/`, and mirrored under `docs/manuals/core-systems/`
- Crafting v4 mechanical JSON + Full Internal JSON (see counts above)
- `rulebook_output.txt` refreshed (was already SHA-identical to v6)

### Companion `src/` promoted from v6
- `src/data/feats.js` (335 IDs)
- `src/data/racial-variants.json`
- `src/data/haven.json` (**new** in RB)
- `src/data/crafting-recipes.json` (433 public runtime)
- `src/components/DungeonGuide.tsx`
- `src/components/MonstersLibrary.tsx`
- `docs/feats/*` status/plan/snapshot from v6

### Monster Manual
- Installed `docs/bestiary/Decennium_Descent_Monster_Manual_Canon_Rewrite_Source_Pack/` into ReviewBible
- Merge: **main baseline → overlay v6** (v6 newer `build-filters.json` + scrubbed fracture-kin entries)
- **Kept main-only classic-label entries** alongside v6 renames for review:
  - `fracture-kin-nabassu.md`, `fracture-kin-sibriex.md` (main)
  - `fracture-kin-fleshwright.md`, `fracture-kin-nightreaver.md` (v6)
- Result: **85** files in RB MM pack (vs 83 in either source alone)

### Reference snapshots
- `docs/canon/V6_PACK_CANON_MANIFEST.json`
- `docs/canon/V6_CONSOLIDATION_REPORT.md`
- `docs/canon/V6_RELEASE_CANDIDATE_STATUS.md`
- `docs/director-only/` merged from v6 with `/XO` (do not overwrite newer RB)

---

## Preserved ReviewBible-ahead (not regressing to v6)

| File | Why kept |
|------|----------|
| `src/data/spells.js` | Already **identical** to v6 (**848** catalog; no 848→832 regression) |
| `src/bestiary_data_full.json` | RB **1.3 MB** vs v6 **347 KB** — RB ahead |
| `src/data/class-details.js` | RB larger |
| `src/data/class-paths.js` | RB larger |
| `src/data/floor-encounters.json` | RB larger |
| `src/data/cosmology-lore.json` | RB larger |
| `src/data/dungeon-mechanics.json` | RB larger |
| `src/data/oracle-mysteries.js` | RB larger |
| `src/data/druid-shapeshifting.js` | RB larger |
| `src/components/EncountersBrowser.tsx` | RB larger |
| `src/data/t6-10-encounter-toolkit.json` | RB-only |
| `src/data/CONTINUITY_GLOSSARY.md` | RB-only |

Existing Director manuals (DM-01, Cosmology, Matrix, World of Aethel, Floor Encounters, etc.) were **not** deleted or replaced by this promote.

---

## Manifest status changes (`docs/canon/CANON_MANIFEST.json`)

| Domain / delivery | Before | After |
|-------------------|--------|-------|
| `pendingDeliveries.DecenniumDescentv6` | `pending-review` | **`promoted-to-ReviewBible`** |
| `crafting` | `pending-review` | **`canonical`** (review-build) — **`pending-main-cutover`** |
| `spellcasting` / `combat` / `gate-tier-scaling` / `economy` | `pending-review` (incoming v1) | **`canonical`** (review-build) pointing at RB Core Systems public **v2** + Director **v1** — **`pending-main-cutover`** |
| `feats` | `canonical` (main+RB registry) | **`canonical`** review-build paths prefer RB v6 feats (**335**) + Feat Compendium; main still **336** until cutover |
| `class-identity` / `paths` / `racial` | `canonical` | Updated to cite **Player Rulebook v6** in ReviewBible; companion main paths still live until cutover |
| MM domains | already `canonical` on main pack | RB now holds merged pack for review audits; main pack remains live SoT until cutover |

**Explicit:** main cutover is **not** done. Do not treat ReviewBible as auto-synced back to main.

---

## Incoming staging markers

- `DescentReviewChanges/incoming/DecenniumDescentv6/PENDING_REVIEW.md` → marked **promoted-to-ReviewBible**
- `incoming/README.md` + crafting-bible pending notes updated accordingly

---

## Open / follow-ups (not part of this promote)

1. Explicit owner order required for **main** cutover (623→687/433, books, feats 336↔335 reconciliation).
2. `Feats and Skills Overview.txt` still missing.
3. Optional: resolve fracture-kin classic-label vs scrubbed rename (both present in RB MM for review).
4. Optional: schema-aware spell union if main ever reintroduces keys not in the 848 catalog.
