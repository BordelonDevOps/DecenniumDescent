# Pack 06 Dice-Level Combat Report

Valid complete result files: 120
Invalid JSON files: 0

## Evidence completeness
- Frozen builds and hashes: `packs/06-dice-level-combat-validation/frozen_builds/` (MANIFEST.json + per-class L# sheets; hashed)
- Frozen fixtures and hashes: `packs/06-dice-level-combat-validation/fixtures/*.json`
- Seeds completed: **120 / 120** (12 scenarios × 10 seeds)
- Missing dice/round logs: **none** — every result includes per-die `roundLog` entries
- Script: `playtests/ai-mega-suite/tools/pack06_dice_combat.py` (Level A)
- Canon edits: **none**

## Observed results by scenario

## DICE-L1-STANDARD
- Seeds: 10
- Outcomes: {'victory': 0, 'retreat': 0, 'defeat': 10, 'timeout': 0}
- Median rounds: 4.0
- Logged rounds: 41
- Rules lookups: 60
- Illegal attempts: 0

## DICE-L3-CARGO
- Seeds: 10
- Outcomes: {'victory': 1, 'retreat': 0, 'defeat': 9, 'timeout': 0}
- Median rounds: 4.0
- Logged rounds: 46
- Rules lookups: 60
- Illegal attempts: 0

## DICE-L5-MOBILITY
- Seeds: 10
- Outcomes: {'victory': 10, 'retreat': 0, 'defeat': 0, 'timeout': 0}
- Median rounds: 2.0
- Logged rounds: 20
- Rules lookups: 60
- Illegal attempts: 0

## DICE-L5-ACTORS
- Seeds: 10
- Outcomes: {'victory': 0, 'retreat': 0, 'defeat': 9, 'timeout': 1}
- Median rounds: 7.0
- Logged rounds: 76
- Rules lookups: 70
- Illegal attempts: 0

## DICE-L10-BOSS
- Seeds: 10
- Outcomes: {'victory': 10, 'retreat': 0, 'defeat': 0, 'timeout': 0}
- Median rounds: 8.0
- Logged rounds: 82
- Rules lookups: 90
- Illegal attempts: 0

## DICE-L10-DARK
- Seeds: 10
- Outcomes: {'victory': 0, 'retreat': 0, 'defeat': 10, 'timeout': 0}
- Median rounds: 7.0
- Logged rounds: 73
- Rules lookups: 90
- Illegal attempts: 30 (Traumatic Casting retrigger / self-reset probes blocked)

## DICE-L10-RETREAT
- Seeds: 10
- Outcomes: {'victory': 0, 'retreat': 10, 'defeat': 0, 'timeout': 0}
- Median rounds: 3.0
- Logged rounds: 34
- Rules lookups: 90
- Illegal attempts: 0

## DICE-L15-CONTROL
- Seeds: 10
- Outcomes: {'victory': 0, 'retreat': 0, 'defeat': 10, 'timeout': 0}
- Median rounds: 7.0
- Logged rounds: 68
- Rules lookups: 90
- Illegal attempts: 12 (control-without-new-save probes blocked)

## DICE-L15-ATTRITION
- Seeds: 10
- Outcomes: {'victory': 10, 'retreat': 0, 'defeat': 0, 'timeout': 0}
- Median rounds: 14.0
- Logged rounds: 57
- Rules lookups: 70
- Illegal attempts: 0

## DICE-L20-CEILING-A
- Seeds: 10
- Outcomes: {'victory': 0, 'retreat': 0, 'defeat': 0, 'timeout': 10}
- Median rounds: 12.0
- Logged rounds: 120
- Rules lookups: 80
- Illegal attempts: 0

## DICE-L20-CEILING-B
- Seeds: 10
- Outcomes: {'victory': 10, 'retreat': 0, 'defeat': 0, 'timeout': 0}
- Median rounds: 9.0
- Logged rounds: 92
- Rules lookups: 80
- Illegal attempts: 0

## DICE-L20-CEILING-C
- Seeds: 10
- Outcomes: {'victory': 0, 'retreat': 0, 'defeat': 2, 'timeout': 8}
- Median rounds: 12.0
- Logged rounds: 120
- Rules lookups: 80
- Illegal attempts: 2

## Action-economy violations
- AAS restack probes on martials were blocked when the shared Additional Action Slot was already filled (logged under illegalAttempts on applicable seeds).
- No successful double-AAS resolution observed.

## Actor-cap violations
- Per-controller independent actor cap (2) enforced in DICE-L5-ACTORS / summoner paths.
- Party of four summoners each deploying 1 actor is legal per controller; fight still heavily favored enemies (Charnel Crawler + Fleshwright) — **0/10 victories**.

## Resource and concentration findings
- Traumatic Casting: first forced cast legal; retrigger/self-reset always illegal (30 blocked attempts across DICE-L10-DARK).
- Control parties: same-source full-turn lock without new save blocked (12 attempts).
- Boss Tenacity (Ashthirst @ L10): party still cleared all 10 seeds (median 8 rounds) — Tenacity converts first lock to Staggered rather than full skip.

## Encounter calibration observations
- **L1 Standard (Cave Bear + Crystal Shardling) = 0/10 wins.** Relative Threat vs L1 party is above Standard budget; treat as overtuned or require lower-CR swap for “Standard” L1.
- **L3 Hard cargo** = 1/10 objective holds — cargo pressure + CR2 pair is severe for L3.
- **L5 mobility objective** = 10/10 — objective completion too easy relative to Hard tag (anchor progress raced out by round 2).
- **L10 boss (Ashthirst)** = 10/10 for 6-PC Severe — workable climax pacing.
- **L10 dark casters vs Angry Grief-Bound** = 0/10 — Catastrophic/Severe caster ceiling fails under Traumatic trauma + boss multiattack.
- **L15 control vs Choralith + Grief-Bound** = 0/10 — control party lacks kill pressure once Tenacity burns.
- **L20 martial/tempo (Ceiling-B)** clears; **mixed (A)** times out; **control/actor (C)** mostly times out/defeats — ceiling balance is composition-sensitive.

## Rules lookups and ambiguity
- Written rulings in `rulings/*.md` and embedded in each result (`RJ-06-01` … `RJ-06-15`).
- Conservative attrition ruling: only limited resource refresh between the three L15 fights (no Long Rest).

## Supported changes (proposed only — see proposed-patches/)
1. Retune L1 Standard enemy pair or budget labeling (Level A evidence: 0/10).
2. Soften L3 Hard cargo seizure pressure or enemy CR for four L3 PCs (1/10).
3. Mobility/anchor objectives need clearer round budget or harder disable DC (10/10 too fast).
4. Revisit L10+ caster-only Severe/Catastrophic fixtures when Traumatic Casting self-tax stacks with boss multiattack.

## Unsupported hypotheses
- “Average DPR proves L20 balanced” — rejected; Ceiling-A/B/C diverge under identical dice protocol.
- Model-estimated win chances — not used.

## Evidence ruling

Only results with frozen build hashes, fixture hashes, individual dice, and complete round logs may support numerical changes. Missing evidence must be listed rather than estimated.
