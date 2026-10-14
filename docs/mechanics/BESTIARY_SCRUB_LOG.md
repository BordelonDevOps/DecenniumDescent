# Bestiary D&D / FR IP Scrub Log

**Date:** 2026-07-29  
**Owner ruling:** #4 — scrub Forgotten Realms / D&D setting leakage; use `Bestiary.xlsx` (primary) + `final_bestiary.xlsx` (metadata supplement) as name sources.  
**Status:** Complete (54 creature entries renamed in JSON + xlsx)

---

## Sources

| Asset | Path | Role |
|-------|------|------|
| Canonical xlsx | `Bestiary.xlsx` (primary names) + `final_bestiary.xlsx` (metadata supplement) | Source of truth for beast names and loot cross-refs |
| Live companion data | `src/bestiary_data_full.json` | Imported by `MonstersLibrary.tsx`, `SessionTracker.tsx`, `CraftingBuilder.tsx`, `ItemsLibrary.tsx` |
| Ingest pipeline | `scripts/ingest_bestiary_from_excel.py` | Rebuild JSON from xlsx; see `docs/mechanics/BESTIARY_INGEST.md` |
| Scrub script | `scripts/scrub_bestiary_ip.py` | Idempotent rename map; re-run after xlsx edits |

**Note:** Root `bestiary_data.json` (50-row subset) and `src/bestiary_data.json` do not contain the scrubbed names — they predate the full ingest and are not wired to the UI.

---

## Scope

Scrubbed **setting-linked and iconic SRD-protected labels** called out in owner ruling #4:

- Lolth (FR deity) and all **Drow** variants
- **Mind Flayer** / **Alhoon** (Illithid line)
- **Beholder** kin (Beholder, Death Tyrant, Gauth)
- **Githyanki** / **Githzerai**
- **Duergar**, **Kuo-toa**, **Yuan-ti**, **Svirfneblin**, **Myconid**

**Not renamed (out of scope this pass):** generic SRD creature labels still in the xlsx (e.g. Owlbear, Behir, Bulette, Displacer Beast, Flumph) — no FR deity/setting text attached; flagged for a later pass if owner wants full SRD de-brand.

**Out of scope (resolved 2026-07-29 PM):** Player race data was still "Drow" when bestiary scrub landed — see **VQ-14 / companion rename** below.

---

## Player race alignment (companion chargen)

| Was (D&D / FR) | Now (Aethel-neutral) | Notes |
|----------------|----------------------|-------|
| Drow (race name) | **Umbrin** | One-word demonym of Umbra; id `umbrin` |
| Noble Drow (subrace) | **Obsidian Highborn** | Exotic noble line; obsidian exile lore |
| Drow Magic / Drow Weapon Training | **Umbrin Magic** / **Umbrin Weapon Training** | Trait labels |
| Undercommon (language) | **Murkish** | Rulebook Murkish for Murk denizens |
| "Dark elves" (info blurb) | Obsidian-banished children of The Murk | Avoids D&D "dark elf" phrasing |

**2026-07-29 PM — Umbrin rename (Director lore pass):** Interim label **Umbral Elf** superseded by **Umbrin** across companion + bestiary (10 creature names: Umbral Elf → Umbrin, Umbral Elf Spider-Priestess → Umbrin Spider-Priestess, etc.). Lore: Calan'thir / First Choir exile, obsidian flesh, perverse Umbra worship.

**Migration:** `character-storage.js` maps saved `race: "Drow"` or `"Umbral Elf"` → `"Umbrin"` and `subrace: "Noble Drow"` or `"Noble Umbral Elf"` → `"Obsidian Highborn"` on load.

**Rulebook note:** Living `rulebook_output.txt` / Player Rulebook `.docx` scrubbed to **Umbrin** (0 whole-word Drow as of 2026-07-31 continuity re-scan).

---

## Rename families (54 bestiary entries)

| Was (D&D / FR) | Now (Aethel-neutral) |
|----------------|----------------------|
| Drow → Umbrin | Removes FR dark-elf faction label |
| Drow Priestess of Lolth → Umbrin Spider-Priestess | Removes Lolth deity reference |
| Drow Matron Mother → Umbrin Matron | |
| Mind Flayer → Voidmind | Fits Hush / void cosmology |
| Alhoon → Voidmind Archivist | Illithid-lich analogue |
| Beholder → Gaze Tyrant | Generic gaze-aberration |
| Death Tyrant → Gaze Tyrant Sovereign | |
| Gauth → Lesser Gaze Tyrant | |
| Beholder Zombie → Gaze Tyrant Husk | |
| Githyanki * → Astral Reaver * | Planar reaver line |
| Githzerai * → Astral Ascetic * | |
| Duergar * → Deep Dwarf * | |
| Kuo-toa * → Depth Toad * | |
| Yuan-ti * → Serpent-Blood * | |
| Svirfneblin → Cave Gnome | |
| Myconid * → Sporefolk * | |

Full map: `scripts/scrub_bestiary_ip.py` → `RENAME_MAP`.

---

## Sample renames

| Before | After |
|--------|-------|
| Drow Priestess of Lolth | Umbrin Spider-Priestess |
| Mind Flayer Arcanist | Voidmind Arcanist |
| Beholder (in lair) | Gaze Tyrant (in lair) |
| Githyanki Kith'rak | Astral Reaver War-Captain |
| Duergar Mind Master | Deep Dwarf Mind Master |
| Yuan-ti Anathema | Serpent-Blood Anathema |

---

## Verification

Post-scrub grep for `Lolth`, `Drow`, `Mind Flayer`, `Beholder`, `Githyanki`, `Duergar`, `Kuo-toa`, `Yuan-ti`, `Svirfneblin`, `Myconid`, `Alhoon`, `Underdark`, `Faerûn`, `Vecna`, `Tiamat` in:

- `src/bestiary_data_full.json` — **0 hits**
- `final_bestiary.xlsx` Monsters sheet — **0 hits**
- `src/components/MonstersLibrary.tsx` — no hardcoded monster names (loads JSON)

---

## Files touched

- `src/bestiary_data_full.json` — 54 `name` fields updated
- `final_bestiary.xlsx` — 230 cell replacements across sheets (Monsters, Drop Locations, Crafting Materials source lists, etc.)
- `scripts/scrub_bestiary_ip.py` — new idempotent scrub utility
- `docs/mechanics/BESTIARY_SCRUB_LOG.md` — this log
- `src/data/CONTINUITY_REPORT.md` — ASK OWNER #4 marked resolved
- `src/data/races.js`, `src/data/builder-races.js`, `src/data/racial-variants.json`, `src/data/feats.js`, `src/lib/character-storage.js` — player race aligned to Umbrin (VQ-14; 2026-07-29 PM lore pass)
- `src/bestiary_data_full.json` — 10 Umbral Elf* names → Umbrin* (2026-07-29 PM)
- `tools/ingest_canon_data.py` — builder template updated
