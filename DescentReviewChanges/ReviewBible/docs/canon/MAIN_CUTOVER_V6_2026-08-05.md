# Main cutover — DecenniumDescentv6 / ReviewBible → main

**Date:** 2026-08-05  
**Owner order:** Explicit authorization — **Move it to main**  
**Source of truth used:** `DescentReviewChanges/ReviewBible/` (already promoted from V6); `DecenniumDescentv6/` / `incoming/DecenniumDescentv6/` referenced only as fallback (not required for missing books — RB was complete)

**ReviewBible:** **retained** (not deleted)  
**Git commit / force-push:** **not performed** (not requested)

---

## Verdict

Main approved release is **cut over**. Live companion and published book/data paths now match the ReviewBible-assembled V6 build for crafting, spells, feats, Player Rulebook v6, Core Systems, MM Source Pack, and related companion `src/` updates. Continuity ops (`CANON_MANIFEST`, activity logs, trackers) were merged carefully — not wiped.

---

## Rollback snapshot

| Location | Contents |
|----------|----------|
| `archive/main-pre-v6-cutover-2026-08-05/` | Pre-overwrite copies of live companion data, key UI, Player Rulebook, Core Systems v1 root files, MM pack (83 files), truncated bestiary |
| `archive/main-pre-v6-cutover-2026-08-05/ARCHIVE_MANIFEST.json` | Inventory metadata |
| `src/data/legacy/crafting-recipes-v1-623.pre-v6-cutover-2026-08-05.json` | Easy-find mirror of archived **623** runtime |
| `src/data/legacy/bestiary_data_full.truncated-262144.pre-v6-cutover.json` | Truncated pre-cutover bestiary (256 KiB corrupt) |

**Rollback:** restore files from `archive/main-pre-v6-cutover-2026-08-05/` over the corresponding main paths (crafting 623, spells 832, feats 336, prior rulebook, prior MM 83, etc.). Do **not** restore the truncated bestiary as live — use RB/main post-cutover full file or a known-good backup.

---

## Crafting counts

| Layer | Path | Recipes |
|-------|------|--------:|
| **Main live (after)** | `src/data/crafting-recipes.json` | **433** |
| **Archive (before)** | `archive/.../src/data/crafting-recipes.json` | **623** |
| **Legacy mirror** | `src/data/legacy/crafting-recipes-v1-623.pre-v6-cutover-2026-08-05.json` | **623** |
| **Mechanical SoT** | `data/crafting/Decennium_Descent_Crafting_Bible_v4.json` | **687** (+ **696** materials) |
| Director Full Internal JSON | `data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json` | (full internal twin) |

Runtime shape remains a **JSON array** with `id` / `components` / `resultItem` — compatible with `CraftingBuilder`. Visibility split (from v6 migration): public 433 / restricted T6 39 / director-only 215 = 687.

Migration notes: `docs/migrations/CRAFTING_V4_MIGRATION.md` (+ `.json`), `docs/crafting/CRAFTING_V4_MAIN_CUTOVER_2026-08-05.md`.

---

## What was promoted onto main

### Books — player (`books/player/` + root aliases)
- `Decennium_Descent_Player_Rulebook_v6.docx` → also `decennium descent player rulebook.docx`, `rulebook_output.txt`, `docs/manuals/Decennium_Descent_Player_Rulebook_v6.docx`
- `Decennium_Descent_Core_Systems_Bible_v2_Known_Descent.docx`
- `Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx`
- `Decennium_Descent_Feat_Compendium_v1.docx`
- `Decennium_Descent_Monster_Manual_of_the_Known_Descent_v2.docx`

### Books — director (`books/director/` — director visibility)
- `Decennium_Descent_Core_Systems_Bible_v1_Full_Director.docx`
- `Decennium_Descent_Crafting_Bible_v4_Full_Internal.docx`
- `Decennium_Descent_Directors_Sealed_Bestiary_v1.docx`
- Visibility note: `docs/manuals/DIRECTOR_MATERIALS_VISIBILITY.md`

### Structured data
- `data/crafting/` (v4 mechanical)
- `data/public/` + `data/director/` (Core Systems + crafting internal)
- `docs/manuals/core-systems/`
- `docs/migrations/`, `docs/feats/`, `docs/crafting/`

### Companion `src/`
- `crafting-recipes.json` (433)
- `spells.js` (**848**; was 832) + `spell-placements.json` + `spell-utils.js` + `class-spell-progression.js`
- `feats.js` (**335**; was 336)
- `racial-variants.json`, `haven.json` (new), `resonance-economy.js`, `prestige-lorebook.json`
- `class-details.js` + `class-core-mechanics.js` (new)
- `dungeon-mechanics.json`
- `DungeonGuide.tsx`, `MonstersLibrary.tsx`, `SpellsLibrary.tsx`, `CharacterBuilder.tsx`, `CharacterSheet.tsx`, `SessionTracker.tsx`
- `src/lib/character-storage.js`, `session-utils.ts`
- `src/bestiary_data_full.json` — **fixed**: pre-cutover main file was truncated at 262144 bytes; replaced with ReviewBible full catalog (**707** entries)

### Monster Manual
- Live pack replaced with ReviewBible merged Source Pack (**85** files; archive retained prior **83**)

### Tooling
- `tsconfig.json` `exclude` extended: `archive`, `backups`, `DecenniumDescentv6`, `DescentReviewChanges`, `out`, `.next` (prevents archived `.tsx` + truncated JSON from failing `tsc`)

---

## Preserved (not wiped)

- Activity logs / continuity trackers / `docs/canon/CANON_MANIFEST.json` (updated, not deleted)
- ReviewBible tree intact
- Incoming / DecenniumDescentv6 historical stage copies
- Existing Director manuals already on main (DM-01, Cosmology, Matrix, World, Floor Encounters, etc.) outside this pack — not deleted

---

## Validation

| Check | Result |
|-------|--------|
| Crafting live count | **433** array; archive/legacy **623** |
| Spells keys | **848** (matches RB) |
| Feats length | **335** (matches RB) |
| MM pack files | **85** live / **83** archived |
| CraftingBuilder shape | array + `resultItem` + `components` OK |
| Module import smoke (spells/feats/haven/class-core/class-spell-progression) | OK |
| `bunx tsc --noEmit` | **Pass** after bestiary repair + tsconfig exclude |

### Validation notes / non-blockers
- Root `Decennium_Descent_Core_Systems_Bible_v1.docx` + `Data_v1.json` remain as historical root copies; authoritative public layer is **v2** under `books/` + `data/public/` (+ manuals mirror). Director Full lives under `books/director/` + `data/director/`.
- `Feats and Skills Overview.txt` still **pending-locate**.
- Optional follow-up: reconcile fracture-kin classic-label vs scrubbed rename (both present in MM pack by design).

---

## Manifest

`docs/canon/CANON_MANIFEST.json`:
- `mainCutover.status`: **`done`**
- Domains previously `pending-main-cutover` → **`mainCutoverStatus: done`**
- Authoritative paths prefer **main** live locations; ReviewBible listed under `alsoPresentAt` / review-build mirror
- `pendingDeliveries.DecenniumDescentv6.status`: **`cut-over-to-main`**
