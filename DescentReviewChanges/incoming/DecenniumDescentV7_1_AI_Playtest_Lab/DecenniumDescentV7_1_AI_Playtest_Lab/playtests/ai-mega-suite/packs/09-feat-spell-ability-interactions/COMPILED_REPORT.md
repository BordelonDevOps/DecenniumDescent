# Feat, Spell, and Ability Interaction Scan — Compiled Report

Raw JSON results: 5 (STATIC-ALL, PAIRWISE-TOP, TRIPLE-TARGETED, DEAD-CHOICE, MANDATORY-CHOICE)
Unreadable results: 0
Evidence: Level A static/scoring + Level C heuristics for dead/mandatory labels
Canon edits: none

## Scenario coverage

- **STATIC-ALL:** 1 result; 335 feats + 848 spells + 85 path/core hooks = **1268** scored records
- **PAIRWISE-TOP:** 5000 pairs scored, **2000** kept for review; **100** high-risk (score ≥ 25)
- **TRIPLE-TARGETED:** **500** triples; **95** flagged (action-reset / actor+action / control-refresh)
- **DEAD-CHOICE:** heuristic Level C candidates
- **MANDATORY-CHOICE:** heuristic Level C candidates (extra_action ∧ reset tags)

## Key findings

1. Highest single-record risk tags cluster on **actor+reset** (Arcane Recall, Echo Spell) and **extra_action+control** (Haste).
2. Pairwise high-risk set is dominated by stacking **extra_action / reset / actor / control** tags across feat×spell and feat×feat pairs.
3. 95/500 targeted triples flagged potential **action-reset loops**, **actor+extra action**, or **control refresh** — must be checked against GAMEPLAY_LOOP_CANON (one AAS; reset once/round; actor cap 2).
4. RULES_HALT: cooldown resets cannot reset the same ability more than once per round — verify any reset+extra_action triple against canon text before tuning numbers.

## Rules halts

- Cooldown reset × extra action triples require human confirmation against shared AAS + once-per-round reset rules.

## Supported follow-ups (proposed-patches only)

- Explicit sheet reminder: Echo/Recall-style resets cannot refill AAS or retrigger the same Action grant in one round.
- Flag Haste-like effects for AAS interaction tests in Pack 15 (already stressed).

## Evidence limits

Dead/mandatory choice lists are Level C heuristics until agent personas confirm no rational use / forced take in play.
