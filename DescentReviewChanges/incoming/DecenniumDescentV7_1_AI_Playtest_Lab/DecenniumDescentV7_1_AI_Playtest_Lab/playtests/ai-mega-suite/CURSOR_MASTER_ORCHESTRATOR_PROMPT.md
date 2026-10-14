# Cursor Master Orchestrator Prompt

You are the lead test coordinator for Decennium Descent V7.1.

## Governing rule

Decennium Descent should have 5e’s readability and speed, Pathfinder 2e’s tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems.

## Workspace requirements

1. Read `AGENTS.md`, `CANON_MANIFEST.json`, `START_HERE_CURSOR.md`, and every file under `playtests/ai-mega-suite/`.
2. Run `python playtests/ai-mega-suite/tools/preflight.py`.
3. Do not edit canonical rule, data, or application files during testing.
4. Put generated fixtures under `playtests/ai-mega-suite/fixtures/generated/`.
5. Put raw results under `playtests/ai-mega-suite/results/<pack-id>/`.
6. Put suggested fixes under `playtests/ai-mega-suite/proposed-patches/`.
7. Record all unclear rules in `playtests/ai-mega-suite/results/rules-halts.csv`.
8. Preserve public/Director information boundaries.

## Evidence discipline

- Use executable simulations for arithmetic and probability claims.
- Use deterministic seeds.
- Freeze builds and fixtures before revealing scenario opposition.
- Record every die for Pack 06 and any targeted tactical reruns.
- Do not use average DPR as a substitute for dice-level combat evidence.
- Agentic simulations must use dedicated player files.
- A player agent may not read files unavailable to that character.
- A Rules Judge ruling applies to all seeds of the same scenario and must be logged.
- Do not silently correct a broken rule while testing it.

## Agent structure

Create separate agents for:

- Test Orchestrator
- Source and Build Auditor
- Rules Judge
- Statistical Auditor
- Exploit Auditor
- Public Canon Boundary Auditor
- Director Scenario Auditor
- Fixture Builder
- Result Integrity Auditor
- one agent for each assigned player file

The same agent may not be both a player and the Rules Judge or Statistical Auditor.

## Execution phases

### Phase 0 — source freeze

- Hash every authoritative source listed by the packs.
- Write `playtests/ai-mega-suite/source-hashes.json`.
- Create `playtests/ai-mega-suite/run-manifest.json`.
- Run all repository validators.

### Phase 1 — baseline simulations

Run:

```bash
python playtests/ai-mega-suite/tools/run_baseline_simulations.py
```

Review the output but do not tune rules yet.

### Phase 2 — mathematical calibration

Run Packs 07, 08, and 16.

### Phase 3 — full combat and interaction

Run Pack 06 first, then Packs 09, 10, and 15. Pack 01 may generate hypotheses but cannot override Pack 06 evidence.

### Phase 4 — complete gameplay loop

Run Packs 11, 12, and 13. Use complete expedition states from planning through Haven settlement.

### Phase 5 — long campaign and usability

Run Packs 14, 05, and 17.

### Phase 6 — regression

Run Pack 18 against the untouched V7.1 baseline. If proposed patches are later approved, rerun it against a patched branch and compare.

### Phase 7 — compilation

Run:

```bash
python playtests/ai-mega-suite/tools/compile_all_results.py
```

Then write `AI_PLAYTEST_MASTER_REPORT.md`.

## Master report structure

1. Executive findings
2. Evidence quality and test volume
3. Mathematical chassis
4. Action economy and actor limits
5. Class balance by level and persona
6. Feats, spells, paths, and exploit interactions
7. Encounter-budget calibration
8. Boss and control mechanics
9. Expedition survival and extraction
10. Cargo risk and profitability
11. Haven economy and faction systems
12. Seasonal and decennial persistence
13. Readability, speed, and GM preparation
14. Rules halts and contradictions
15. Confirmed defects
16. Suspected defects requiring human play
17. Proposed changes ranked by confidence
18. Human GM playtest agenda

## Prohibited behavior

- Do not declare the game balanced because agents completed scenarios.
- Do not discard outliers without explanation.
- Do not change canon during a run.
- Do not expose Director-only truths in public reports.
- Do not summarize away raw evidence.
- Do not claim human readability was proven by AI personas.
