# Bestiary lore quality pass — 2026-07-30

**Status:** complete (owner sign-off review ready)  
**Owner:** sign-off to apply lore-aligned Excel changes (established lore only; no new cosmology).

## Summary for owner review

1. **Excel** (`Bestiary.xlsx`) received a lore-aligned quality pass: Gate Guardian floors, IP/deity renames, culture Type normalization, archetype Type fixes, provisional attack polish.
2. **Xarog bug fixed:** sheet had only `Xarog the Pactbound Furnace` (no comma). Script now aliases/renames → `Xarog, the Pactbound Furnace` and applies Fiend / Huge / Lawful Evil / **CR 24** / XP 62000 / Zone **Pactbound Arena** / Tags Gate Guardian. No duplicate Xarog rows in Excel or JSON.
3. **Ingest refreshed:** `npm run ingest:bestiary` → `src/bestiary_data_full.json` (785 creatures after alias/IP dedupe). Ingest now canonicalizes override names (IP renames + Xarog alias) and lets **Excel win CR/XP** for guardians when present.
4. **Scrub sync:** quality-pass `RENAMES` merged into `scripts/scrub_bestiary_ip.py` `RENAME_MAP` so future scrub stays consistent.
5. **HORN_AT / Session code:** **purged 2026-07-31** to `HORN_AT = 1200` / Opening **2400 h** — see [`OPENING_CLOCK_PURGE_2026-07-31.md`](./OPENING_CLOCK_PURGE_2026-07-31.md). (This lore pass itself did not touch Session.)

## Gate Guardian CR ladder (spot-checked Excel + JSON)

| Seal | Type | Zone | CR | XP | Alignment |
|------|------|------|----|----|-----------|
| Vaskor, the Stone Maw | Elemental | Yieldheart Caverns | 8 | 3900 | Neutral |
| The Bloom That Hungers | Plant | Bloomdeep Marsh | 11 | 7200 | Chaotic Evil |
| Ashthirst the Hollow | Elemental | Anvil of Brogi | 14 | 11500 | Neutral Evil |
| Gor Vekk, Architect of Ends | Aberration | Isles of Eternal Radiance | 17 | 18000 | Lawful Evil |
| Choralith, Voice Below | Aberration | Sanctum of Echoing Choirs | 20 | 25000 | Neutral |
| Lumen of the Shattered Thread | Elemental | Crossroads of the Shattered Thread | 22 | 41000 | Chaotic Neutral |
| **Xarog, the Pactbound Furnace** | **Fiend** | **Pactbound Arena** | **24** | **62000** | **Lawful Evil** |
| Eirfax, the Dusk Crowned | Fey | Duskshard Pools | 26 | 90000 | Neutral Evil |
| Threxus, the Iron Spiral | Construct | Veiled Iron Spiral | 28 | 120000 | Lawful Neutral |
| The Marquis of Silence | Fiend | Silencebound Void | 30 | 155000 | Chaotic Evil |

All ten tagged `Gate Guardian`. Single Xarog row (comma form only).

## Sample renames (Excel + JSON)

Present under new names (old IP names absent from JSON after ingest canonicalize):

- Flumph → Lumen Drifter  
- Owlbear → Hookbeast  
- Tarrasque → Worldbreaker  
- Intellect Devourer → Mind Leech  
- Drider → Umbrin Arachnid  
- (+ full deity/yugoloth/modron/slaad/eladrin/star-spawn/demon-line set in script)

## Backups

- First pass: `backups/Bestiary_pre_quality_20260730_200944.xlsx`
- Xarog fix re-run: `backups/Bestiary_pre_quality_20260730_201212.xlsx`
- Idempotent re-stamp: `backups/Bestiary_pre_quality_20260730_201423.xlsx`

## Scripts touched

- `scripts/bestiary_lore_quality_pass.py` — guardian alias resolve (rename-only → canonical; delete if both); Xarog no-comma alias; idempotent re-run safe
- `scripts/scrub_bestiary_ip.py` — `RENAME_MAP` extended with lore-pass renames
- `scripts/ingest_bestiary_from_excel.py` — `canonicalize_name` (IP + aliases); override keys remapped; Excel CR/XP win for guardians; no stale extra rows for renamed aliases

## Ingest confirmation

```
npm run ingest:bestiary
→ primary Bestiary.xlsx, supplement final_bestiary.xlsx
→ excel_rows 708, json_rows 785, skipped_hidden 1
→ src/bestiary_data_full.json refreshed
```

## Known debt (no silent rulebook overwrite)

- **Session Horn clock:** **Aligned 2026-07-31** — `HORN_AT = 1200` / Opening **2400 h** ([`OPENING_CLOCK_PURGE_2026-07-31.md`](./OPENING_CLOCK_PURGE_2026-07-31.md)).
- **Sandbox combat shells:** many creatures still have provisional AC/HP/CR from excel-sandbox (e.g. Hookbeast/Worldbreaker combat numbers are not “true” legendary budgets). Lore renames + Types are fixed; deep combat authorship is separate.
- **Xarog attack labels:** still Elemental-flavored (`Elemental Slam` / `Surge Burst`) from pre-fix Type; Type/Zone/CR/Alignment/Tags/Description are correct. Optional polish later.
- **Young Red Shadow Dragon:** Type heuristic can flip Shadow→Undead then Dragon on re-run; currently Dragon. Confirm preferred Type if owner cares.
- **Quality-pass log overwrite:** re-running the script regenerates the short run log section; this stamped summary is the owner-facing record.

## First-pass change log (excerpt)

First run applied ~211 renames/type/attack fixes (deleted 0). Second run fixed Xarog alias + re-stamped all 10 guardians. Representative renames from first pass:

- RENAME Flumph → Lumen Drifter
- RENAME Tarrasque → Worldbreaker
- RENAME Owlbear → Hookbeast
- RENAME Intellect Devourer → Mind Leech
- RENAME alias Xarog the Pactbound Furnace → Xarog, the Pactbound Furnace
- GATE fix all 10 seals to CR ladder above

---

**Todos:** audit done · Excel fixes applied · ingest done · log stamped.
