# Crafting v4 — main cutover (2026-08-05)

**Scope:** Main approved-release runtime + mechanical dataset  
**Prior ReviewBible-only install:** `docs/crafting/CRAFTING_V4_REVIEWBIBLE_INSTALL_2026-08-05.md` (historical)

## Actions

1. Archived main live **623** recipes → `archive/main-pre-v6-cutover-2026-08-05/src/data/crafting-recipes.json`
2. Legacy easy-find mirror → `src/data/legacy/crafting-recipes-v1-623.pre-v6-cutover-2026-08-05.json`
3. Installed mechanical SoT **687** recipes / **696** materials → `data/crafting/Decennium_Descent_Crafting_Bible_v4.json`
4. Replaced live companion runtime with ReviewBible public **433** → `src/data/crafting-recipes.json`
5. Installed Director Full Internal JSON → `data/director/Decennium_Descent_Crafting_Bible_v4_Full_Internal.json`
6. Player / Director publications under `books/player/` and `books/director/`
7. Migration notes present at `docs/migrations/CRAFTING_V4_MIGRATION.md` (+ `.json`)

## Counts after main cutover

| Dataset | Count |
|---------|------:|
| Archived prior main runtime | 623 |
| V4 mechanical bible | 687 |
| Materials in v4 bible | 696 |
| Public companion runtime (main live) | **433** |
| ReviewBible runtime (mirror) | 433 |

## Visibility split (from v6 migration)

- Public: 433  
- Restricted Tier VI: 39  
- Director-only: 215  
- Total: 687  

Stable legacy IDs retained across migration: 623 (per v6 migration notes).

## App expectation

`CraftingBuilder` imports `@/data/crafting-recipes.json` as an **array** of recipes with `components` + `resultItem`. The 433 public runtime matches that shape (validated on cutover).
