# Decennium Descent V7.2 — AI Evidence Clarification Report

**Release line:** V7.2 AI Evidence Clarified  
**Date:** August 6, 2026

## Purpose

V7.2 converts high-confidence procedural findings from the V7.1 AI Lab into canonical, testable rules while refusing to treat AI narrative estimates as proof of numerical balance.

## What the V7.1 reports supported

The returned test archive contained completed material for Packs 05–18, but Packs 01–04 were absent. The strongest numerical proxy found that encounter labels did not preserve the same meaning across levels: a four-character Level 1 Standard cell reported a 41.9% success rate over 1,000 runs, while several Level 5–20 Standard cells reported 100% success. The same proxy reported global means of 92.4% for Standard, 74.2% for Hard, 23.5% for Severe, and 2.8% for Catastrophic encounters.

Those results establish a calibration problem in the provisional encounter chassis. They do not, by themselves, prove that a particular class, spell, feat, monster, or final budget must be changed. Several reports used proxy builds or model interpretation rather than frozen legal characters and complete roll logs.

## Canonical procedural corrections

V7.2 now defines:

- one explicit party-size multiplier table;
- objective, terrain, surprise, and hazard adjustments applied exactly once;
- a full unopposed enemy round as a two-step complication rather than ordinary surprise;
- Rest Debt as a two-Watch deadline with explicit interruption and stacking timing;
- one ordinary Escape source per retreat round, with a critical-success exception;
- Extraction Class modifiers from +0 through +6, Attention +1, and a combined cargo/handling cap of +7;
- player choice between the stated time/complication cost and identified low-priority cargo risk after an extraction failure;
- a costly Unknown-route Forced March that prevents progress-zero soft locks;
- a five-step Tier I Haven settlement path with escalation to the full procedure;
- counterfeit seizure and innocent-versus-knowing-holder consequences;
- explicit Haven tax, insurance, Heat, bribe, and reputation-access procedures;
- exactly one dungeon Opening per ten-year Cycle, while allowing many expeditions and campaign phases within that Opening;
- a machine-readable prestige registry snapshot containing all 18 paths;
- fail-closed application guards for roster size, Rest Debt, action limits, extraction modifiers, and Haven state.

## Publications and application changes

- Gameplay Loop JSON promoted to v1.2.
- Gameplay Loop Canon and worked examples updated.
- Gameplay Loop Bible rebuilt as v1.2.
- A one-page Quickstart Reference was added.
- Expedition Tracker now uses a two-Watch Rest Debt countdown and migrates legacy saves.
- New gameplay-state and prestige-snapshot validators were added.
- Public/Director information boundaries remain enforced.

## What remains provisional

The encounter Threat Point table and difficulty budgets remain a provisional chassis. No global class buff, class nerf, monster rebalance, or permanent budget change was promoted from the V7.1 proxies.

Numerical promotion requires:

1. frozen legal character builds;
2. frozen monster and scenario fixtures;
3. deterministic seeds and complete raw evidence;
4. separate training and holdout sets;
5. confidence intervals and practical-effect review;
6. regression testing of the complete expedition and Haven loop;
7. final validation by an experienced human GM and live players.

## V7.2 AI Calibration Lab

A single Cursor workspace accompanies this release. It contains 20 test packs, 68 dedicated class/persona files, deterministic mathematical tests, dice-level and agentic protocols, source hashing, raw-result contracts, and standard and high-volume presets.

The standard executable preset represents more than 400,000 test cases and state simulations before Cursor runs the persona packs. The high-volume preset represents more than 2.6 million executable cases and states before agentic play.

AI testing can stress arithmetic, rules interactions, exploits, and state transitions at scale. Human play remains required to assess live comprehension, table communication, dramatic pacing, emotional engagement, and experienced-GM preparation burden.
