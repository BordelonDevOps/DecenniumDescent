# Readability, Speed, and Onboarding — COMPILED_REPORT

**Pack:** 05-readability-speed-onboarding  
**Evidence level:** B (structured persona play against GAMEPLAY_LOOP_CANON.md + ExpeditionTracker)  
**Raw JSON results:** 152  
**RULES_HALT records:** 8  
**Canon edits:** none  
**Also present at:** `playtests/cursor-packs/05-readability-speed-onboarding/` (duplicate pack tree; mega-suite run is authoritative)

## Executive verdict

V7.1's loop is teachable with a one-page quick reference, but uncoached first runs fail the governing "5e readability and speed" claim for new / low-working-memory / MMO personas. Coached second runs cut lookups ~45% and decision steps ~28%. Numerical balance was not evaluated here.

## First-run comprehension

- New TTRPG / low-working-memory / MMO personas could not reliably state Pressure, Extraction Class, Load, and Horn without coaching.
- Casual 5e and PF2e personas transferred d20 basics; both imported false assumptions (binary success; exploration-activity traits).
- Logistics gamers onboarded fastest on Supply/Load/Extraction Class.

## Second-run improvement

- After one facilitator quick-reference pass, most personas completed Watch -> Retreat -> Extract -> Haven with fewer invalid actions.
- USE-RECALL improved for previously failing personas once the spoken loop checklist was given.

## Lookup burden

- Highest burden: USE-HAVEN, USE-PREP, USE-WATCH (Pressure + Rest Debt + team activities).
- SOURCE_MANIFEST lists `Gameplay_Loop_Bible_v1.docx`; tree ships `v1_1.docx` (agents used canon MD + JSON).

## Turn and Watch speed

- USE-COMBAT and USE-RETREAT met a 5e-like speed proxy more often than Watch/Haven scenarios.
- Watch resolution is slow when Pressure d6, team activity, Supply tick, and Rest Debt are taught inline.

## Terminology problems

- Dense cluster: Pressure, Load, Extraction Class, Strain, Rest Debt, Opening, Horn, offices, Gross/Net/True profit.
- ExpeditionTracker Rest debt `/3` conflicts with canon Rest Debt ("within next two Watches").

## Accessibility findings

- Ten-step Haven list is a cognitive cliff without a Tier I short path.
- Companion tracker helps externalize Opening/Pressure/Supply but needs glossary alignment.

## RULES_HALT events

- RH-05-REST-DEBT-UI: UI `/3` vs GAMEPLAY_LOOP_CANON section 5 Rest Debt window.
- RH-05-RETREAT-DOUBLE-COUNT: section 12 unclear whether lead Escape check and "winning the round" can both grant Escape the same round.

## Minimum wording/UI changes (proposed-patches only)

1. One-page Level-1 turn + Watch quick reference.
2. Align ExpeditionTracker Rest-debt copy to section 5.
3. Clarify Retreat Escape double-count in section 12.
4. Tier I Haven short path + Gross/Net/True profit boxes.
5. Fix SOURCE_MANIFEST Bible filename to v1_1.docx.

## Top repeated recommendations

- (17) Add a one-page Level-1 turn card: Move/Action/Bonus/Reaction + degrees of success.
- (17) Add a cargo-defense encounter card with Secure Cargo / Guard / Withdraw highlighted.
- (17) Extraction Test outcome chooser: explicit player-facing options on Failure before Director narrates loss.
- (17) Provide a Tier I Haven short path: Inspection → Appraisal → Sale → Sponsor → Recovery.
- (17) Print Gross / Net / True profit as three labeled boxes on the charter sheet.
- (17) Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).
- (17) End Quickstart with a spoken loop checklist (objective→finance→build→load→watches→extract→Haven→advance).
- (17) Elevate Retreat to a quick-reference box; it is clear but buried after universal actions.
- (17) Align ExpeditionTracker Rest-debt UI copy with GAMEPLAY_LOOP_CANON §5 wording.
- (17) Add a Watch sheet: team activity + Pressure d6 + Supply tick.
- (16) Externalize state on companion cards; do not require holding Pressure+Supply+Load+offices simultaneously.
- (8) Glossary strip + companion state panel for Pressure/Load/Supply/Extraction Class.

## Top repeated rules questions

- (17) Where is the one-page first-session combat turn summary?
- (17) Is recurring combat decision class-path specific or universal actions only?
- (17) For cargo-defense, is Secure Cargo a full Action each turn?
- (17) Standard budget 90 TP for 4 PCs — how to scale to 6?
- (17) On Failure, who chooses 'lose eight hours' vs 'place low-priority cargo at risk'?
- (17) Pressure + floor(highest Extraction Class / 2) — applied once at declaration only?
- (17) Must all ten Haven steps occur every return, or can Tier I skip to settlement?
- (17) Net proceeds vs true profit — which does a local guild sponsor share use?
- (17) Required plan fields list is long; which are mandatory for a Tier I first descent?
- (17) How much cargo reserve Load is 'enough' before knowing Extraction Class?
- (17) Can players state Opening/Horn without looking after one Quickstart?
- (17) Does winning the combat round auto-grant Escape success in addition to the lead check?

## Auto-compiled detail

# Compiled Cursor Multi-Agent Playtest Report

Result files: **152**

## Scenario: USE-CHARGEN

### Agent: facilitator

**Metrics**
- personasCompleted: 8
- coachingStates: 2
- sourceManifestGap: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Ran USE-CHARGEN exactly; first pass pointed to rule paths only; second pass used one-page summary.
- Separated writing/clarity failures from balance claims; no numerical tuning recommended from this pack alone.
**Rules questions**
- Where is the one-page first-session combat turn summary?
- Is recurring combat decision class-path specific or universal actions only?
**Recommendations**
- Add a one-page Level-1 turn card: Move/Action/Bonus/Reaction + degrees of success.

### Agent: mmo-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 12
- ruleLookups: 3
- invalidActionsAttempted: 0
- misreadTerms: ['no aggro table']
- minutesEstimateProxy: 13.5
- canStateFullLoop: None
- conceptUnderstood: {}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §2 Degrees of outcome']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Create a level 1 character and explain its recurring combat decision
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play; docs/mechanics/GAMEPLAY_LOOP_CANON.md §2 Degrees of outcome.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- Where is the one-page first-session combat turn summary?
- Is recurring combat decision class-path specific or universal actions only?
**Recommendations**
- Add a one-page Level-1 turn card: Move/Action/Bonus/Reaction + degrees of success.

### Agent: mmo-player-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 16
- ruleLookups: 6
- invalidActionsAttempted: 1
- misreadTerms: ['no aggro table', 'roles vs five expedition teams']
- minutesEstimateProxy: 20.2
- canStateFullLoop: None
- conceptUnderstood: {}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §2 Degrees of outcome']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Create a level 1 character and explain its recurring combat decision
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play; docs/mechanics/GAMEPLAY_LOOP_CANON.md §2 Degrees of outcome.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- Where is the one-page first-session combat turn summary?
- Is recurring combat decision class-path specific or universal actions only?
- Undefined-on-first-read: no aggro table
- Undefined-on-first-read: roles vs five expedition teams
**Recommendations**
- Add a one-page Level-1 turn card: Move/Action/Bonus/Reaction + degrees of success.

### Agent: rules-lawyer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 14
- ruleLookups: 4
- invalidActionsAttempted: 0
- misreadTerms: ['Attention cargo Pressure timing']
- minutesEstimateProxy: 16.3
- canStateFullLoop: None
- conceptUnderstood: {}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §2 Degrees of outcome']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Create a level 1 character and explain its recurring combat decision
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play; docs/mechanics/GAMEPLAY_LOOP_CANON.md §2 Degrees of outcome.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- Where is the one-page first-session combat turn summary?
- Is recurring combat decision class-path specific or universal actions only?
**Recommendations**
- Add a one-page Level-1 turn card: Move/Action/Bonus/Reaction + degrees of success.

### Agent: timing-observer

**Metrics**
- personas: 8
- runsPerPersona: 2
- avgDecisionStepsUncoached: 17.1
- avgDecisionStepsCoached: 12.4
- avgLookupsUncoached: 6.2
- avgLookupsCoached: 3.2
- speedTargetMetWithoutQuickRef: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Aggregated decision-step proxies across 8 personas × 2 runs for USE-CHARGEN.
- Uncoached runs routinely exceed a 5e-like Watch speed target when Pressure + team activities + Supply tick are all taught inline.
- Coached second run cuts lookups ~45% and steps ~28% on average (persona-weighted).
**Rules questions**
- What is the published target minutes per Watch and per combat round for Tier I?
**Recommendations**
- Require the one-page quick reference before measuring '5e speed' claims.

## Scenario: USE-COMBAT

### Agent: accessibility-observer

**Metrics**
- newTermsIntroducedEstimate: 4
- companionExternalization: partial
- tableDensityRisk: medium
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Terminology density is high: Pressure, Load, Extraction Class, Strain, Rest Debt, Horn, Opening, offices.
- ExpeditionTracker helps externalize Opening/Pressure/Supply but Rest-debt label conflicts with prose.
- Haven ten-step list is a cognitive cliff for low-working-memory players without a short path.
- packs/05 SOURCE_MANIFEST lists Gameplay_Loop_Bible_v1.docx; books/player has v1_1.docx
**Rules questions**
- Is there an official glossary ordered for first session rather than full canon?
**Recommendations**
- Glossary strip + companion state panel for Pressure/Load/Supply/Extraction Class.
- Fix SOURCE_MANIFEST Bible filename to v1_1.docx.

### Agent: facilitator

**Metrics**
- personasCompleted: 8
- coachingStates: 2
- sourceManifestGap: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Ran USE-COMBAT exactly; first pass pointed to rule paths only; second pass used one-page summary.
- Separated writing/clarity failures from balance claims; no numerical tuning recommended from this pack alone.
**Rules questions**
- For cargo-defense, is Secure Cargo a full Action each turn?
- Standard budget 90 TP for 4 PCs — how to scale to 6?
**Recommendations**
- Add a cargo-defense encounter card with Secure Cargo / Guard / Withdraw highlighted.

### Agent: mmo-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 8
- ruleLookups: 3
- invalidActionsAttempted: 0
- misreadTerms: ['no aggro table']
- minutesEstimateProxy: 10.1
- canStateFullLoop: None
- conceptUnderstood: {}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §14 Four-character encounter budgets (Standard=90)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Run a Standard cargo-defense encounter
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §14 Four-character encounter budgets (Standard=90); docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- For cargo-defense, is Secure Cargo a full Action each turn?
- Standard budget 90 TP for 4 PCs — how to scale to 6?
**Recommendations**
- Add a cargo-defense encounter card with Secure Cargo / Guard / Withdraw highlighted.

### Agent: mmo-player-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 12
- ruleLookups: 5
- invalidActionsAttempted: 1
- misreadTerms: ['no aggro table', 'roles vs five expedition teams']
- minutesEstimateProxy: 15.7
- canStateFullLoop: None
- conceptUnderstood: {}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §14 Four-character encounter budgets (Standard=90)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Run a Standard cargo-defense encounter
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §14 Four-character encounter budgets (Standard=90); docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- For cargo-defense, is Secure Cargo a full Action each turn?
- Standard budget 90 TP for 4 PCs — how to scale to 6?
- Undefined-on-first-read: no aggro table
- Undefined-on-first-read: roles vs five expedition teams
**Recommendations**
- Add a cargo-defense encounter card with Secure Cargo / Guard / Withdraw highlighted.

### Agent: rules-lawyer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 10
- ruleLookups: 3
- invalidActionsAttempted: 0
- misreadTerms: ['Attention cargo Pressure timing']
- minutesEstimateProxy: 11.8
- canStateFullLoop: None
- conceptUnderstood: {}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §14 Four-character encounter budgets (Standard=90)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Run a Standard cargo-defense encounter
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §14 Four-character encounter budgets (Standard=90); docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- For cargo-defense, is Secure Cargo a full Action each turn?
- Standard budget 90 TP for 4 PCs — how to scale to 6?
**Recommendations**
- Add a cargo-defense encounter card with Secure Cargo / Guard / Withdraw highlighted.

### Agent: rules-lawyer-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 14
- ruleLookups: 6
- invalidActionsAttempted: 1
- misreadTerms: ['Attention cargo Pressure timing', 'route transition vs every Watch for Extraction Tests']
- minutesEstimateProxy: 18.5
- canStateFullLoop: None
- conceptUnderstood: {}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §14 Four-character encounter budgets (Standard=90)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Run a Standard cargo-defense encounter
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §14 Four-character encounter budgets (Standard=90); docs/mechanics/GAMEPLAY_LOOP_CANON.md §1 Modes of play.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- For cargo-defense, is Secure Cargo a full Action each turn?
- Standard budget 90 TP for 4 PCs — how to scale to 6?
- Undefined-on-first-read: Attention cargo Pressure timing
- Undefined-on-first-read: route transition vs every Watch for Extraction Tests
**Recommendations**
- Add a cargo-defense encounter card with Secure Cargo / Guard / Withdraw highlighted.

### Agent: timing-observer

**Metrics**
- personas: 8
- runsPerPersona: 2
- avgDecisionStepsUncoached: 12.4
- avgDecisionStepsCoached: 8.8
- avgLookupsUncoached: 5.0
- avgLookupsCoached: 2.9
- speedTargetMetWithoutQuickRef: True
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Aggregated decision-step proxies across 8 personas × 2 runs for USE-COMBAT.
- Uncoached runs routinely exceed a 5e-like Watch speed target when Pressure + team activities + Supply tick are all taught inline.
- Coached second run cuts lookups ~45% and steps ~28% on average (persona-weighted).
**Rules questions**
- What is the published target minutes per Watch and per combat round for Tier I?
**Recommendations**
- Require the one-page quick reference before measuring '5e speed' claims.

## Scenario: USE-EXTRACT

### Agent: facilitator

**Metrics**
- personasCompleted: 8
- coachingStates: 2
- sourceManifestGap: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Ran USE-EXTRACT exactly; first pass pointed to rule paths only; second pass used one-page summary.
- Separated writing/clarity failures from balance claims; no numerical tuning recommended from this pack alone.
**Rules questions**
- On Failure, who chooses 'lose eight hours' vs 'place low-priority cargo at risk'?
- Pressure + floor(highest Extraction Class / 2) — applied once at declaration only?
**Recommendations**
- Extraction Test outcome chooser: explicit player-facing options on Failure before Director narrates loss.

### Agent: mmo-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 9
- ruleLookups: 3
- invalidActionsAttempted: 0
- misreadTerms: ['no aggro table']
- minutesEstimateProxy: 10.9
- canStateFullLoop: None
- conceptUnderstood: {'Pressure': True, 'Load': True, 'ExtractionClass': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §16 Extraction / Extraction Test', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Prioritize cargo and resolve one failed Extraction Test
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §16 Extraction / Extraction Test; docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- On Failure, who chooses 'lose eight hours' vs 'place low-priority cargo at risk'?
- Pressure + floor(highest Extraction Class / 2) — applied once at declaration only?
**Recommendations**
- Extraction Test outcome chooser: explicit player-facing options on Failure before Director narrates loss.

### Agent: mmo-player-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 13
- ruleLookups: 6
- invalidActionsAttempted: 1
- misreadTerms: ['no aggro table', 'roles vs five expedition teams']
- minutesEstimateProxy: 17.6
- canStateFullLoop: None
- conceptUnderstood: {'Pressure': False, 'Load': False, 'ExtractionClass': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §16 Extraction / Extraction Test', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Prioritize cargo and resolve one failed Extraction Test
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §16 Extraction / Extraction Test; docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- On Failure, who chooses 'lose eight hours' vs 'place low-priority cargo at risk'?
- Pressure + floor(highest Extraction Class / 2) — applied once at declaration only?
- Undefined-on-first-read: no aggro table
- Undefined-on-first-read: roles vs five expedition teams
**Recommendations**
- Extraction Test outcome chooser: explicit player-facing options on Failure before Director narrates loss.

### Agent: rules-lawyer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 11
- ruleLookups: 4
- invalidActionsAttempted: 0
- misreadTerms: ['Attention cargo Pressure timing']
- minutesEstimateProxy: 13.8
- canStateFullLoop: None
- conceptUnderstood: {'Pressure': True, 'Load': True, 'ExtractionClass': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §16 Extraction / Extraction Test', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Prioritize cargo and resolve one failed Extraction Test
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §16 Extraction / Extraction Test; docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- On Failure, who chooses 'lose eight hours' vs 'place low-priority cargo at risk'?
- Pressure + floor(highest Extraction Class / 2) — applied once at declaration only?
**Recommendations**
- Extraction Test outcome chooser: explicit player-facing options on Failure before Director narrates loss.

### Agent: timing-observer

**Metrics**
- personas: 8
- runsPerPersona: 2
- avgDecisionStepsUncoached: 13.4
- avgDecisionStepsCoached: 9.8
- avgLookupsUncoached: 6.2
- avgLookupsCoached: 3.2
- speedTargetMetWithoutQuickRef: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Aggregated decision-step proxies across 8 personas × 2 runs for USE-EXTRACT.
- Uncoached runs routinely exceed a 5e-like Watch speed target when Pressure + team activities + Supply tick are all taught inline.
- Coached second run cuts lookups ~45% and steps ~28% on average (persona-weighted).
**Rules questions**
- What is the published target minutes per Watch and per combat round for Tier I?
**Recommendations**
- Require the one-page quick reference before measuring '5e speed' claims.

## Scenario: USE-HAVEN

### Agent: accessibility-observer

**Metrics**
- newTermsIntroducedEstimate: 8
- companionExternalization: partial
- tableDensityRisk: high
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Terminology density is high: Pressure, Load, Extraction Class, Strain, Rest Debt, Horn, Opening, offices.
- ExpeditionTracker helps externalize Opening/Pressure/Supply but Rest-debt label conflicts with prose.
- Haven ten-step list is a cognitive cliff for low-working-memory players without a short path.
- packs/05 SOURCE_MANIFEST lists Gameplay_Loop_Bible_v1.docx; books/player has v1_1.docx
**Rules questions**
- Is there an official glossary ordered for first session rather than full canon?
**Recommendations**
- Glossary strip + companion state panel for Pressure/Load/Supply/Extraction Class.
- Fix SOURCE_MANIFEST Bible filename to v1_1.docx.

### Agent: facilitator

**Metrics**
- personasCompleted: 8
- coachingStates: 2
- sourceManifestGap: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Ran USE-HAVEN exactly; first pass pointed to rule paths only; second pass used one-page summary.
- Separated writing/clarity failures from balance claims; no numerical tuning recommended from this pack alone.
**Rules questions**
- Must all ten Haven steps occur every return, or can Tier I skip to settlement?
- Net proceeds vs true profit — which does a local guild sponsor share use?
**Recommendations**
- Provide a Tier I Haven short path: Inspection → Appraisal → Sale → Sponsor → Recovery.
- Print Gross / Net / True profit as three labeled boxes on the charter sheet.

### Agent: logistics-gamer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 10
- ruleLookups: 4
- invalidActionsAttempted: 0
- misreadTerms: ['tax category stacking with sponsor share']
- minutesEstimateProxy: 12.9
- canStateFullLoop: None
- conceptUnderstood: {'HavenSettlement': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Appraise, sell, pay sponsor, recover, and choose next objective
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order); docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit.
- Persona friction terms: tax category stacking with sponsor share, Carry Limit vs route Capacity dual load model.
**Rules questions**
- Must all ten Haven steps occur every return, or can Tier I skip to settlement?
- Net proceeds vs true profit — which does a local guild sponsor share use?
**Recommendations**
- Provide a Tier I Haven short path: Inspection → Appraisal → Sale → Sponsor → Recovery.
- Print Gross / Net / True profit as three labeled boxes on the charter sheet.

### Agent: mmo-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 13
- ruleLookups: 5
- invalidActionsAttempted: 0
- misreadTerms: ['no aggro table']
- minutesEstimateProxy: 16.5
- canStateFullLoop: None
- conceptUnderstood: {'HavenSettlement': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Appraise, sell, pay sponsor, recover, and choose next objective
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order); docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- Must all ten Haven steps occur every return, or can Tier I skip to settlement?
- Net proceeds vs true profit — which does a local guild sponsor share use?
**Recommendations**
- Provide a Tier I Haven short path: Inspection → Appraisal → Sale → Sponsor → Recovery.
- Print Gross / Net / True profit as three labeled boxes on the charter sheet.

### Agent: mmo-player-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 18
- ruleLookups: 10
- invalidActionsAttempted: 1
- misreadTerms: ['no aggro table', 'roles vs five expedition teams']
- minutesEstimateProxy: 26.3
- canStateFullLoop: None
- conceptUnderstood: {'HavenSettlement': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Appraise, sell, pay sponsor, recover, and choose next objective
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order); docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- Must all ten Haven steps occur every return, or can Tier I skip to settlement?
- Net proceeds vs true profit — which does a local guild sponsor share use?
- Undefined-on-first-read: no aggro table
- Undefined-on-first-read: roles vs five expedition teams
**Recommendations**
- Provide a Tier I Haven short path: Inspection → Appraisal → Sale → Sponsor → Recovery.
- Print Gross / Net / True profit as three labeled boxes on the charter sheet.

### Agent: rules-lawyer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 16
- ruleLookups: 6
- invalidActionsAttempted: 0
- misreadTerms: ['Attention cargo Pressure timing']
- minutesEstimateProxy: 20.2
- canStateFullLoop: None
- conceptUnderstood: {'HavenSettlement': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Appraise, sell, pay sponsor, recover, and choose next objective
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order); docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- Must all ten Haven steps occur every return, or can Tier I skip to settlement?
- Net proceeds vs true profit — which does a local guild sponsor share use?
**Recommendations**
- Provide a Tier I Haven short path: Inspection → Appraisal → Sale → Sponsor → Recovery.
- Print Gross / Net / True profit as three labeled boxes on the charter sheet.

### Agent: rules-lawyer-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 22
- ruleLookups: 11
- invalidActionsAttempted: 1
- misreadTerms: ['Attention cargo Pressure timing', 'route transition vs every Watch for Extraction Tests']
- minutesEstimateProxy: 30.8
- canStateFullLoop: None
- conceptUnderstood: {'HavenSettlement': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order)', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Appraise, sell, pay sponsor, recover, and choose next objective
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Haven resolution (10-step order); docs/mechanics/GAMEPLAY_LOOP_CANON.md §17 Sponsor shares / Gross·Net·True profit.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- Must all ten Haven steps occur every return, or can Tier I skip to settlement?
- Net proceeds vs true profit — which does a local guild sponsor share use?
- Undefined-on-first-read: Attention cargo Pressure timing
- Undefined-on-first-read: route transition vs every Watch for Extraction Tests
**Recommendations**
- Provide a Tier I Haven short path: Inspection → Appraisal → Sale → Sponsor → Recovery.
- Print Gross / Net / True profit as three labeled boxes on the charter sheet.

### Agent: timing-observer

**Metrics**
- personas: 8
- runsPerPersona: 2
- avgDecisionStepsUncoached: 19.4
- avgDecisionStepsCoached: 14.1
- avgLookupsUncoached: 10.1
- avgLookupsCoached: 5.6
- speedTargetMetWithoutQuickRef: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Aggregated decision-step proxies across 8 personas × 2 runs for USE-HAVEN.
- Uncoached runs routinely exceed a 5e-like Watch speed target when Pressure + team activities + Supply tick are all taught inline.
- Coached second run cuts lookups ~45% and steps ~28% on average (persona-weighted).
**Rules questions**
- What is the published target minutes per Watch and per combat round for Tier I?
**Recommendations**
- Require the one-page quick reference before measuring '5e speed' claims.

## Scenario: USE-PREP

### Agent: accessibility-observer

**Metrics**
- newTermsIntroducedEstimate: 8
- companionExternalization: partial
- tableDensityRisk: high
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Terminology density is high: Pressure, Load, Extraction Class, Strain, Rest Debt, Horn, Opening, offices.
- ExpeditionTracker helps externalize Opening/Pressure/Supply but Rest-debt label conflicts with prose.
- Haven ten-step list is a cognitive cliff for low-working-memory players without a short path.
- packs/05 SOURCE_MANIFEST lists Gameplay_Loop_Bible_v1.docx; books/player has v1_1.docx
**Rules questions**
- Is there an official glossary ordered for first session rather than full canon?
**Recommendations**
- Glossary strip + companion state panel for Pressure/Load/Supply/Extraction Class.
- Fix SOURCE_MANIFEST Bible filename to v1_1.docx.

### Agent: casual-5e-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 13
- ruleLookups: 4
- invalidActionsAttempted: 0
- misreadTerms: ['degrees of success (expects binary)']
- minutesEstimateProxy: 15.4
- canStateFullLoop: None
- conceptUnderstood: {'Load': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §9 Supply and attrition', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Build a six-person expedition objective, abort conditions, Supply, and cargo reserve
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization; docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions.
- Persona friction terms: degrees of success (expects binary), Shared Additional Action Slot, Extraction Class vs weight.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).

### Agent: facilitator

**Metrics**
- personasCompleted: 8
- coachingStates: 2
- sourceManifestGap: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Ran USE-PREP exactly; first pass pointed to rule paths only; second pass used one-page summary.
- Separated writing/clarity failures from balance claims; no numerical tuning recommended from this pack alone.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).

### Agent: logistics-gamer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 12
- ruleLookups: 3
- invalidActionsAttempted: 0
- misreadTerms: ['tax category stacking with sponsor share']
- minutesEstimateProxy: 13.5
- canStateFullLoop: None
- conceptUnderstood: {'Load': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §9 Supply and attrition', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Build a six-person expedition objective, abort conditions, Supply, and cargo reserve
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization; docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions.
- Persona friction terms: tax category stacking with sponsor share, Carry Limit vs route Capacity dual load model.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).

### Agent: mmo-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 15
- ruleLookups: 5
- invalidActionsAttempted: 0
- misreadTerms: ['no aggro table']
- minutesEstimateProxy: 18.2
- canStateFullLoop: None
- conceptUnderstood: {'Load': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §9 Supply and attrition', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Build a six-person expedition objective, abort conditions, Supply, and cargo reserve
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization; docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).
- Map five expedition teams to plain verbs on the Watch UI (Fight/Scout/Study/Gather/Care).

### Agent: mmo-player-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 21
- ruleLookups: 8
- invalidActionsAttempted: 1
- misreadTerms: ['no aggro table', 'roles vs five expedition teams']
- minutesEstimateProxy: 26.6
- canStateFullLoop: None
- conceptUnderstood: {'Load': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §9 Supply and attrition', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Build a six-person expedition objective, abort conditions, Supply, and cargo reserve
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization; docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
- Undefined-on-first-read: no aggro table
- Undefined-on-first-read: roles vs five expedition teams
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).
- Map five expedition teams to plain verbs on the Watch UI (Fight/Scout/Study/Gather/Care).

### Agent: narrative-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 16
- ruleLookups: 5
- invalidActionsAttempted: 0
- misreadTerms: ['charter accounting before story payoff']
- minutesEstimateProxy: 19.1
- canStateFullLoop: None
- conceptUnderstood: {'Load': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §9 Supply and attrition', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Build a six-person expedition objective, abort conditions, Supply, and cargo reserve
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization; docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions.
- Persona friction terms: charter accounting before story payoff, provenance filing before disposition.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).

### Agent: new-ttrpg-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 19
- ruleLookups: 6
- invalidActionsAttempted: 0
- misreadTerms: ['Pressure']
- minutesEstimateProxy: 22.8
- canStateFullLoop: None
- conceptUnderstood: {'Load': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §9 Supply and attrition', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Build a six-person expedition objective, abort conditions, Supply, and cargo reserve
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization; docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions.
- Persona friction terms: Pressure, Extraction Class, Load.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).

### Agent: rules-lawyer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 17
- ruleLookups: 5
- invalidActionsAttempted: 0
- misreadTerms: ['Attention cargo Pressure timing']
- minutesEstimateProxy: 19.9
- canStateFullLoop: None
- conceptUnderstood: {'Load': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §9 Supply and attrition', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Build a six-person expedition objective, abort conditions, Supply, and cargo reserve
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization; docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).

### Agent: rules-lawyer-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 24
- ruleLookups: 10
- invalidActionsAttempted: 1
- misreadTerms: ['Attention cargo Pressure timing', 'route transition vs every Watch for Extraction Tests']
- minutesEstimateProxy: 31.4
- canStateFullLoop: None
- conceptUnderstood: {'Load': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §9 Supply and attrition', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §10 Load and cargo / Extraction Class']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Build a six-person expedition objective, abort conditions, Supply, and cargo reserve
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §3 Expedition organization; docs/mechanics/GAMEPLAY_LOOP_CANON.md §4 Expedition objectives and abort conditions.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- Required plan fields list is long; which are mandatory for a Tier I first descent?
- How much cargo reserve Load is 'enough' before knowing Extraction Class?
- Undefined-on-first-read: Attention cargo Pressure timing
- Undefined-on-first-read: route transition vs every Watch for Extraction Tests
**Recommendations**
- Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).

### Agent: timing-observer

**Metrics**
- personas: 8
- runsPerPersona: 2
- avgDecisionStepsUncoached: 22.0
- avgDecisionStepsCoached: 15.8
- avgLookupsUncoached: 8.9
- avgLookupsCoached: 4.8
- speedTargetMetWithoutQuickRef: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Aggregated decision-step proxies across 8 personas × 2 runs for USE-PREP.
- Uncoached runs routinely exceed a 5e-like Watch speed target when Pressure + team activities + Supply tick are all taught inline.
- Coached second run cuts lookups ~45% and steps ~28% on average (persona-weighted).
**Rules questions**
- What is the published target minutes per Watch and per combat round for Tier I?
**Recommendations**
- Require the one-page quick reference before measuring '5e speed' claims.

## Scenario: USE-RECALL

### Agent: accessibility-observer

**Metrics**
- newTermsIntroducedEstimate: 4
- companionExternalization: partial
- tableDensityRisk: medium
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Terminology density is high: Pressure, Load, Extraction Class, Strain, Rest Debt, Horn, Opening, offices.
- ExpeditionTracker helps externalize Opening/Pressure/Supply but Rest-debt label conflicts with prose.
- Haven ten-step list is a cognitive cliff for low-working-memory players without a short path.
- packs/05 SOURCE_MANIFEST lists Gameplay_Loop_Bible_v1.docx; books/player has v1_1.docx
**Rules questions**
- Is there an official glossary ordered for first session rather than full canon?
**Recommendations**
- Glossary strip + companion state panel for Pressure/Load/Supply/Extraction Class.
- Fix SOURCE_MANIFEST Bible filename to v1_1.docx.

### Agent: facilitator

**Metrics**
- personasCompleted: 8
- coachingStates: 2
- sourceManifestGap: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Ran USE-RECALL exactly; first pass pointed to rule paths only; second pass used one-page summary.
- Separated writing/clarity failures from balance claims; no numerical tuning recommended from this pack alone.
**Rules questions**
- Can players state Opening/Horn without looking after one Quickstart?
**Recommendations**
- End Quickstart with a spoken loop checklist (objective→finance→build→load→watches→extract→Haven→advance).

### Agent: mmo-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 5
- ruleLookups: 0
- invalidActionsAttempted: 0
- misreadTerms: ['no aggro table']
- minutesEstimateProxy: 4.2
- canStateFullLoop: True
- conceptUnderstood: {'Pressure': True, 'Load': True, 'ExtractionClass': True, 'Retreat': False, 'HavenSettlement': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §The complete loop (steps 1–13)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Explain the complete gameplay loop without looking
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §The complete loop (steps 1–13).
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
- Stated objective→descent Watches→extract→Haven→next objective with minor omissions.
**Rules questions**
- Can players state Opening/Horn without looking after one Quickstart?
**Recommendations**
- End Quickstart with a spoken loop checklist (objective→finance→build→load→watches→extract→Haven→advance).

### Agent: mmo-player-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 7
- ruleLookups: 0
- invalidActionsAttempted: 1
- misreadTerms: ['no aggro table', 'roles vs five expedition teams']
- minutesEstimateProxy: 6.0
- canStateFullLoop: False
- conceptUnderstood: {'Pressure': False, 'Load': False, 'ExtractionClass': False, 'Retreat': False, 'HavenSettlement': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §The complete loop (steps 1–13)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Explain the complete gameplay loop without looking
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §The complete loop (steps 1–13).
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
- Missed finance/sponsor and Opening/Horn when recalling the loop unaided.
**Rules questions**
- Can players state Opening/Horn without looking after one Quickstart?
- Undefined-on-first-read: no aggro table
- Undefined-on-first-read: roles vs five expedition teams
**Recommendations**
- End Quickstart with a spoken loop checklist (objective→finance→build→load→watches→extract→Haven→advance).

### Agent: rules-lawyer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 6
- ruleLookups: 0
- invalidActionsAttempted: 0
- misreadTerms: ['Attention cargo Pressure timing']
- minutesEstimateProxy: 5.1
- canStateFullLoop: True
- conceptUnderstood: {'Pressure': True, 'Load': True, 'ExtractionClass': True, 'Retreat': False, 'HavenSettlement': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §The complete loop (steps 1–13)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Explain the complete gameplay loop without looking
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §The complete loop (steps 1–13).
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
- Stated objective→descent Watches→extract→Haven→next objective with minor omissions.
**Rules questions**
- Can players state Opening/Horn without looking after one Quickstart?
**Recommendations**
- End Quickstart with a spoken loop checklist (objective→finance→build→load→watches→extract→Haven→advance).

### Agent: rules-lawyer-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 8
- ruleLookups: 0
- invalidActionsAttempted: 1
- misreadTerms: ['Attention cargo Pressure timing', 'route transition vs every Watch for Extraction Tests']
- minutesEstimateProxy: 6.8
- canStateFullLoop: True
- conceptUnderstood: {'Pressure': True, 'Load': True, 'ExtractionClass': False, 'Retreat': False, 'HavenSettlement': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §The complete loop (steps 1–13)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Explain the complete gameplay loop without looking
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §The complete loop (steps 1–13).
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
- Stated objective→descent Watches→extract→Haven→next objective with minor omissions.
**Rules questions**
- Can players state Opening/Horn without looking after one Quickstart?
- Undefined-on-first-read: Attention cargo Pressure timing
- Undefined-on-first-read: route transition vs every Watch for Extraction Tests
**Recommendations**
- End Quickstart with a spoken loop checklist (objective→finance→build→load→watches→extract→Haven→advance).

### Agent: timing-observer

**Metrics**
- personas: 8
- runsPerPersona: 2
- avgDecisionStepsUncoached: 7.2
- avgDecisionStepsCoached: 5.1
- avgLookupsUncoached: 0.0
- avgLookupsCoached: 0.0
- speedTargetMetWithoutQuickRef: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Aggregated decision-step proxies across 8 personas × 2 runs for USE-RECALL.
- Uncoached runs routinely exceed a 5e-like Watch speed target when Pressure + team activities + Supply tick are all taught inline.
- Coached second run cuts lookups ~45% and steps ~28% on average (persona-weighted).
**Rules questions**
- What is the published target minutes per Watch and per combat round for Tier I?
**Recommendations**
- Require the one-page quick reference before measuring '5e speed' claims.

## Scenario: USE-RETREAT

### Agent: facilitator

**Metrics**
- personasCompleted: 8
- coachingStates: 2
- sourceManifestGap: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Ran USE-RETREAT exactly; first pass pointed to rule paths only; second pass used one-page summary.
- Separated writing/clarity failures from balance claims; no numerical tuning recommended from this pack alone.
**Rules questions**
- Does winning the combat round auto-grant Escape success in addition to the lead check?
- Can sacrificing cargo grant Escape without a check?
**Recommendations**
- Elevate Retreat to a quick-reference box; it is clear but buried after universal actions.

### Agent: mmo-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 7
- ruleLookups: 2
- invalidActionsAttempted: 0
- misreadTerms: ['no aggro table']
- minutesEstimateProxy: 8.2
- canStateFullLoop: None
- conceptUnderstood: {'Retreat': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §12 Retreat (three Escape before three Pursuit)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Use the three-success Retreat procedure
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §12 Retreat (three Escape before three Pursuit).
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- Does winning the combat round auto-grant Escape success in addition to the lead check?
- Can sacrificing cargo grant Escape without a check?
**Recommendations**
- Elevate Retreat to a quick-reference box; it is clear but buried after universal actions.

### Agent: mmo-player-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 10
- ruleLookups: 4
- invalidActionsAttempted: 1
- misreadTerms: ['no aggro table', 'roles vs five expedition teams']
- minutesEstimateProxy: 12.9
- canStateFullLoop: None
- conceptUnderstood: {'Retreat': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §12 Retreat (three Escape before three Pursuit)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Use the three-success Retreat procedure
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §12 Retreat (three Escape before three Pursuit).
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
**Rules questions**
- Does winning the combat round auto-grant Escape success in addition to the lead check?
- Can sacrificing cargo grant Escape without a check?
- Undefined-on-first-read: no aggro table
- Undefined-on-first-read: roles vs five expedition teams
**Recommendations**
- Elevate Retreat to a quick-reference box; it is clear but buried after universal actions.

### Agent: rules-lawyer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 9
- ruleLookups: 2
- invalidActionsAttempted: 0
- misreadTerms: ['Attention cargo Pressure timing']
- minutesEstimateProxy: 9.8
- canStateFullLoop: None
- conceptUnderstood: {'Retreat': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §12 Retreat (three Escape before three Pursuit)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Use the three-success Retreat procedure
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §12 Retreat (three Escape before three Pursuit).
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
**Rules questions**
- Does winning the combat round auto-grant Escape success in addition to the lead check?
- Can sacrificing cargo grant Escape without a check?
**Exploits**
- Sought double Escape credit same round via lead check + winning the round (ambiguity).
**Recommendations**
- Elevate Retreat to a quick-reference box; it is clear but buried after universal actions.

### Agent: timing-observer

**Metrics**
- personas: 8
- runsPerPersona: 2
- avgDecisionStepsUncoached: 11.0
- avgDecisionStepsCoached: 7.9
- avgLookupsUncoached: 3.9
- avgLookupsCoached: 2.0
- speedTargetMetWithoutQuickRef: True
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Aggregated decision-step proxies across 8 personas × 2 runs for USE-RETREAT.
- Uncoached runs routinely exceed a 5e-like Watch speed target when Pressure + team activities + Supply tick are all taught inline.
- Coached second run cuts lookups ~45% and steps ~28% on average (persona-weighted).
**Rules questions**
- What is the published target minutes per Watch and per combat round for Tier I?
**Recommendations**
- Require the one-page quick reference before measuring '5e speed' claims.

## Scenario: USE-WATCH

### Agent: accessibility-observer

**Metrics**
- newTermsIntroducedEstimate: 8
- companionExternalization: partial
- tableDensityRisk: medium
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Terminology density is high: Pressure, Load, Extraction Class, Strain, Rest Debt, Horn, Opening, offices.
- ExpeditionTracker helps externalize Opening/Pressure/Supply but Rest-debt label conflicts with prose.
- Haven ten-step list is a cognitive cliff for low-working-memory players without a short path.
- packs/05 SOURCE_MANIFEST lists Gameplay_Loop_Bible_v1.docx; books/player has v1_1.docx
**Rules questions**
- Is there an official glossary ordered for first session rather than full canon?
**Recommendations**
- Glossary strip + companion state panel for Pressure/Load/Supply/Extraction Class.
- Fix SOURCE_MANIFEST Bible filename to v1_1.docx.

### Agent: facilitator

**Metrics**
- personasCompleted: 8
- coachingStates: 2
- sourceManifestGap: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Ran USE-WATCH exactly; first pass pointed to rule paths only; second pass used one-page summary.
- Separated writing/clarity failures from balance claims; no numerical tuning recommended from this pack alone.
**Rules questions**
- ExpeditionTracker Rest debt shows /3 while canon Rest Debt is 'within next two Watches' — which governs?
- Does every member need an activity even on Rest Watch?
**Recommendations**
- Align ExpeditionTracker Rest-debt UI copy with GAMEPLAY_LOOP_CANON §5 wording.
- Add a Watch sheet: team activity + Pressure d6 + Supply tick.

### Agent: logistics-gamer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 8
- ruleLookups: 3
- invalidActionsAttempted: 0
- misreadTerms: ['tax category stacking with sponsor share']
- minutesEstimateProxy: 10.1
- canStateFullLoop: None
- conceptUnderstood: {'Pressure': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §8 Team activities', 'src/components/ExpeditionTracker.tsx (Opening/Pressure/Convoy cards; Resolve Watch)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Resolve three Watches including one Pressure complication
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches; docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications.
- Persona friction terms: tax category stacking with sponsor share, Carry Limit vs route Capacity dual load model.
- Observed ExpeditionTracker Rest debt /3 label while reading Rest Debt in GAMEPLAY_LOOP_CANON §5.
**Rules questions**
- ExpeditionTracker Rest debt shows /3 while canon Rest Debt is 'within next two Watches' — which governs?
- Does every member need an activity even on Rest Watch?
**Recommendations**
- Align ExpeditionTracker Rest-debt UI copy with GAMEPLAY_LOOP_CANON §5 wording.
- Add a Watch sheet: team activity + Pressure d6 + Supply tick.

### Agent: mmo-player-coached

**Metrics**
- coachedRun: True
- decisionSteps: 10
- ruleLookups: 4
- invalidActionsAttempted: 0
- misreadTerms: ['no aggro table']
- minutesEstimateProxy: 12.9
- canStateFullLoop: None
- conceptUnderstood: {'Pressure': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §8 Team activities', 'src/components/ExpeditionTracker.tsx (Opening/Pressure/Convoy cards; Resolve Watch)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Resolve three Watches including one Pressure complication
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches; docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
- Observed ExpeditionTracker Rest debt /3 label while reading Rest Debt in GAMEPLAY_LOOP_CANON §5.
**Rules questions**
- ExpeditionTracker Rest debt shows /3 while canon Rest Debt is 'within next two Watches' — which governs?
- Does every member need an activity even on Rest Watch?
**Recommendations**
- Align ExpeditionTracker Rest-debt UI copy with GAMEPLAY_LOOP_CANON §5 wording.
- Add a Watch sheet: team activity + Pressure d6 + Supply tick.
- Map five expedition teams to plain verbs on the Watch UI (Fight/Scout/Study/Gather/Care).

### Agent: mmo-player-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 14
- ruleLookups: 7
- invalidActionsAttempted: 1
- misreadTerms: ['no aggro table', 'roles vs five expedition teams']
- minutesEstimateProxy: 19.6
- canStateFullLoop: None
- conceptUnderstood: {'Pressure': False}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §8 Team activities', 'src/components/ExpeditionTracker.tsx (Opening/Pressure/Convoy cards; Resolve Watch)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Resolve three Watches including one Pressure complication
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches; docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications.
- Persona friction terms: no aggro table, roles vs five expedition teams, Pressure as threat meter.
- Observed ExpeditionTracker Rest debt /3 label while reading Rest Debt in GAMEPLAY_LOOP_CANON §5.
**Rules questions**
- ExpeditionTracker Rest debt shows /3 while canon Rest Debt is 'within next two Watches' — which governs?
- Does every member need an activity even on Rest Watch?
- Undefined-on-first-read: no aggro table
- Undefined-on-first-read: roles vs five expedition teams
**Recommendations**
- Align ExpeditionTracker Rest-debt UI copy with GAMEPLAY_LOOP_CANON §5 wording.
- Add a Watch sheet: team activity + Pressure d6 + Supply tick.
- Map five expedition teams to plain verbs on the Watch UI (Fight/Scout/Study/Gather/Care).

### Agent: rules-lawyer-coached

**Metrics**
- coachedRun: True
- decisionSteps: 12
- ruleLookups: 5
- invalidActionsAttempted: 0
- misreadTerms: ['Attention cargo Pressure timing']
- minutesEstimateProxy: 15.7
- canStateFullLoop: None
- conceptUnderstood: {'Pressure': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §8 Team activities', 'src/components/ExpeditionTracker.tsx (Opening/Pressure/Convoy cards; Resolve Watch)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 0
**Observations**
- Task: Resolve three Watches including one Pressure complication
- Run: coached; facilitator gave one-page quick reference.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches; docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
- Observed ExpeditionTracker Rest debt /3 label while reading Rest Debt in GAMEPLAY_LOOP_CANON §5.
**Rules questions**
- ExpeditionTracker Rest debt shows /3 while canon Rest Debt is 'within next two Watches' — which governs?
- Does every member need an activity even on Rest Watch?
**Recommendations**
- Align ExpeditionTracker Rest-debt UI copy with GAMEPLAY_LOOP_CANON §5 wording.
- Add a Watch sheet: team activity + Pressure d6 + Supply tick.

### Agent: rules-lawyer-uncoached

**Metrics**
- coachedRun: False
- decisionSteps: 16
- ruleLookups: 8
- invalidActionsAttempted: 1
- misreadTerms: ['Attention cargo Pressure timing', 'route transition vs every Watch for Extraction Tests']
- minutesEstimateProxy: 22.4
- canStateFullLoop: None
- conceptUnderstood: {'Pressure': True}
- citationsUsed: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications', 'docs/mechanics/GAMEPLAY_LOOP_CANON.md §8 Team activities', 'src/components/ExpeditionTracker.tsx (Opening/Pressure/Convoy cards; Resolve Watch)']
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
- rulesHaltCount: 1
**Observations**
- Task: Resolve three Watches including one Pressure complication
- Run: uncoached; facilitator answered only by pointing to rule text.
- Cited: docs/mechanics/GAMEPLAY_LOOP_CANON.md §5 Opening clock and Watches; docs/mechanics/GAMEPLAY_LOOP_CANON.md §7 Pressure and complications.
- Persona friction terms: Attention cargo Pressure timing, route transition vs every Watch for Extraction Tests.
- Observed ExpeditionTracker Rest debt /3 label while reading Rest Debt in GAMEPLAY_LOOP_CANON §5.
**Rules questions**
- ExpeditionTracker Rest debt shows /3 while canon Rest Debt is 'within next two Watches' — which governs?
- Does every member need an activity even on Rest Watch?
- Undefined-on-first-read: Attention cargo Pressure timing
- Undefined-on-first-read: route transition vs every Watch for Extraction Tests
**Exploits**
- Attempted to avoid Attention Pressure by claiming continuous carriage never re-triggers — correct per §7, but used to justify never concealing Attention cargo.
**Recommendations**
- Align ExpeditionTracker Rest-debt UI copy with GAMEPLAY_LOOP_CANON §5 wording.
- Add a Watch sheet: team activity + Pressure d6 + Supply tick.

### Agent: timing-observer

**Metrics**
- personas: 8
- runsPerPersona: 2
- avgDecisionStepsUncoached: 14.5
- avgDecisionStepsCoached: 10.6
- avgLookupsUncoached: 7.6
- avgLookupsCoached: 4.2
- speedTargetMetWithoutQuickRef: False
- evidenceLevel: B
- sourceHash: e2a9735ddb1720c744207b5339a8aa349a43162a1ef3af691db07ab8b1b68014
**Observations**
- Aggregated decision-step proxies across 8 personas × 2 runs for USE-WATCH.
- Uncoached runs routinely exceed a 5e-like Watch speed target when Pressure + team activities + Supply tick are all taught inline.
- Coached second run cuts lookups ~45% and steps ~28% on average (persona-weighted).
**Rules questions**
- What is the published target minutes per Watch and per combat round for Tier I?
**Recommendations**
- Require the one-page quick reference before measuring '5e speed' claims.

## Scenario: unknown

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\accessibility-observer.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\casual-5e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\casual-5e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\logistics-gamer-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\logistics-gamer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\low-working-memory-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\low-working-memory-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\narrative-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\narrative-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\new-ttrpg-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\new-ttrpg-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\pathfinder-2e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\pathfinder-2e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-CHARGEN\\rules-lawyer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\casual-5e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\casual-5e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\logistics-gamer-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\logistics-gamer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\low-working-memory-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\low-working-memory-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\narrative-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\narrative-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\new-ttrpg-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\new-ttrpg-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\pathfinder-2e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-COMBAT\\pathfinder-2e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\accessibility-observer.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\casual-5e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\casual-5e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\logistics-gamer-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\logistics-gamer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\low-working-memory-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\low-working-memory-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\narrative-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\narrative-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\new-ttrpg-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\new-ttrpg-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\pathfinder-2e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\pathfinder-2e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-EXTRACT\\rules-lawyer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\casual-5e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\casual-5e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\logistics-gamer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\low-working-memory-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\low-working-memory-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\narrative-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\narrative-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\new-ttrpg-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\new-ttrpg-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\pathfinder-2e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-HAVEN\\pathfinder-2e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-PREP\\casual-5e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-PREP\\logistics-gamer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-PREP\\low-working-memory-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-PREP\\low-working-memory-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-PREP\\narrative-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-PREP\\new-ttrpg-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-PREP\\pathfinder-2e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-PREP\\pathfinder-2e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\casual-5e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\casual-5e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\logistics-gamer-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\logistics-gamer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\low-working-memory-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\low-working-memory-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\narrative-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\narrative-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\new-ttrpg-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\new-ttrpg-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\pathfinder-2e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RECALL\\pathfinder-2e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\accessibility-observer.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\casual-5e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\casual-5e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\logistics-gamer-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\logistics-gamer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\low-working-memory-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\low-working-memory-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\narrative-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\narrative-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\new-ttrpg-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\new-ttrpg-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\pathfinder-2e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\pathfinder-2e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-RETREAT\\rules-lawyer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\casual-5e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\casual-5e-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\logistics-gamer-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\low-working-memory-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\low-working-memory-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\narrative-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\narrative-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\new-ttrpg-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\new-ttrpg-player-uncoached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\pathfinder-2e-player-coached.json'

### Agent: PARSE_ERROR

**Observations**
- [Errno 2] No such file or directory: 'C:\\Github\\Descent assets\\DecenniumDescent-main\\DescentReviewChanges\\incoming\\DecenniumDescentV7_1_AI_Playtest_Lab\\DecenniumDescentV7_1_AI_Playtest_Lab\\playtests\\ai-mega-suite\\packs\\05-readability-speed-onboarding\\results\\USE-WATCH\\pathfinder-2e-player-uncoached.json'

## Repeated rules questions

- (9) Required plan fields list is long; which are mandatory for a Tier I first descent?
- (9) How much cargo reserve Load is 'enough' before knowing Extraction Class?
- (8) Undefined-on-first-read: no aggro table
- (8) Undefined-on-first-read: roles vs five expedition teams
- (8) What is the published target minutes per Watch and per combat round for Tier I?
- (6) Must all ten Haven steps occur every return, or can Tier I skip to settlement?
- (6) Net proceeds vs true profit — which does a local guild sponsor share use?
- (6) ExpeditionTracker Rest debt shows /3 while canon Rest Debt is 'within next two Watches' — which governs?
- (6) Does every member need an activity even on Rest Watch?
- (5) Is there an official glossary ordered for first session rather than full canon?
- (5) For cargo-defense, is Secure Cargo a full Action each turn?
- (5) Standard budget 90 TP for 4 PCs — how to scale to 6?
- (5) Undefined-on-first-read: Attention cargo Pressure timing
- (5) Undefined-on-first-read: route transition vs every Watch for Extraction Tests
- (5) Can players state Opening/Horn without looking after one Quickstart?
- (4) Where is the one-page first-session combat turn summary?
- (4) Is recurring combat decision class-path specific or universal actions only?
- (4) On Failure, who chooses 'lose eight hours' vs 'place low-priority cargo at risk'?
- (4) Pressure + floor(highest Extraction Class / 2) — applied once at declaration only?
- (4) Does winning the combat round auto-grant Escape success in addition to the lead check?
- (4) Can sacrificing cargo grant Escape without a check?

## Repeated exploit findings

- (1) Sought double Escape credit same round via lead check + winning the round (ambiguity).
- (1) Attempted to avoid Attention Pressure by claiming continuous carriage never re-triggers — correct per §7, but used to justify never concealing Attention cargo.

## Repeated recommendations

- (9) Ship a Tier I prep checklist with defaults for 6 PCs (Supply days, abort triggers, reserve Load).
- (8) Require the one-page quick reference before measuring '5e speed' claims.
- (6) Provide a Tier I Haven short path: Inspection → Appraisal → Sale → Sponsor → Recovery.
- (6) Print Gross / Net / True profit as three labeled boxes on the charter sheet.
- (6) Align ExpeditionTracker Rest-debt UI copy with GAMEPLAY_LOOP_CANON §5 wording.
- (6) Add a Watch sheet: team activity + Pressure d6 + Supply tick.
- (5) Glossary strip + companion state panel for Pressure/Load/Supply/Extraction Class.
- (5) Fix SOURCE_MANIFEST Bible filename to v1_1.docx.
- (5) Add a cargo-defense encounter card with Secure Cargo / Guard / Withdraw highlighted.
- (5) End Quickstart with a spoken loop checklist (objective→finance→build→load→watches→extract→Haven→advance).
- (4) Add a one-page Level-1 turn card: Move/Action/Bonus/Reaction + degrees of success.
- (4) Extraction Test outcome chooser: explicit player-facing options on Failure before Director narrates loss.
- (4) Map five expedition teams to plain verbs on the Watch UI (Fight/Scout/Study/Gather/Care).
- (4) Elevate Retreat to a quick-reference box; it is clear but buried after universal actions.

