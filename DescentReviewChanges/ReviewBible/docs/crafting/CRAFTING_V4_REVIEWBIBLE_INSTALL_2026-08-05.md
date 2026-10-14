# Crafting v4 install — ReviewBible only (2026-08-05)

**Scope:** ReviewBible runtime + mechanical dataset (historical — pre-main cutover)  
**Main live:** Cut over 2026-08-05 — see `docs/crafting/CRAFTING_V4_MAIN_CUTOVER_2026-08-05.md` (live **433**; prior **623** archived)

## Actions

1. Archived prior ReviewBible runtime **623** recipes → `archive/legacy/crafting-recipes-v1-623.json`
2. Installed mechanical SoT **687** recipes / **696** materials → `data/crafting/Decennium_Descent_Crafting_Bible_v4.json`
3. Installed V6 public runtime **433** recipes → `src/data/crafting-recipes.json`
4. Installed Director Full Internal JSON twin → `data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json`
5. Copied pack migration notes → `docs/migrations/CRAFTING_V4_MIGRATION.md` (+ `.json`)
6. Player publication: `books/player/Decennium_Descent_Crafting_Bible_v5_Known_Descent.docx`
7. Director publication: `books/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.docx`

## Counts after install

| Dataset | Count |
|---------|------:|
| Archived legacy RB runtime | 623 |
| V4 mechanical bible | 687 |
| Materials in v4 bible | 696 |
| Public companion runtime (RB) | 433 |
| Main live runtime | 623 (not cut over) |

## Visibility split (from v6 migration)

- Public: 433  
- Restricted Tier VI: 39  
- Director-only: 215  
- Total: 687  

Stable legacy IDs retained across migration: 623 (per v6 migration notes).
