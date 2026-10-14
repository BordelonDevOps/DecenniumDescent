# Cursor Multi-Agent Playtest Programs

The core gameplay loop is written and implemented. These programs cover the functions that require repeated empirical play rather than additional rules writing.

| Pack | Function | Required output |
|---|---|---|
| `01-combat-class-balance` | Class, feat, spell, boss, control, summon, healing, and encounter-budget balance | `COMPILED_REPORT.md` plus raw JSON |
| `02-expedition-extraction` | Watches, team participation, Pressure, Supply, camps, cargo, casualties, and extraction | `COMPILED_REPORT.md` plus raw JSON |
| `03-haven-economy-social` | Appraisal, sponsors, banking, smuggling, labor, trafficking, pleasure houses, brewing, substances, and factions | `COMPILED_REPORT.md` plus raw JSON |
| `04-seasonal-decennial-persistence` | Cycle Records, ten-year persistence, replenishment, Haven change, and legacy | `COMPILED_REPORT.md` plus raw JSON |
| `05-readability-speed-onboarding` | First-session comprehension, lookup burden, turn speed, terminology, and accessibility | `COMPILED_REPORT.md` plus raw JSON |

The combat pack contains one dedicated player-agent file for each of the seventeen classes. The expedition pack contains twelve dedicated roster-player files matching the maximum Expedition structure.

Do not let playtest agents directly edit canon. Proposed changes must be separate patches supported by the compiled evidence.

- `06-dice-level-combat-validation`: fixed builds, fixed public monster records, deterministic dice, and complete round logs. This replaces model-estimated DPR as the evidentiary path for numerical combat changes.
