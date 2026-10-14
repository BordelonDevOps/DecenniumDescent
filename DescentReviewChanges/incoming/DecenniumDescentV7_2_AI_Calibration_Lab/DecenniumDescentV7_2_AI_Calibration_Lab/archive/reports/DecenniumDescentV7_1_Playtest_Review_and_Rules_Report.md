# Decennium Descent V7.1 — Playtest Review and Rules Clarification Report

**Release line:** V7.1 Rules Clarified  
**Evidence reviewed:** `DD_V7_Playtest_Reports.zip`  
**Review date:** 2026-08-06  
**Governing design rule:** Decennium Descent should have 5e’s readability and speed, Pathfinder 2e’s tactical clarity and balance discipline, and its own expedition, extraction, Haven, and seasonal systems.

## Executive ruling

The returned Cursor reports were useful for identifying procedural ambiguity, exploit surfaces, conflicting terminology, and missing operational rules. They were not accepted as proof of final numerical balance because the combat reports used modeled or estimated outcomes rather than complete fixed-build, dice-by-dice transcripts, and the readability/speed pack was not returned.

V7.1 therefore promotes supported rules clarifications without applying a global HP, damage, encounter-budget, or economy rebalance.

## Evidence received

The archive contained compiled reports for:

1. Combat and class balance
2. Expedition and extraction
3. Haven economy and social systems
4. Seasonal and decennial persistence

The archive did not contain the Pack 05 readability and speed results.

## Canonical rules promoted in V7.1

### Action economy and independent actors

- All effects that grant a complete additional Action use one shared **Additional Action Slot**.
- A character cannot receive multiple complete extra Actions in the same turn merely by stacking class, spell, item, or ally effects.
- Summons, companions, autonomous deployables, reflections, drones, and independent undead use one shared independent-actor framework.
- Passive devices that do not take their own turns do not count toward the independent-actor limit.
- Creatures beyond the permitted independent-actor limit must be represented as a cohort, swarm, unit, or narrative support effect rather than separate full turns.
- **Dual Cast** is one Action that casts two eligible one-Action Tier 1–2 spells. Both RP costs are paid, and no more than one concentration effect may remain active.
- **Traumatic Casting** cannot refund, reset, protect, or retrigger itself.

### Expedition survival and extraction

- Every route now has a **Sustenance** rating from 0–4.
- Forage output is bounded by route Sustenance rather than producing unlimited Supply from repeated checks.
- Rest Debt must be resolved within the next two Watches or by the day boundary; otherwise Strain increases.
- Attention cargo creates Pressure when exposed or re-exposed, not automatically during every Watch.
- Extraction Test cadence is determined by Mapping quality and route length.
- Retreat normally produces one meaningful pursuit threat per pursuit round rather than an unrestricted enemy nova.

### Haven economy

- Expedition charters distinguish:
  - Gross recovered value
  - Net expedition proceeds
  - True profit after shares, taxes, wages, debt, replacement costs, and losses
- Haven taxes now have explicit rates by cargo class.
- Coin assay and reminting have defined costs and DCs.
- Public commodity medians and value ranges exist for documented Tiers I–V.
- The Underways uses a Heat track from 0–6.
- Labor status, wage baselines, debt-interest limits, and legal standing are explicit.
- No race receives a universal purchase price or inherent slave-market value.
- Trafficking investigations use an Evidence Clock.
- Haven districts provide structured downtime activities.

### Reputation and seasonal continuity

- Reputation uses a unified -5 to +5 scale.
- Cycle documentation is split into a public Cycle Record and a Director-Sealed Consequence Record.
- Cycle consequences are classified as Minor, Standard, or Severe.
- Haven districts track Intact, Strained, Damaged, Captured, or Recovering states.
- Maps can persist, degrade, or become unreliable after replenishment.
- Heirs and successor characters inherit only defined legacy benefits rather than complete predecessor progression.
- Milestone advancement is the default. Detailed XP remains an optional procedure.

### Public-canon protection

- Public validation now scans player-facing mechanics documentation in addition to runtime source and public data.
- The internal continuity document was moved to Director-only storage.
- The public advancement document was rewritten to avoid confirming unknown deep-tier geography or hidden endgame truths.

## Data and application changes

- Gameplay Loop canonical document advanced to version 1.1.
- Public and runtime Gameplay Loop JSON advanced to version 1.1.
- Expedition Tracker now records Sustenance, Rest Debt, Attention exposure, extraction-test timing, and gross/net/true-profit targets.
- Haven structured data now includes tax, assay, remint, commodities, Heat, labor, trafficking evidence, downtime, and district-condition procedures.
- Reputation UI and data now use the -5 to +5 scale.
- Class text was synchronized to the shared Additional Action Slot and independent-actor rules.
- Druid, Lich, Necromancer, Bard, Dragoon, Ranger, Mirrorsage, Tinker, and summon-related text was checked against the clarified timing model.

## Findings deliberately deferred

The following proposals were not promoted because the supplied evidence did not establish them:

- Increasing Standard encounter HP or damage by a fixed 15–25%.
- Raising Catastrophic or level-20 boss output globally.
- Changing every encounter budget from modeled win rates.
- Applying automatic wealth penalties at a specific counter-economy threshold.
- Treating simulated smuggling, trafficking, or market percentages as canonical economic rates.
- Claiming actual human onboarding time, lookup burden, or turn speed.

## Follow-up evidence packages

### Pack 05: Readability and Speed

This pack must be run with human readers or closely observed sessions. It measures explanation time, turn length, rules lookups, terminology failures, misunderstood decisions, and confidence after onboarding.

### Pack 06: Dice-Level Combat Validation

This new pack replaces modeled DPR with:

- Frozen legal character builds
- Fixed public monster stat blocks
- Visible deterministic random seeds
- Every attack roll, save, damage roll, heal, resource spend, condition, and reaction recorded
- Seventeen dedicated class-player files
- Director, Rules Judge, Dice Recorder, Build Auditor, Metrics Auditor, and Exploit Auditor agents
- Twelve fixed scenario families across level breakpoints

Numerical changes should be promoted only after repeated dice-level or human-table evidence supports them.

## Validation results

- Gameplay Loop validator: PASS
- Public canon validator: PASS
- Magic system validator: PASS — 848 spells, 936 placements, 17 classes
- Class ability validator: PASS — 17 classes, 335 feats, 10 oaths, 10 mysteries, 10 curses
- Updated Gameplay Loop Bible: rendered and visually reviewed across all 27 pages

## Release status

V7.1 is a rules-clarified release candidate. The written gameplay loop is complete and runnable. Remaining work is empirical:

1. Human readability and speed observation
2. Dice-by-dice combat calibration
3. Repeated extraction-profitability trials
4. Multi-Cycle campaign observation
5. Final numerical adjustment based on observed evidence
