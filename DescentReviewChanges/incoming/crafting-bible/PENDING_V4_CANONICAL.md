# Crafting Bible v4 — ReviewBible promoted; main pending cutover

**Date:** 2026-08-05  
**Status:** `promoted-to-ReviewBible` / **`pending-main-cutover`**

## Authoritative filenames (owner lock §3 / priorities #2)

| File | Status |
|------|--------|
| `Decennium_Descent_Crafting_Bible_v4_Standalone.docx` | Found (incoming + SHA-identical to Director Full Internal) |
| `Decennium_Descent_Crafting_Bible_v4.json` | **Promoted into ReviewBible** (`data/crafting/…`) — 687 recipes / 696 materials |

## ReviewBible install (2026-08-05)

- Archived RB prior runtime 623 → `ReviewBible/archive/legacy/crafting-recipes-v1-623.json`
- Mechanical SoT 687 → `ReviewBible/data/crafting/Decennium_Descent_Crafting_Bible_v4.json`
- Public runtime 433 → `ReviewBible/src/data/crafting-recipes.json`
- Player book v5 Known Descent + Director Full Internal docx installed under `ReviewBible/books/`
- Report: `ReviewBible/docs/crafting/CRAFTING_V4_REVIEWBIBLE_INSTALL_2026-08-05.md`
- Pack promote summary: `ReviewBible/PROMOTION_V6_2026-08-05.md`

## Live main app (unchanged)

- Main `src/data/crafting-recipes.json` — **still 623**
- No main cutover until explicit owner order

## Deprecate (do not treat as SoT)

- `DescentReviewChanges/crafting-bible/Decennium_Descent_Crafting_Bible_v2.docx` / `.json`
- No v3 bible files found
