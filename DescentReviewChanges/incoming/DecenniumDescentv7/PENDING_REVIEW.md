# DecenniumDescentv7 — pending-review (playtest + Gameplay Loop Bible)

**Date staged:** 2026-08-05  
**Status:** `pending-review`  
**Do not** promote to ReviewBible or main without owner order.

## What this is

Owner-delivered **V7 Cursor Multi-Agent Playtest** packs plus **Gameplay Loop Bible v1** (`.docx`). These exercise balance / expedition / Haven / seasonal functions that authorship alone cannot finish. They are **not** an auto-cutover of live companion or published books.

## Staged layout

| Path | Role |
|------|------|
| `DD_V7_Cursor_Playtest_Master_Instructions.md` | Cross-pack orchestrator workflow |
| `Decennium_Descent_Gameplay_Loop_Bible_v1.docx` | Gameplay procedure bible (v1.0, Aug 2026) |
| `GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt` | UTF-8 text extract for agent review (staging aid) |
| `DD_V7_Cursor_0N_*.zip` | Original zip archives (retained) |
| `01_Combat_Class_Balance/` | Unzipped pack `01-combat-class-balance/` |
| `02_Expedition_Extraction/` | Unzipped pack `02-expedition-extraction/` |
| `03_Haven_Economy_Social/` | Unzipped pack `03-haven-economy-social/` |
| `04_Seasonal_Decennial/` | Unzipped pack `04-seasonal-decennial-persistence/` |

## Not delivered in this drop

- Pack **`05-readability-speed-onboarding`** is listed in Master Instructions recommended order but **no zip** was provided.

## Promotion blockers / prerequisites (do not invent)

Playtest READMEs assume a **“DecenniumDescent V7 Gameplay Complete”** tree with files that are **not yet on main** after V6 cutover, including:

- `docs/mechanics/GAMEPLAY_LOOP_CANON.md`
- `docs/mechanics/DESIGN_DOCTRINE.md`
- `data/public/Decennium_Descent_Gameplay_Loop_v1.json` / `src/data/gameplay-loop.json`

Until those are promoted from this bible (or a later V7 product pack) under owner approval, treat this folder as **incoming playtest kits + pending bible**, not live SoT.

## Playtest staging (2026-08-05)

Disposable run root (no main/ReviewBible promote):

- `playtest_workspace/` — synthetic V7 root with derived `GAMEPLAY_LOOP_CANON.md`, `DESIGN_DOCTRINE.md`, gameplay-loop JSON twins, hardlinks/junctions to existing companion sources.
- `PLAYTEST_RUN_ROOT.md` — cwd + path map for sibling pack agents.
- Remaining manifest gap: `src/components/ExpeditionTracker.tsx` (pack 02). Pack 05 still undelivered.

## Agent restrictions (from Master Instructions)

- Identify defects / propose patches; **do not rewrite canon during a test**.
- Distinguish illegal play, unclear rules, weak/dominant options, genuine imbalance.
- Player agents: only assigned-character information.
- Director agents: record rulings; do not silently treat rulings as written rules.
- Proposed changes need repeated scenario evidence or labeled hypothesis.
