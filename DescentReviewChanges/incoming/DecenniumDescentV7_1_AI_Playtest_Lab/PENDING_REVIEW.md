# DecenniumDescentV7_1_AI_Playtest_Lab — pending-review

**Date staged:** 2026-08-06  
**Status:** `pending-review`  
**Source zip:** `DecenniumDescentV7_1_AI_Playtest_Lab.zip` (~5.9 MB; 733 extracted files)  
**Do not** promote to ReviewBible or main without owner order.  
**Do not** auto-run the AI mega-suite from this drop alone (no “run immediately” instruction; owner drop = stage + summarize).

## What this is

Owner-delivered **V7.1 Rules Clarified** consolidated repository + integrated **AI Playtest Lab**. It is a full companion/rules tree (not kits-only), incorporating the V7 Gameplay Complete loop and post–packs-01–04 evidence review.

Per `RELEASE_CANDIDATE_STATUS.md` / review report: rules-complete RC; empirical playtesting still pending for numerical balance. Cursor sims from prior packs informed **procedural clarifications only** — not global HP/damage/economy rebalance.

## Staged layout

| Path | Role |
|------|------|
| `DecenniumDescentV7_1_AI_Playtest_Lab.zip` | Original delivery (retained) |
| `DecenniumDescentV7_1_AI_Playtest_Lab/` | Unzipped tree (via `tar`; Expand-Archive failed on long paths) |
| `START_HERE_CURSOR.md` | Lab entry: open folder, paste master orchestrator |
| `README.md` | V7.1 consolidated repo overview |
| `RELEASE_CANDIDATE_STATUS.md` | RC status; playtesting pending |
| `DecenniumDescentV7_1_Playtest_Review_and_Rules_Report.md` | Evidence ruling from packs 01–04 reports |
| `DecenniumDescentV7_Gameplay_Completion_Report.md` | Prior V7 Gameplay Complete summary |
| `docs/mechanics/GAMEPLAY_LOOP_CANON.md` + `DESIGN_DOCTRINE.md` | Loop SoT (v1.1 in this tree) |
| `data/public/Decennium_Descent_Gameplay_Loop_v1_1.json` | Structured loop v1.1 |
| `books/player/Decennium_Descent_Gameplay_Loop_Bible_v1_1.docx` | Gameplay Loop Bible v1.1 |
| `src/components/ExpeditionTracker.tsx` | EXPEDITION companion surface |
| `playtests/cursor-packs/` | Packs **01–06** (includes missing #05 + new #06 dice-level) |
| `playtests/ai-mega-suite/` | Integrated lab: packs **01–18**, schemas, tools, fixtures |
| `playtests/reports/DD_V7_Playtest_Reports.zip` | Prior Cursor report archive reviewed into V7.1 |

## Relation to prior incoming `DecenniumDescentv7`

| Prior (2026-08-05) | This lab (2026-08-06) |
|--------------------|------------------------|
| Kits + Gameplay Loop Bible **v1** only | Full V7.1 tree + Bible / JSON / canon **v1.1** |
| Packs 01–04 delivered; **05 missing** | Pack **05** present; pack **06** dice-level added |
| Synthetic `playtest_workspace/` on main staging | Self-contained repo intended as Cursor workspace root |
| Evidence not yet folded into rules | Review report promotes procedural clarifications from 01–04 |

Prior `DecenniumDescentv7/` remains historical staging for the first kit drop. This V7.1 lab is the candidate **rules-clarified + expanded test lab** package — still pending-review for ReviewBible/main.

## Recommended run order (from `START_HERE_CURSOR.md` — not executed)

1. Preflight + static validators  
2. Packs **07, 08, 16** (math / structural baselines)  
3. Pack **06** (dice-level tactical combat)  
4. Packs **09, 10, 15** (interaction / exploit)  
5. Packs **11, 12** (expedition / extraction)  
6. Pack **13** (Haven economy)  
7. Pack **14** (seasonal)  
8. Packs **05, 17** (usability / GM readiness)  
9. Pack **18** (regression gate)  
10. Compile all results → `AI_PLAYTEST_MASTER_REPORT.md` + `proposed-patches/` only  

## Agent restrictions (lab)

- Do not edit canon during tests; patches under `playtests/ai-mega-suite/proposed-patches/`  
- Public-player agents must not read Director-only files  
- Preserve source hashes; record RULES_HALT when written rules cannot resolve an action  
- AI narration ≠ numerical evidence
