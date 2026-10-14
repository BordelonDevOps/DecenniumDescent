# Cursor Multi-Agent Playtest Master Instructions

## Purpose

The gameplay loop is authored and implemented. These six packs test the functions that cannot be honestly finished through rules writing alone: numerical balance, repeated expedition outcomes, economic throughput, long-term Cycle behavior, and real-player usability.

## General workflow for every pack

1. Create a clean Git branch or disposable copy of Decennium Descent V7.2.
2. Extract one playtest ZIP into the repository root.
3. Open the repository root in Cursor, not only the extracted pack directory.
4. Open `README_FIRST.md` inside the extracted pack.
5. Give Cursor the complete contents of `CURSOR_ORCHESTRATOR_PROMPT.md` as the controlling prompt.
6. Allow Cursor to create the agents listed in `AGENT_ROSTER.md` and any dedicated player files under `agents/players/`.
7. Require each agent to use only the files listed in `SOURCE_MANIFEST.json`.
8. Run every scenario in `SCENARIO_MATRIX.csv` without silently changing canon or repairing rules during the test.
9. Store each agent result under `results/` in the format required by `RESULT_SCHEMA.json`.
10. Run `python compile_results.py` from the pack directory.
11. Return `COMPILED_REPORT.md` together with the raw `results/` directory for review in this ChatGPT Project.

## Agent restrictions

- Agents may identify defects and propose patches, but may not directly rewrite canon during a test.
- Agents must distinguish illegal play, unclear rules, weak options, dominant options, and genuine numerical imbalance.
- Player agents may use only information visible to their assigned character.
- Director agents must record rulings rather than quietly treating rulings as written rules.
- Every proposed change must cite repeated evidence from the scenarios or be labeled a hypothesis requiring another test.

## Recommended execution order

1. `06-dice-level-combat-validation`
2. `02-expedition-extraction`
3. `03-haven-economy-social`
4. `05-readability-speed-onboarding`
5. `04-seasonal-decennial-persistence`

Pack 01 remains useful for exploit discovery, but Pack 06 is the evidentiary combat test because it requires fixed builds, fixed fixtures, deterministic dice, and complete round logs.

Combat and expedition results should inform the economy and onboarding runs. Seasonal testing should occur last because it depends on stable short-term rules.

## Pack-specific deliverables

| Pack | Primary question | Required evidence |
|---|---|---|
| Combat and Class Balance | Are all seventeen classes tactically useful without action, control, summon, healing, or damage exploits? | Round logs, turn time, resources, damage, healing, prevention, control, objective contribution, rules lookups |
| Expedition and Extraction | Do Watches, Pressure, Supply, camps, cargo, casualties, and retreat create meaningful decisions? | Route logs, team activity, resource attrition, abandoned cargo, casualties, extraction outcomes |
| Haven Economy and Social | Does the Haven convert dungeon success into understandable economic and faction consequences? | Appraisals, claims, shares, prices, services, reputation changes, exploits, player choices |
| Seasonal and Decennial | Do Cycle Records preserve player consequence while replenishment creates a meaningfully new Opening? | Three-or-more-Cycle state comparison, persistence ledger, map and economy changes, legacy outcomes |
| Readability, Speed, and Onboarding | Can different player types learn and run the game at the intended speed? | Explanation time, turn time, lookups, misunderstandings, abandoned choices, confidence ratings |
| Dice-Level Combat Validation | Do observed dice-level outcomes support numerical changes? | Frozen build and fixture hashes, every die, full round state, written rulings, actual outcomes |

## Dedicated player files

The combat pack contains one dedicated player file for each of the seventeen classes. Every file includes an in-world background, expected player behavior, fight interpretation, decision protocol, class-specific tests, and required output.

The expedition pack contains twelve dedicated roster-player files matching the maximum Expedition size. These agents test whether each team and noncombat role remains relevant during travel, attrition, cargo management, retreat, and extraction.

## Return package

After each pack completes, return:

- `COMPILED_REPORT.md`
- the complete `results/` directory
- any proposed patch files kept separate from canon
- Cursor's agent execution log when available

Do not return only a prose summary. Raw results are needed to verify whether the compilation accurately represents the agents' findings.

## Evidence standard

Synthetic agent estimates may expose ambiguity and exploit surfaces but cannot prove numerical balance or human readability. Numerical changes require Pack 06 evidence; usability claims require Pack 05 with actual or closely observed readers.
