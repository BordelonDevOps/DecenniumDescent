# Feat, Spell, and Ability Interaction Scan — Compiled Report

Raw JSON results: 10
Unreadable skipped: 0

## Scenario coverage

- **DEAD-CHOICE:** 2 results; evidence C; outcome heuristic
- **MANDATORY-CHOICE:** 2 results; evidence C; outcome heuristic
- **PAIRWISE-TOP:** 2 results; evidence A; outcome reviewed
- **STATIC-ALL:** 2 results; evidence A; outcome scanned
- **TRIPLE-TARGETED:** 2 results; evidence A; outcome reviewed

## Rules halts

Total: 2
- {'code': 'RULES_HALT', 'detail': 'Cooldown resets cannot reset the same ability more than once per round — verify any reset+extra_action triple against GAMEPLAY_LOOP_CANON.'}
- {'code': 'RULES_HALT', 'detail': 'Cooldown resets cannot reset the same ability more than once per round — verify any reset+extra_action triple against GAMEPLAY_LOOP_CANON.'}

## Findings

Total: 24
- [?] deadChoices
- [?] mandatoryChoices
- [?] pairwiseReviewed
- [?] highRiskPairs
- [?] note
- [?] inventory
- [?] riskTagCounts
- [?] topRiskRecords
- [?] deadChoiceCandidates
- [?] mandatoryChoiceCandidates
- [?] topTriples
- [?] flaggedTriples
- [?] deadChoices
- [?] mandatoryChoices
- [?] pairwiseReviewed
- [?] highRiskPairs
- [?] note
- [?] inventory
- [?] riskTagCounts
- [?] topRiskRecords
- [?] deadChoiceCandidates
- [?] mandatoryChoiceCandidates
- [?] topTriples
- [?] flaggedTriples

## Wave summary

Static inventory: 335 feats, 848 spells parsed; 2000 pairwise + 500 triple scored.
Top risks: extra_action / actor / reset / unbounded / control stacking tags.
Level A static scan; agent confirmation still required for mandatory-choice claims.
