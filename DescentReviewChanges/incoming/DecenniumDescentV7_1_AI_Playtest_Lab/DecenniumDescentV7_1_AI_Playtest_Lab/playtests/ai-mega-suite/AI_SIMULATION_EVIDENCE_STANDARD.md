# AI Simulation Evidence Standard

## Evidence levels

### Level A — executable evidence

Accepted for numerical tuning:

- deterministic seeded simulation;
- complete roll-by-roll transcript;
- frozen character and monster fixtures;
- source hashes;
- reproducible script output;
- sample size and confidence interval;
- no silent rulings.

### Level B — structured agent play

Accepted for rules and usability findings:

- dedicated player persona;
- visible-information restriction;
- complete turn or watch decisions;
- written rules citations;
- recorded RULES_HALT rulings;
- repeated patterns across scenarios.

Level B may justify wording, procedure, or interface changes. It does not by itself justify global damage, HP, DC, or encounter-budget changes.

### Level C — expert hypothesis

Useful for test generation only:

- theorycraft;
- expected DPR;
- narrative outcome estimate;
- one-agent opinion;
- unlogged or unseeded simulation.

Level C findings must be retested at Level A or B.

## Required reproducibility fields

Every result must include:

- test pack;
- scenario ID;
- run ID;
- seed;
- source-manifest hash;
- fixture hash;
- agent or script version;
- rules halts;
- assumptions;
- raw outcome;
- interpretation;
- evidence level.

## Bias controls

- Freeze builds before enemies are revealed.
- Rotate initiative and terrain.
- Use multiple party compositions.
- Use optimizer, cautious, novice, and narrative-risk personas.
- Separate public and Director knowledge.
- Never let the same agent act as player, Rules Judge, and metrics auditor.
- Report negative and null findings.
- Do not discard TPKs, trivial wins, or failed expeditions.
