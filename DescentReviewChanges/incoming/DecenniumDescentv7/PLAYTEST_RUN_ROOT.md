# V7 Playtest Run Root

**Prepared:** 2026-08-05  
**Status:** Staging workspace for Cursor packs 01–04. **Not** promoted to ReviewBible or main.

## Run root (cwd for pack agents)

```
C:\Github\Descent assets\DecenniumDescent-main\DescentReviewChanges\incoming\DecenniumDescentv7\playtest_workspace
```

Treat this directory as the **“DecenniumDescent V7 Gameplay Complete”** root assumed by each pack’s `README_FIRST.md` and `SOURCE_MANIFEST.json`. All manifest paths are relative to this cwd.

Sibling agents: open Cursor / set working directory to **`playtest_workspace`**, not only the unzipped pack folder.

## Pack directories (do not move; run compile from pack dir)

| Pack | Path (under `DecenniumDescentv7/`) | Suggested results unzip target under run root |
|------|--------------------------------------|-----------------------------------------------|
| 01 Combat / Class Balance | `01_Combat_Class_Balance/01-combat-class-balance/` | `playtests/runs/combat/` |
| 02 Expedition / Extraction | `02_Expedition_Extraction/02-expedition-extraction/` | `playtests/runs/expedition/` |
| 03 Haven Economy / Social | `03_Haven_Economy_Social/03-haven-economy-social/` | `playtests/runs/haven/` |
| 04 Seasonal / Decennial | `04_Seasonal_Decennial/04-seasonal-decennial-persistence/` | `playtests/runs/seasonal/` |

Master instructions: `DD_V7_Cursor_Playtest_Master_Instructions.md` (parent of this file).  
Recommended order: 01 → 02 → 03 → (05 missing) → 04 last.

Pack zips may be copied or junctioned into `playtest_workspace/playtests/runs/<name>/` if desired; source packs above are authoritative.

## Canon produced for this run (new files in run root)

| Manifest / README path | Created at |
|------------------------|------------|
| `docs/mechanics/DESIGN_DOCTRINE.md` | `playtest_workspace/docs/mechanics/DESIGN_DOCTRINE.md` |
| `docs/mechanics/GAMEPLAY_LOOP_CANON.md` | `playtest_workspace/docs/mechanics/GAMEPLAY_LOOP_CANON.md` |
| `data/public/Decennium_Descent_Gameplay_Loop_v1.json` | same under run root |
| `src/data/gameplay-loop.json` | identical twin of the public JSON |
| `AGENTS.md` | playtest stub (restrictions + pointers) |

Source text: `GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt` (from `Decennium_Descent_Gameplay_Loop_Bible_v1.docx`). Regenerator: `playtest_workspace/_build_canon.py`.

## Linked from main / ReviewBible (not promoted copies of new canon)

Hardlinks or junctions into the run root for existing companion data:

- Class / feats / spells / bestiary / haven / dungeon / reputation / crafting / Core Systems v2
- Root + `docs/canon/CANON_MANIFEST.json` → main `docs/canon/CANON_MANIFEST.json`
- `docs/director-only/continuity/` → `DescentReviewChanges/ReviewBible/docs/director-only/continuity/`

## SOURCE_MANIFEST gaps still missing

| Path | Packs | Notes |
|------|-------|-------|
| `src/components/ExpeditionTracker.tsx` | **02** | Does not exist on main; no `ExpeditionTracker` in `src/components/`. Closest UI is `SessionTracker.tsx` (not linked; different contract). Pack 02 agents should note the gap and simulate from `GAMEPLAY_LOOP_CANON.md` + `gameplay-loop.json` + `dungeon-mechanics.json` / `haven.json` unless owner supplies the component. |
| Pack **05** `05-readability-speed-onboarding` | Master order | Zip not delivered in this drop. |

All other paths listed in packs 01–04 `SOURCE_MANIFEST.json` resolve under `playtest_workspace`.

## Pack 01 completion (2026-08-05)

- Ran end-to-end from pack dir (also mirrored pending-review Loop files onto main `docs/mechanics/` for SOURCE_MANIFEST).
- Outputs: `01_Combat_Class_Balance/01-combat-class-balance/COMPILED_REPORT.md`, `results/` (110 JSON), `proposed_patches/PACK01_PROPOSED_PATCHES.md`.
- **140 seeds / 10 scenarios.** Canon not rewritten.

## Agent restrictions (remind)

- Do **not** rewrite canon during the test; propose patches separately.
- Do **not** promote this workspace into ReviewBible or main.
- Use only files on that pack’s `SOURCE_MANIFEST.json` (plus the pack’s own agent/scenario files).
