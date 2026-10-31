# Compiled Cursor Multi-Agent Playtest Report

**Pack:** 04-seasonal-decennial-persistence  
**Date:** 2026-08-05  
**Campaigns:** 10× three-Cycle + 3× five-Cycle stress (seeds 301–351, 501–503)  
**Agent result files:** 104  
**Canon edits:** none  
**Pack 05:** skipped (zip not delivered)

## Executive findings
- Cycle Records preserved consequence (routes, districts, factions/debts, heirs, shocks) while replenishment restored chamber/map uncertainty.
- **Runaway wealth risk** OBSERVED on stress seed **501** (Haven boom wealthIndex 55→95 over five Openings) without solving the dungeon.
- Market glut seeds showed next-Cycle demand collapse then crafting pivot (wealth 50→42→47).
- Public vs Director boundary **PASS** (0 leaks): no Marquis / crystal path / Floor 97–100 / beyond-Sixth-Gate confirmation in public records.
- Source gaps: GAMEPLAY_LOOP_CANON.md / DESIGN_DOCTRINE.md / main docs/director-only/continuity/ missing — used bible extract §20 + ReviewBible continuity + MM CANON_BOUNDARY.
- Proposed patches (not applied): proposed_patches/PATCH_PROPOSALS.md
- Narrative template report: SEASONAL_REPORT.md · ledgers: campaign_ledgers/

---

# Seasonal and Decennial Report

## Cycle summaries
- Ran **10** three-Cycle campaigns and **3** five-Cycle stress campaigns across 6 scenarios.
- Seeds: 301, 302, 311, 312, 321, 322, 331, 341, 342, 351, 501, 502, 503.
- Each Opening produced a full Cycle Record (public) + optional directorSealed notes; then one Geography/Ecology/Economy/Politics/Resonance change cause-linked to that record; then ten-year advance.

## Persistence that mattered
- Secured route principles, faction standings/debts, Haven civic core, provenance, heirs/trainers, and political memory changed later Openings.
- Dynasty heirs gained soft legacy without automatic dungeon solve.
- Faction-war provenance liens and Haven damage repair bonds persisted across decades.

## Replenishment that restored uncertainty
- Chamber map fidelity fell across Cycles; unsecured spurs and resource nodes effectively reset.
- Market demand shifted after gluts; ordinary treasure nodes did not remain permanently stripped in a way that deleted play.
- Geography GEP changes invalidated at least some prior shortcuts even when trunks stayed Secured.

## Economic and political trajectories
- Haven boom wealth trajectories (incl. stress 501): [[55, 75, 87], [55, 75, 87], [55, 75, 87, 95, 95]].
- Market glut trajectories: [[50, 42, 47], [50, 42, 47]].
- Failed-depth seeds produced insurance panic and route abandonment without cosmology leak.
- Faction-war seeds kept district contest alive; damage seeds showed multi-Opening civic recovery.

## New-player accessibility
- Generally remained viable; boom late-Cycles risked sponsorship oligopoly (access <0.5) — patch proposal #6/#new-player charter slots.
- Post-disappearance cautionary mood improved Haven-focused entry for new companies.

## Canon-boundary findings
- Public records did not confirm Marquis truth, claimant succession, crystal path, Floor 97/100, or tiers beyond the failed Sixth Gate.
- Companion `dungeon-mechanics.json` still contains deep-tier draft victory text — flagged for separate scrub, not edited.
- Pack 05 onboarding zip missing — skipped per owner instruction.

## Recommended changes
- See `proposed_patches/PATCH_PROPOSALS.md` (not applied).

## Source gaps
- docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)
- docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)
- docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)


---

## Raw agent compilation
Result files: **104**

## Scenario: SEA-DYNASTY

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.79, 0.57, 0.34]
- securedPrincipleValue: [0.77, 0.76, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 341
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.79; principle=0.77; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.57; principle=0.76; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.34; principle=0.68; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.77, 0.76, 0.68]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.79, 0.57, 0.34]
- securedPrincipleValue: [0.77, 0.76, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 341
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.79; principle=0.77; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.57; principle=0.76; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.34; principle=0.68; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.79, 0.57, 0.34]
- securedPrincipleValue: [0.77, 0.76, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 341
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.79; principle=0.77; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.57; principle=0.76; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.34; principle=0.68; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.79, 0.57, 0.34]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.79, 0.57, 0.34]
- securedPrincipleValue: [0.77, 0.76, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 341
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.79; principle=0.77; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.57; principle=0.76; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.34; principle=0.68; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=6, retired=4, heirsReady=3.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
- Heir cohorts inherited outfitter liens and Routekeeper training; new Opening still required fresh Supply and route risk.
**Rules questions**
- Bible lists successors but not heir mechanical benefits — used soft reputation + trainer access only.
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.79, 0.57, 0.34]
- securedPrincipleValue: [0.77, 0.76, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 341
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.79; principle=0.77; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.57; principle=0.76; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.34; principle=0.68; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Iron Ledger Houses': 'strengthened'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.79, 0.57, 0.34]
- securedPrincipleValue: [0.77, 0.76, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 341
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.79; principle=0.77; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.57; principle=0.76; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.34; principle=0.68; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.79, 0.57, 0.34] (replenishment / geography shifts).
- Secured-route principle value: [0.77, 0.76, 0.68] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.79, 0.57, 0.34]
- securedPrincipleValue: [0.77, 0.76, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 341
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.79; principle=0.77; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.57; principle=0.76; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.34; principle=0.68; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [50, 55, 60].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.79, 0.57, 0.34]
- securedPrincipleValue: [0.77, 0.76, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 341
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.79; principle=0.77; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.57; principle=0.76; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.34; principle=0.68; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.55] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.84, 0.5, 0.26]
- securedPrincipleValue: [0.78, 0.65, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 342
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.84; principle=0.78; GEP={G:subsidence collapses a previously mapped...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.5; principle=0.65; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.78, 0.65, 0.62]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.84, 0.5, 0.26]
- securedPrincipleValue: [0.78, 0.65, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 342
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.84; principle=0.78; GEP={G:subsidence collapses a previously mapped...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.5; principle=0.65; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.84, 0.5, 0.26]
- securedPrincipleValue: [0.78, 0.65, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 342
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.84; principle=0.78; GEP={G:subsidence collapses a previously mapped...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.5; principle=0.65; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.84, 0.5, 0.26]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.84, 0.5, 0.26]
- securedPrincipleValue: [0.78, 0.65, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 342
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.84; principle=0.78; GEP={G:subsidence collapses a previously mapped...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.5; principle=0.65; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=6, retired=4, heirsReady=3.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
- Heir cohorts inherited outfitter liens and Routekeeper training; new Opening still required fresh Supply and route risk.
**Rules questions**
- Bible lists successors but not heir mechanical benefits — used soft reputation + trainer access only.
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.84, 0.5, 0.26]
- securedPrincipleValue: [0.78, 0.65, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 342
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.84; principle=0.78; GEP={G:subsidence collapses a previously mapped...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.5; principle=0.65; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Iron Ledger Houses': 'strengthened'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.84, 0.5, 0.26]
- securedPrincipleValue: [0.78, 0.65, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 342
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.84; principle=0.78; GEP={G:subsidence collapses a previously mapped...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.5; principle=0.65; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.84, 0.5, 0.26] (replenishment / geography shifts).
- Secured-route principle value: [0.78, 0.65, 0.62] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.84, 0.5, 0.26]
- securedPrincipleValue: [0.78, 0.65, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 342
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.84; principle=0.78; GEP={G:subsidence collapses a previously mapped...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.5; principle=0.65; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [50, 55, 60].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [50, 55, 60]
- mapChamberFidelity: [0.84, 0.5, 0.26]
- securedPrincipleValue: [0.78, 0.65, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 342
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.84; principle=0.78; GEP={G:subsidence collapses a previously mapped...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.5; principle=0.65; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.55] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [50, 55, 60, 65, 70]
- mapChamberFidelity: [0.83, 0.6, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.75, 0.7, 0.61, 0.59, 0.53]
- newPlayerAccess: [0.65, 0.65, 0.55, 0.55, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 503
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.83; principle=0.75; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.6; principle=0.7; GEP={G:subsidence collapses a previously mapped...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.25; principle=0.61; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=65; mapFidelity=0.1; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=70; mapFidelity=0.1; principle=0.53; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.75, 0.7, 0.61, 0.59, 0.53]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [50, 55, 60, 65, 70]
- mapChamberFidelity: [0.83, 0.6, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.75, 0.7, 0.61, 0.59, 0.53]
- newPlayerAccess: [0.65, 0.65, 0.55, 0.55, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 503
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.83; principle=0.75; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.6; principle=0.7; GEP={G:subsidence collapses a previously mapped...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.25; principle=0.61; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=65; mapFidelity=0.1; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=70; mapFidelity=0.1; principle=0.53; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [50, 55, 60, 65, 70]
- mapChamberFidelity: [0.83, 0.6, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.75, 0.7, 0.61, 0.59, 0.53]
- newPlayerAccess: [0.65, 0.65, 0.55, 0.55, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 503
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.83; principle=0.75; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.6; principle=0.7; GEP={G:subsidence collapses a previously mapped...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.25; principle=0.61; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=65; mapFidelity=0.1; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=70; mapFidelity=0.1; principle=0.53; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 5 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.83, 0.6, 0.25, 0.1, 0.1]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [50, 55, 60, 65, 70]
- mapChamberFidelity: [0.83, 0.6, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.75, 0.7, 0.61, 0.59, 0.53]
- newPlayerAccess: [0.65, 0.65, 0.55, 0.55, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 503
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.83; principle=0.75; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.6; principle=0.7; GEP={G:subsidence collapses a previously mapped...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.25; principle=0.61; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=65; mapFidelity=0.1; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=70; mapFidelity=0.1; principle=0.53; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=4, retired=6, heirsReady=5.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
- Heir cohorts inherited outfitter liens and Routekeeper training; new Opening still required fresh Supply and route risk.
**Rules questions**
- Bible lists successors but not heir mechanical benefits — used soft reputation + trainer access only.
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [50, 55, 60, 65, 70]
- mapChamberFidelity: [0.83, 0.6, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.75, 0.7, 0.61, 0.59, 0.53]
- newPlayerAccess: [0.65, 0.65, 0.55, 0.55, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 503
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.83; principle=0.75; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.6; principle=0.7; GEP={G:subsidence collapses a previously mapped...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.25; principle=0.61; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=65; mapFidelity=0.1; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=70; mapFidelity=0.1; principle=0.53; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Iron Ledger Houses': 'strengthened'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [50, 55, 60, 65, 70]
- mapChamberFidelity: [0.83, 0.6, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.75, 0.7, 0.61, 0.59, 0.53]
- newPlayerAccess: [0.65, 0.65, 0.55, 0.55, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 503
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.83; principle=0.75; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.6; principle=0.7; GEP={G:subsidence collapses a previously mapped...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.25; principle=0.61; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=65; mapFidelity=0.1; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=70; mapFidelity=0.1; principle=0.53; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.83, 0.6, 0.25, 0.1, 0.1] (replenishment / geography shifts).
- Secured-route principle value: [0.75, 0.7, 0.61, 0.59, 0.53] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [50, 55, 60, 65, 70]
- mapChamberFidelity: [0.83, 0.6, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.75, 0.7, 0.61, 0.59, 0.53]
- newPlayerAccess: [0.65, 0.65, 0.55, 0.55, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 503
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.83; principle=0.75; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.6; principle=0.7; GEP={G:subsidence collapses a previously mapped...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.25; principle=0.61; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=65; mapFidelity=0.1; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=70; mapFidelity=0.1; principle=0.53; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [50, 55, 60, 65, 70].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [50, 55, 60, 65, 70]
- mapChamberFidelity: [0.83, 0.6, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.75, 0.7, 0.61, 0.59, 0.53]
- newPlayerAccess: [0.65, 0.65, 0.55, 0.55, 0.55]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Iron Ledger Houses': 'strengthened'}
- finalDepthPublic: Haven
- seed: 503
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=50; mapFidelity=0.83; principle=0.75; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=55; mapFidelity=0.6; principle=0.7; GEP={G:subsidence collapses a previously mapped...}', 'Opening 3: depth=Haven; wealth=60; mapFidelity=0.25; principle=0.61; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=65; mapFidelity=0.1; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=70; mapFidelity=0.1; principle=0.53; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.55, 0.55, 0.55] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

## Scenario: SEA-FACTION-WAR

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [48, 48, 48]
- mapChamberFidelity: [0.77, 0.54, 0.31]
- securedPrincipleValue: [0.69, 0.72, 0.59]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 331
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.77; principle=0.69; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.54; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.31; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.69, 0.72, 0.59]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [48, 48, 48]
- mapChamberFidelity: [0.77, 0.54, 0.31]
- securedPrincipleValue: [0.69, 0.72, 0.59]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 331
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.77; principle=0.69; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.54; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.31; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [48, 48, 48]
- mapChamberFidelity: [0.77, 0.54, 0.31]
- securedPrincipleValue: [0.69, 0.72, 0.59]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 331
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.77; principle=0.69; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.54; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.31; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.77, 0.54, 0.31]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [48, 48, 48]
- mapChamberFidelity: [0.77, 0.54, 0.31]
- securedPrincipleValue: [0.69, 0.72, 0.59]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 331
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.77; principle=0.69; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.54; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.31; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=10, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [48, 48, 48]
- mapChamberFidelity: [0.77, 0.54, 0.31]
- securedPrincipleValue: [0.69, 0.72, 0.59]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 331
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.77; principle=0.69; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.54; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.31; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
- Sponsor contest kept Seal Exchange / Gateward contested across Cycles; institutions remembered liens.
**Exploits**
- If provenance liens never expire, faction war can lock auction liquidity for multiple Openings.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [48, 48, 48]
- mapChamberFidelity: [0.77, 0.54, 0.31]
- securedPrincipleValue: [0.69, 0.72, 0.59]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 331
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.77; principle=0.69; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.54; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.31; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.77, 0.54, 0.31] (replenishment / geography shifts).
- Secured-route principle value: [0.69, 0.72, 0.59] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [48, 48, 48]
- mapChamberFidelity: [0.77, 0.54, 0.31]
- securedPrincipleValue: [0.69, 0.72, 0.59]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 331
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.77; principle=0.69; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.54; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.31; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [48, 48, 48].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [48, 48, 48]
- mapChamberFidelity: [0.77, 0.54, 0.31]
- securedPrincipleValue: [0.69, 0.72, 0.59]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 331
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.77; principle=0.69; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.54; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.31; principle=0.59; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.65] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [48, 48, 48, 48, 48]
- mapChamberFidelity: [0.8, 0.55, 0.29, 0.1, 0.1]
- securedPrincipleValue: [0.67, 0.63, 0.63, 0.62, 0.45]
- newPlayerAccess: [0.65, 0.65, 0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 502
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.8; principle=0.67; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.55; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.29; principle=0.63; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.62; GEP={G:subsidence collapses a previously mapped...}', 'Opening 5: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.45; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.67, 0.63, 0.63, 0.62, 0.45]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [48, 48, 48, 48, 48]
- mapChamberFidelity: [0.8, 0.55, 0.29, 0.1, 0.1]
- securedPrincipleValue: [0.67, 0.63, 0.63, 0.62, 0.45]
- newPlayerAccess: [0.65, 0.65, 0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 502
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.8; principle=0.67; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.55; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.29; principle=0.63; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.62; GEP={G:subsidence collapses a previously mapped...}', 'Opening 5: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.45; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [48, 48, 48, 48, 48]
- mapChamberFidelity: [0.8, 0.55, 0.29, 0.1, 0.1]
- securedPrincipleValue: [0.67, 0.63, 0.63, 0.62, 0.45]
- newPlayerAccess: [0.65, 0.65, 0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 502
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.8; principle=0.67; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.55; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.29; principle=0.63; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.62; GEP={G:subsidence collapses a previously mapped...}', 'Opening 5: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.45; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 5 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.8, 0.55, 0.29, 0.1, 0.1]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [48, 48, 48, 48, 48]
- mapChamberFidelity: [0.8, 0.55, 0.29, 0.1, 0.1]
- securedPrincipleValue: [0.67, 0.63, 0.63, 0.62, 0.45]
- newPlayerAccess: [0.65, 0.65, 0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 502
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.8; principle=0.67; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.55; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.29; principle=0.63; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.62; GEP={G:subsidence collapses a previously mapped...}', 'Opening 5: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.45; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=10, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [48, 48, 48, 48, 48]
- mapChamberFidelity: [0.8, 0.55, 0.29, 0.1, 0.1]
- securedPrincipleValue: [0.67, 0.63, 0.63, 0.62, 0.45]
- newPlayerAccess: [0.65, 0.65, 0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 502
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.8; principle=0.67; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.55; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.29; principle=0.63; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.62; GEP={G:subsidence collapses a previously mapped...}', 'Opening 5: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.45; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
- Sponsor contest kept Seal Exchange / Gateward contested across Cycles; institutions remembered liens.
**Exploits**
- If provenance liens never expire, faction war can lock auction liquidity for multiple Openings.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [48, 48, 48, 48, 48]
- mapChamberFidelity: [0.8, 0.55, 0.29, 0.1, 0.1]
- securedPrincipleValue: [0.67, 0.63, 0.63, 0.62, 0.45]
- newPlayerAccess: [0.65, 0.65, 0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 502
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.8; principle=0.67; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.55; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.29; principle=0.63; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.62; GEP={G:subsidence collapses a previously mapped...}', 'Opening 5: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.45; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.8, 0.55, 0.29, 0.1, 0.1] (replenishment / geography shifts).
- Secured-route principle value: [0.67, 0.63, 0.63, 0.62, 0.45] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [48, 48, 48, 48, 48]
- mapChamberFidelity: [0.8, 0.55, 0.29, 0.1, 0.1]
- securedPrincipleValue: [0.67, 0.63, 0.63, 0.62, 0.45]
- newPlayerAccess: [0.65, 0.65, 0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 502
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.8; principle=0.67; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.55; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.29; principle=0.63; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.62; GEP={G:subsidence collapses a previously mapped...}', 'Opening 5: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.45; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [48, 48, 48, 48, 48].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [48, 48, 48, 48, 48]
- mapChamberFidelity: [0.8, 0.55, 0.29, 0.1, 0.1]
- securedPrincipleValue: [0.67, 0.63, 0.63, 0.62, 0.45]
- newPlayerAccess: [0.65, 0.65, 0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Seal Exchange': 'captured', 'Gateward Caravan Yards': 'contested'}
- finalDepthPublic: Haven
- seed: 502
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=48; mapFidelity=0.8; principle=0.67; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=48; mapFidelity=0.55; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=48; mapFidelity=0.29; principle=0.63; GEP={G:subsidence collapses a previously mapped...}', 'Opening 4: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.62; GEP={G:subsidence collapses a previously mapped...}', 'Opening 5: depth=Haven; wealth=48; mapFidelity=0.1; principle=0.45; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.65, 0.65, 0.65] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

## Scenario: SEA-FAILED-DEPTH

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.82, 0.52, 0.25]
- securedPrincipleValue: [0.32, 0.34, 0.32]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 321
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.82; principle=0.32; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.52; principle=0.34; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.25; principle=0.32; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.32, 0.34, 0.32]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.82, 0.52, 0.25]
- securedPrincipleValue: [0.32, 0.34, 0.32]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 321
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.82; principle=0.32; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.52; principle=0.34; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.25; principle=0.32; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
- Tier IV disappearance recorded as unverified public rumor/panic — not as cosmology reveal.
**Rules questions**
- dungeon-mechanics.json still lists Tier 7–10 gate bosses and Marquis victory text in companion data — playtest used public ceiling from CANON_BOUNDARY; companion scrub is a separate continuity task (not edited here).
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.82, 0.52, 0.25]
- securedPrincipleValue: [0.32, 0.34, 0.32]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 321
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.82; principle=0.32; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.52; principle=0.34; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.25; principle=0.32; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.82, 0.52, 0.25]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.82, 0.52, 0.25]
- securedPrincipleValue: [0.32, 0.34, 0.32]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 321
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.82; principle=0.32; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.52; principle=0.34; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.25; principle=0.32; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=9, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
- Opening 1 total loss produced rumor/debt persistence without living veterans; later Openings were non-dynastic replacements.
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.82, 0.52, 0.25]
- securedPrincipleValue: [0.32, 0.34, 0.32]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 321
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.82; principle=0.32; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.52; principle=0.34; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.25; principle=0.32; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.82, 0.52, 0.25]
- securedPrincipleValue: [0.32, 0.34, 0.32]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 321
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.82; principle=0.32; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.52; principle=0.34; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.25; principle=0.32; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.82, 0.52, 0.25] (replenishment / geography shifts).
- Secured-route principle value: [0.32, 0.34, 0.32] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.82, 0.52, 0.25]
- securedPrincipleValue: [0.32, 0.34, 0.32]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 321
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.82; principle=0.32; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.52; principle=0.34; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.25; principle=0.32; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [25, 25, 25].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.82, 0.52, 0.25]
- securedPrincipleValue: [0.32, 0.34, 0.32]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 321
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.82; principle=0.32; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.52; principle=0.34; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.25; principle=0.32; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.7, 0.7] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
- After famous disappearance, cautionary public ceiling actually improved new-company Haven focus (access rose).
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.76, 0.57, 0.26]
- securedPrincipleValue: [0.41, 0.32, 0.27]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 322
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.76; principle=0.41; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.57; principle=0.32; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.26; principle=0.27; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.41, 0.32, 0.27]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.76, 0.57, 0.26]
- securedPrincipleValue: [0.41, 0.32, 0.27]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 322
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.76; principle=0.41; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.57; principle=0.32; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.26; principle=0.27; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
- Tier IV disappearance recorded as unverified public rumor/panic — not as cosmology reveal.
**Rules questions**
- dungeon-mechanics.json still lists Tier 7–10 gate bosses and Marquis victory text in companion data — playtest used public ceiling from CANON_BOUNDARY; companion scrub is a separate continuity task (not edited here).
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.76, 0.57, 0.26]
- securedPrincipleValue: [0.41, 0.32, 0.27]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 322
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.76; principle=0.41; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.57; principle=0.32; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.26; principle=0.27; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.76, 0.57, 0.26]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.76, 0.57, 0.26]
- securedPrincipleValue: [0.41, 0.32, 0.27]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 322
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.76; principle=0.41; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.57; principle=0.32; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.26; principle=0.27; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=9, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
- Opening 1 total loss produced rumor/debt persistence without living veterans; later Openings were non-dynastic replacements.
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.76, 0.57, 0.26]
- securedPrincipleValue: [0.41, 0.32, 0.27]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 322
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.76; principle=0.41; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.57; principle=0.32; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.26; principle=0.27; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.76, 0.57, 0.26]
- securedPrincipleValue: [0.41, 0.32, 0.27]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 322
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.76; principle=0.41; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.57; principle=0.32; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.26; principle=0.27; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.76, 0.57, 0.26] (replenishment / geography shifts).
- Secured-route principle value: [0.41, 0.32, 0.27] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.76, 0.57, 0.26]
- securedPrincipleValue: [0.41, 0.32, 0.27]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 322
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.76; principle=0.41; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.57; principle=0.32; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.26; principle=0.27; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [25, 25, 25].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [25, 25, 25]
- mapChamberFidelity: [0.76, 0.57, 0.26]
- securedPrincipleValue: [0.41, 0.32, 0.27]
- newPlayerAccess: [0.65, 0.7, 0.7]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {}
- finalDepthPublic: Haven / Tier III (cautionary ceiling in public talk)
- seed: 322
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier IV (disappeared; no verified return); wealth=25; mapFidelity=0.76; principle=0.41; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.57; principle=0.32; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Haven / Tier III (cautionary ceiling in public talk); wealth=25; mapFidelity=0.26; principle=0.27; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.7, 0.7] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
- After famous disappearance, cautionary public ceiling actually improved new-company Haven focus (access rose).
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

## Scenario: SEA-HAVEN-BOOM

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.81, 0.5, 0.29]
- securedPrincipleValue: [0.75, 0.63, 0.66]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 301
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.81; principle=0.75; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.5; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.66; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.75, 0.63, 0.66]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.81, 0.5, 0.29]
- securedPrincipleValue: [0.75, 0.63, 0.66]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 301
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.81; principle=0.75; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.5; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.66; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.81, 0.5, 0.29]
- securedPrincipleValue: [0.75, 0.63, 0.66]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 301
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.81; principle=0.75; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.5; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.66; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.81, 0.5, 0.29]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.81, 0.5, 0.29]
- securedPrincipleValue: [0.75, 0.63, 0.66]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 301
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.81; principle=0.75; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.5; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.66; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=11, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.81, 0.5, 0.29]
- securedPrincipleValue: [0.75, 0.63, 0.66]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 301
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.81; principle=0.75; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.5; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.66; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.81, 0.5, 0.29]
- securedPrincipleValue: [0.75, 0.63, 0.66]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 301
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.81; principle=0.75; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.5; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.66; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.81, 0.5, 0.29] (replenishment / geography shifts).
- Secured-route principle value: [0.75, 0.63, 0.66] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.81, 0.5, 0.29]
- securedPrincipleValue: [0.75, 0.63, 0.66]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 301
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.81; principle=0.75; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.5; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.66; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [55, 75, 87].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.81, 0.5, 0.29]
- securedPrincipleValue: [0.75, 0.63, 0.66]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 301
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.81; principle=0.75; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.5; principle=0.63; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.66; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.45] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?
**Exploits**
- Late-Cycle institutionalized boom lowered new-player access below 0.5 — sponsorship oligopoly risk.
**Recommendations**
- Offer public charter slots / starter debts so new companies can enter boom Havens without dynasty capital.

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.75, 0.56, 0.29]
- securedPrincipleValue: [0.72, 0.67, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 302
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.75; principle=0.72; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.56; principle=0.67; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.72, 0.67, 0.62]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.75, 0.56, 0.29]
- securedPrincipleValue: [0.72, 0.67, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 302
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.75; principle=0.72; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.56; principle=0.67; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.75, 0.56, 0.29]
- securedPrincipleValue: [0.72, 0.67, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 302
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.75; principle=0.72; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.56; principle=0.67; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.75, 0.56, 0.29]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.75, 0.56, 0.29]
- securedPrincipleValue: [0.72, 0.67, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 302
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.75; principle=0.72; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.56; principle=0.67; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=11, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.75, 0.56, 0.29]
- securedPrincipleValue: [0.72, 0.67, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 302
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.75; principle=0.72; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.56; principle=0.67; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.75, 0.56, 0.29]
- securedPrincipleValue: [0.72, 0.67, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 302
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.75; principle=0.72; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.56; principle=0.67; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.75, 0.56, 0.29] (replenishment / geography shifts).
- Secured-route principle value: [0.72, 0.67, 0.62] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.75, 0.56, 0.29]
- securedPrincipleValue: [0.72, 0.67, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 302
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.75; principle=0.72; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.56; principle=0.67; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [55, 75, 87].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [55, 75, 87]
- mapChamberFidelity: [0.75, 0.56, 0.29]
- securedPrincipleValue: [0.72, 0.67, 0.62]
- newPlayerAccess: [0.65, 0.65, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 302
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.75; principle=0.72; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.56; principle=0.67; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.29; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.45] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?
**Exploits**
- Late-Cycle institutionalized boom lowered new-player access below 0.5 — sponsorship oligopoly risk.
**Recommendations**
- Offer public charter slots / starter debts so new companies can enter boom Havens without dynasty capital.

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [55, 75, 87, 95, 95]
- mapChamberFidelity: [0.79, 0.53, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.73, 0.65, 0.6, 0.55, 0.46]
- newPlayerAccess: [0.65, 0.65, 0.45, 0.45, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: True
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 501
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.79; principle=0.73; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.53; principle=0.65; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.25; principle=0.6; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 4: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.55; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.46; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.73, 0.65, 0.6, 0.55, 0.46]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [55, 75, 87, 95, 95]
- mapChamberFidelity: [0.79, 0.53, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.73, 0.65, 0.6, 0.55, 0.46]
- newPlayerAccess: [0.65, 0.65, 0.45, 0.45, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: True
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 501
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.79; principle=0.73; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.53; principle=0.65; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.25; principle=0.6; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 4: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.55; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.46; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [55, 75, 87, 95, 95]
- mapChamberFidelity: [0.79, 0.53, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.73, 0.65, 0.6, 0.55, 0.46]
- newPlayerAccess: [0.65, 0.65, 0.45, 0.45, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: True
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 501
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.79; principle=0.73; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.53; principle=0.65; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.25; principle=0.6; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 4: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.55; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.46; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 5 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.79, 0.53, 0.25, 0.1, 0.1]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
- OBSERVED RISK: multi-Cycle Haven boom pushed wealthIndex into runaway band while secured trunk still valued.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Exploits**
- Institutionalized Haven boom + retained trunk principles can stack into near-solved surface economy without solving the dungeon.
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [55, 75, 87, 95, 95]
- mapChamberFidelity: [0.79, 0.53, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.73, 0.65, 0.6, 0.55, 0.46]
- newPlayerAccess: [0.65, 0.65, 0.45, 0.45, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: True
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 501
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.79; principle=0.73; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.53; principle=0.65; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.25; principle=0.6; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 4: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.55; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.46; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=11, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [55, 75, 87, 95, 95]
- mapChamberFidelity: [0.79, 0.53, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.73, 0.65, 0.6, 0.55, 0.46]
- newPlayerAccess: [0.65, 0.65, 0.45, 0.45, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: True
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 501
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.79; principle=0.73; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.53; principle=0.65; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.25; principle=0.6; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 4: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.55; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.46; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [55, 75, 87, 95, 95]
- mapChamberFidelity: [0.79, 0.53, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.73, 0.65, 0.6, 0.55, 0.46]
- newPlayerAccess: [0.65, 0.65, 0.45, 0.45, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: True
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 501
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.79; principle=0.73; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.53; principle=0.65; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.25; principle=0.6; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 4: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.55; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.46; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.79, 0.53, 0.25, 0.1, 0.1] (replenishment / geography shifts).
- Secured-route principle value: [0.73, 0.65, 0.6, 0.55, 0.46] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [55, 75, 87, 95, 95]
- mapChamberFidelity: [0.79, 0.53, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.73, 0.65, 0.6, 0.55, 0.46]
- newPlayerAccess: [0.65, 0.65, 0.45, 0.45, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: True
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 501
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.79; principle=0.73; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.53; principle=0.65; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.25; principle=0.6; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 4: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.55; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.46; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [55, 75, 87, 95, 95].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Exploits**
- Repeated profitable Haven institutionalization without glut correction → runaway wealthIndex.
**Recommendations**
- Mandate at least one Economy GEP that counters any wealthIndex ≥80 boom unless a named disaster intervenes.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [55, 75, 87, 95, 95]
- mapChamberFidelity: [0.79, 0.53, 0.25, 0.1, 0.1]
- securedPrincipleValue: [0.73, 0.65, 0.6, 0.55, 0.46]
- newPlayerAccess: [0.65, 0.65, 0.45, 0.45, 0.45]
- anyExplorationTrivial: False
- runawayWealthRisk: True
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 5
- stress: True
- finalDistricts: {'Gateward Caravan Yards': 'strengthened', "Makers' Quarter": 'strengthened'}
- finalDepthPublic: Haven
- seed: 501
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=55; mapFidelity=0.79; principle=0.73; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Haven; wealth=75; mapFidelity=0.53; principle=0.65; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 3: depth=Haven; wealth=87; mapFidelity=0.25; principle=0.6; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 4: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.55; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 5: depth=Haven; wealth=95; mapFidelity=0.1; principle=0.46; GEP={G:rockfall seals an unsecured shortcut whi...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.45, 0.45, 0.45] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?
**Exploits**
- Late-Cycle institutionalized boom lowered new-player access below 0.5 — sponsorship oligopoly risk.
**Recommendations**
- Offer public charter slots / starter debts so new companies can enter boom Havens without dynasty capital.

## Scenario: SEA-HAVEN-DAMAGE

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [35, 45, 55]
- mapChamberFidelity: [0.76, 0.56, 0.26]
- securedPrincipleValue: [0.72, 0.65, 0.62]
- newPlayerAccess: [0.6, 0.6, 0.6]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Draughtworks': 'strengthened', 'Underways': 'strained'}
- finalDepthPublic: Haven
- seed: 351
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=35; mapFidelity=0.76; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=45; mapFidelity=0.56; principle=0.65; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=55; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.72, 0.65, 0.62]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [35, 45, 55]
- mapChamberFidelity: [0.76, 0.56, 0.26]
- securedPrincipleValue: [0.72, 0.65, 0.62]
- newPlayerAccess: [0.6, 0.6, 0.6]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Draughtworks': 'strengthened', 'Underways': 'strained'}
- finalDepthPublic: Haven
- seed: 351
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=35; mapFidelity=0.76; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=45; mapFidelity=0.56; principle=0.65; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=55; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [35, 45, 55]
- mapChamberFidelity: [0.76, 0.56, 0.26]
- securedPrincipleValue: [0.72, 0.65, 0.62]
- newPlayerAccess: [0.6, 0.6, 0.6]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Draughtworks': 'strengthened', 'Underways': 'strained'}
- finalDepthPublic: Haven
- seed: 351
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=35; mapFidelity=0.76; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=45; mapFidelity=0.56; principle=0.65; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=55; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.76, 0.56, 0.26]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [35, 45, 55]
- mapChamberFidelity: [0.76, 0.56, 0.26]
- securedPrincipleValue: [0.72, 0.65, 0.62]
- newPlayerAccess: [0.6, 0.6, 0.6]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Draughtworks': 'strengthened', 'Underways': 'strained'}
- finalDepthPublic: Haven
- seed: 351
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=35; mapFidelity=0.76; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=45; mapFidelity=0.56; principle=0.65; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=55; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=10, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [35, 45, 55]
- mapChamberFidelity: [0.76, 0.56, 0.26]
- securedPrincipleValue: [0.72, 0.65, 0.62]
- newPlayerAccess: [0.6, 0.6, 0.6]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Draughtworks': 'strengthened', 'Underways': 'strained'}
- finalDepthPublic: Haven
- seed: 351
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=35; mapFidelity=0.76; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=45; mapFidelity=0.56; principle=0.65; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=55; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Draughtworks': 'strengthened', 'Underways': 'strained'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
- Damaged district moved damaged→recovering→strengthened across three Openings; outbound capacity lagged wealth recovery.
**Rules questions**
- No numeric civic HP / repair-cost table in haven.json — recovery pace was a Director ruling.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [35, 45, 55]
- mapChamberFidelity: [0.76, 0.56, 0.26]
- securedPrincipleValue: [0.72, 0.65, 0.62]
- newPlayerAccess: [0.6, 0.6, 0.6]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Draughtworks': 'strengthened', 'Underways': 'strained'}
- finalDepthPublic: Haven
- seed: 351
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=35; mapFidelity=0.76; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=45; mapFidelity=0.56; principle=0.65; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=55; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.76, 0.56, 0.26] (replenishment / geography shifts).
- Secured-route principle value: [0.72, 0.65, 0.62] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [35, 45, 55]
- mapChamberFidelity: [0.76, 0.56, 0.26]
- securedPrincipleValue: [0.72, 0.65, 0.62]
- newPlayerAccess: [0.6, 0.6, 0.6]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Draughtworks': 'strengthened', 'Underways': 'strained'}
- finalDepthPublic: Haven
- seed: 351
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=35; mapFidelity=0.76; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=45; mapFidelity=0.56; principle=0.65; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=55; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [35, 45, 55].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [35, 45, 55]
- mapChamberFidelity: [0.76, 0.56, 0.26]
- securedPrincipleValue: [0.72, 0.65, 0.62]
- newPlayerAccess: [0.6, 0.6, 0.6]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Draughtworks': 'strengthened', 'Underways': 'strained'}
- finalDepthPublic: Haven
- seed: 351
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Haven; wealth=35; mapFidelity=0.76; principle=0.72; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 2: depth=Haven; wealth=45; mapFidelity=0.56; principle=0.65; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 3: depth=Haven; wealth=55; mapFidelity=0.26; principle=0.62; GEP={G:subsidence collapses a previously mapped...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.6, 0.6, 0.6] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

## Scenario: SEA-MARKET-GLUT

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.82, 0.56, 0.29]
- securedPrincipleValue: [0.66, 0.69, 0.63]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 311
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.82; principle=0.66; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.56; principle=0.69; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.29; principle=0.63; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.66, 0.69, 0.63]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.82, 0.56, 0.29]
- securedPrincipleValue: [0.66, 0.69, 0.63]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 311
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.82; principle=0.66; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.56; principle=0.69; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.29; principle=0.63; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.82, 0.56, 0.29]
- securedPrincipleValue: [0.66, 0.69, 0.63]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 311
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.82; principle=0.66; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.56; principle=0.69; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.29; principle=0.63; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.82, 0.56, 0.29]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.82, 0.56, 0.29]
- securedPrincipleValue: [0.66, 0.69, 0.63]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 311
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.82; principle=0.66; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.56; principle=0.69; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.29; principle=0.63; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=10, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.82, 0.56, 0.29]
- securedPrincipleValue: [0.66, 0.69, 0.63]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 311
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.82; principle=0.66; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.56; principle=0.69; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.29; principle=0.63; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.82, 0.56, 0.29]
- securedPrincipleValue: [0.66, 0.69, 0.63]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 311
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.82; principle=0.66; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.56; principle=0.69; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.29; principle=0.63; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.82, 0.56, 0.29] (replenishment / geography shifts).
- Secured-route principle value: [0.66, 0.69, 0.63] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.82, 0.56, 0.29]
- securedPrincipleValue: [0.66, 0.69, 0.63]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 311
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.82; principle=0.66; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.56; principle=0.69; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.29; principle=0.63; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [50, 42, 47].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
- Next-Cycle demand collapse after flood was the dominant ten-year effect; alternate harvest restored partial wealth.
**Rules questions**
- No explicit glut→price elasticity numbers in companion data — used qualitative shock tiers.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.82, 0.56, 0.29]
- securedPrincipleValue: [0.66, 0.69, 0.63]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 311
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.82; principle=0.66; GEP={G:rockfall seals an unsecured shortcut whi...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.56; principle=0.69; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.29; principle=0.63; GEP={G:earthshift reorients a Haven approach co...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.65] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

### Agent: campaign-chronicler

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.84, 0.51, 0.26]
- securedPrincipleValue: [0.7, 0.62, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 312
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.84; principle=0.7; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.51; principle=0.62; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.26; principle=0.68; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Every later GEP change cited an earlier shock, unresolved item, or route event from the prior Cycle Record.
- Persistence ledger: knowledge/provenance/civic core persisted; chambers replenished; secured principles decayed slowly ([0.7, 0.62, 0.68]).
- Cycle Record fields matched bible §20 checklist (routes, districts, artifacts, factions/debts, specialists/successors, unresolved, shocks, public depth).
- No orphaned Cycle-to-Cycle changes in this seed.
**Rules questions**
- How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
**Recommendations**
- Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.

### Agent: canon-boundary-auditor

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.84, 0.51, 0.26]
- securedPrincipleValue: [0.7, 0.62, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 312
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.84; principle=0.7; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.51; principle=0.62; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.26; principle=0.68; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Public Cycle Records used haven.json standing language (Haven, Tier III/IV, Sixth Gate failure ceiling) — no verified beyond-Gate-VI claims.
- Director sealed notes (if any) were stored separately from public records.
- No public confirmation of Marquis office, claimant succession, crystal path, Floor 97/100, or Silent Ones.
- Leak scan on public JSON: none.
- PASS: public vs Director boundary held for this seed.
**Recommendations**
- Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.

### Agent: cycle-director

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.84, 0.51, 0.26]
- securedPrincipleValue: [0.7, 0.62, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 312
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.84; principle=0.7; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.51; principle=0.62; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.26; principle=0.68; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Applied replenishment across 3 Openings with one G/E/E/P/R change each, each cause-linked to prior Cycle Record (bible §20).
- Creature/resource/unsecured-route replenishment restored chamber uncertainty (map fidelity [0.84, 0.51, 0.26]).
- Director-only notes kept out of public Cycle Record fields; public depth stayed at or below failed-Sixth-Gate knowledge ceiling.
- Horn/Opening timing assumed 2400h Opening / 1200h PoNR per dungeon-mechanics.json + locked baselines; ten-year advance between Openings.
**Rules questions**
- Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
**Recommendations**
- Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.

### Agent: expedition-dynasty

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.84, 0.51, 0.26]
- securedPrincipleValue: [0.7, 0.62, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 312
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.84; principle=0.7; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.51; principle=0.62; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.26; principle=0.68; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Survivors=10, retired=0, heirsReady=0.
- Legacy rewards expressed as trainers, charters, liens, and reputation — not automatic high-tier gear dominance.
- Ten-year advance aged veterans into retirement while heirs led subsequent Openings (dynasty seeds).
**Exploits**
- If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
**Recommendations**
- Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).

### Agent: haven-council

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.84, 0.51, 0.26]
- securedPrincipleValue: [0.7, 0.62, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 312
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.84; principle=0.7; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.51; principle=0.62; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.26; principle=0.68; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- District end-state: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}.
- Haven civic core assumed permanent unless destroyed (bible §20); damage scenarios recovered over 1–2 ten-year advances.
- Political memory (debts, decrees, contested provenance) persisted even when markets reset.
**Recommendations**
- Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.

### Agent: map-and-route-auditor

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.84, 0.51, 0.26]
- securedPrincipleValue: [0.7, 0.62, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 312
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.84; principle=0.7; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.51; principle=0.62; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.26; principle=0.68; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Chamber map fidelity by Opening: [0.84, 0.51, 0.26] (replenishment / geography shifts).
- Secured-route principle value: [0.7, 0.62, 0.68] (persists, not every chamber).
- Old maps helped trunk navigation but failed on replenished side chambers — exploration remained non-trivial when fidelity <0.5.
**Rules questions**
- Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
**Recommendations**
- On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.

### Agent: market-historian

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.84, 0.51, 0.26]
- securedPrincipleValue: [0.7, 0.62, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 312
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.84; principle=0.7; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.51; principle=0.62; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.26; principle=0.68; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- Wealth trajectory across Openings: [50, 42, 47].
- Market demand/scarcity replenishes per bible §20; glut seeds showed price crash then crafting pivot.
- Extracted provenance persisted; ordinary nodes replenished so boom material was not infinite each Opening.
- Next-Cycle demand collapse after flood was the dominant ten-year effect; alternate harvest restored partial wealth.
**Rules questions**
- No explicit glut→price elasticity numbers in companion data — used qualitative shock tiers.
**Recommendations**
- Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.

### Agent: new-player-company

**Metrics**
- wealthTrajectory: [50, 42, 47]
- mapChamberFidelity: [0.84, 0.51, 0.26]
- securedPrincipleValue: [0.7, 0.62, 0.68]
- newPlayerAccess: [0.65, 0.65, 0.65]
- anyExplorationTrivial: False
- runawayWealthRisk: False
- gepAlwaysCausedByPriorRecord: True
- publicCanonLeaks: []
- cyclesRun: 3
- stress: False
- finalDistricts: {'Seal Exchange': 'strengthened', "Makers' Quarter": 'strained'}
- finalDepthPublic: Tier III
- seed: 312
- sourceGaps: ['docs/mechanics/GAMEPLAY_LOOP_CANON.md (not on main; used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt §20 as pending-review stand-in)', 'docs/mechanics/DESIGN_DOCTRINE.md (not on main; doctrine text present in bible extract header)', 'docs/director-only/continuity/ (not on main tree; used ReviewBible/docs/director-only/continuity/ + MM CANON_BOUNDARY.md)']
- authorityNote: Gameplay Loop Bible v1 extract §20 + haven.json + dungeon-mechanics.json cycle; Director boundary from CANON_BOUNDARY / LEVEL_97 dual-layer. No silent canon edits.
- cycleLedger: ['Opening 1: depth=Tier III; wealth=50; mapFidelity=0.84; principle=0.7; GEP={G:flood opens a new lower gallery near a s...}', 'Opening 2: depth=Tier III; wealth=42; mapFidelity=0.51; principle=0.62; GEP={G:earthshift reorients a Haven approach co...}', 'Opening 3: depth=Tier III; wealth=47; mapFidelity=0.26; principle=0.68; GEP={G:flood opens a new lower gallery near a s...}']
- priorMattersWithoutTrivialExploration: True
**Observations**
- New-player access scores by Opening: [0.65, 0.65, 0.65] (1.0 = fully open field).
- Prior campaigns changed politics, prices, and rumors without granting unbeatable exclusive dungeon solves.
- Secured route principles helped veterans; replenished chambers kept first-time mapping relevant.
**Rules questions**
- Should Cycle Records expose competitor charters to new players, or only public decrees?

## Repeated rules questions

- (13) How should 'publicly accepted depth record' be phrased when a company disappears at Tier IV without verification?
- (13) Bible §20 requires GEP changes but does not specify magnitude tables — Director adjudication required each Cycle (recorded as ruling, not silent rule).
- (13) Bible says secured route principles persist but not every chamber — no Mapping-step reset procedure after ten years.
- (13) Should Cycle Records expose competitor charters to new players, or only public decrees?
- (3) Bible lists successors but not heir mechanical benefits — used soft reputation + trainer access only.
- (2) dungeon-mechanics.json still lists Tier 7–10 gate bosses and Marquis victory text in companion data — playtest used public ceiling from CANON_BOUNDARY; companion scrub is a separate continuity task (not edited here).
- (2) No explicit glut→price elasticity numbers in companion data — used qualitative shock tiers.
- (1) No numeric civic HP / repair-cost table in haven.json — recovery pace was a Director ruling.

## Repeated exploit findings

- (13) If heirs inherited secured trunk + full capital without Supply attrition, dynasty could skip early expedition tension (not observed under soft-legacy ruling).
- (3) Late-Cycle institutionalized boom lowered new-player access below 0.5 — sponsorship oligopoly risk.
- (2) If provenance liens never expire, faction war can lock auction liquidity for multiple Openings.
- (1) Institutionalized Haven boom + retained trunk principles can stack into near-solved surface economy without solving the dungeon.
- (1) Repeated profitable Haven institutionalization without glut correction → runaway wealthIndex.

## Repeated recommendations

- (13) Require chronicler sign-off that each GEP line references a Cycle Record bullet ID.
- (13) Keep Cycle Record template with explicit publicDepthRecord + directorSealedConsequence fields to prevent accidental merge.
- (13) Publish optional GEP magnitude bands (minor/standard/severe) tied to economicShocks severity without hard-coding lore.
- (13) Clarify heir package: titles/property/reputation yes; chamber maps and stocked nodes no (align §20 replenishment).
- (13) Add optional Haven district condition track (Intact / Strained / Damaged / Captured) for Cycle Records.
- (13) On Cycle advance: keep Secured tag on trunk; reset Mapping progress on unsecured spurs; apply one Geography change to at least one prior shortcut.
- (12) Keep glut/scarcity as required Economy GEP when economicShocks list a flood or panic.
- (3) Offer public charter slots / starter debts so new companies can enter boom Havens without dynasty capital.
- (1) Mandate at least one Economy GEP that counters any wealthIndex ≥80 boom unless a named disaster intervenes.


