# Crafting v4 migration

- Legacy runtime archived: **623 recipes** (main archive 2026-08-05 + earlier ReviewBible archive)
- Canonical v4 database: **687 recipes** (`data/crafting/Decennium_Descent_Crafting_Bible_v4.json` on main)
- Player runtime: **433 public recipes** (`src/data/crafting-recipes.json` — **live on main** after 2026-08-05 cutover)
- Restricted Sixth-Gate formulas: **39**
- Director-only unknown formulas: **215**
- Stable legacy IDs retained: **623**

The full v4 JSON is the mechanical Source of Truth. Player builds ingest only records marked `visibility: public`.

Main cutover report: `docs/canon/MAIN_CUTOVER_V6_2026-08-05.md` · crafting note: `docs/crafting/CRAFTING_V4_MAIN_CUTOVER_2026-08-05.md`.
