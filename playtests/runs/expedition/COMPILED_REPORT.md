# Compiled Cursor Multi-Agent Playtest Report

**Pack:** `02-expedition-extraction` (V7 Cursor Pack 02 — Expedition / Extraction)  
**Iterations:** 65 seeded runs (10×5 scenarios + 15× EXP-HORN-RACE) → **90** agent JSON + 1 orchestrator summary  
**Canon:** No silent rewrites. Patches in `proposed_patches/PROPOSED_PATCHES.md`.  
**Sources:** `GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt` (+ playtest_workspace canon mirrors). SOURCE_MANIFEST gaps: `ExpeditionTracker.tsx` still missing; `GAMEPLAY_LOOP_CANON.md` / `gameplay-loop.json` exist under `playtest_workspace/` but not main.  
**Pack 01 assumption:** `01-combat-class-balance/results/` exists but **0** JSON — combat balance findings not incorporated; expedition checks used bible tier DC + roster lead mods only.

## Scenario outcomes

| Scenario | Haven% | Objective% | Sealed% | Avg elapsed | Peak P | Avg profit gp |
|---|---:|---:|---:|---:|---:|---:|
| EXP-T1-PROFIT | 100 | 0 | 0 | 68h | 2.0 | -383 |
| EXP-HAVEN-RUN | 100 | 0 | 0 | 147h | 5.7 | +343 |
| EXP-T3-LONG | 100 | 30 | 0 | 360h | 6.0 | -1223 |
| EXP-T4-DARK | 50 | 50 | 0 | 458h | 6.0 | -1224 |
| EXP-HORN-RACE | 40 | 40 | **60** | 108h | 6.0 | -216 |
| EXP-CASUALTY | 100 | 0 | 0 | 160h | 6.0 | -864 |

## Watch participation
All twelve roster agents received assignments every active Watch; Evening used the bible 3-worker / 9-rester camp pattern. Combat team size **3** is below optimal **4–6**, which collapses Escort capacity in EXP-CASUALTY when two Combat members start Downed.

## Pressure behavior
Mapped Tier I stayed mild (peak ~2). Haven-run / T3 / T4 / Horn / Casualty routinely hit Pressure 6 (Immediate crisis). Attention cargo + Load>Capacity + abort-continue are the dominant escalators. Attention **per-Watch stacking cadence is undefined** in bible §7 (see P2-02).

## Supply and rest curve
Per-Watch 1/3 daily Supply (worked example) is playable. Tier I Forage often erases Supply abort tension. Evening camp workers' Rest-debt timing vs §5 Strain needs clarification (P2-05).

## Cargo and casualty decisions
At-risk lots were stated before every extraction response. Priority-1 bulk salvage acts as a dump valve. EXP-CASUALTY: Capacity 55 vs Downed×2 (12 Load) + Living (6) forces Progress penalties; Extraction Failures threaten the only cargo lot (Living) despite priority 5 — Living preserved to Haven only when tests succeed; avg 6 Load abandoned.

## Profitability
"Profitable" / 8,000 gp targets fail often once **wages** (sim: 12×15 gp×days) and sponsor shares apply. Charter needs an explicit profit metric (P2-03). Gross Haven arrival ≠ profitable career outcome.

## Rules questions
Extraction Test spacing; Attention Pressure cadence; Rest-debt for camp workers; Rulebook periods vs Loop Watches; wages vs sponsor ordering; convoy vs route Capacity.

## Recommended changes
See `proposed_patches/PROPOSED_PATCHES.md` (P2-01…P2-07). Do not apply without owner order.

---

## Agent detail (compile_results.py)
Result files: **91**

## Scenario: EXP-CASUALTY

### Agent: 01-mara-vann

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 11.0
- avg_idle_watches: 4.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Escort': 110}
- team: Combat
- office: Expedition Leader
**Observations**
- Mara Venn (Combat/Expedition Leader): avg meaningful Watch marks 11.0, idle-ish rests 4.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Escort': 110}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
- With two Downed Combat members, Escort lead pressure shifts to remaining fighter + Support Transport.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 02-orrik-stonewake

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 4.8
- avg_idle_watches: 0.0
- avg_end_strain: 0.2
- downed_or_dead_pct: 100.0
- activity_counts: {}
- team: Combat
- office: Rear Guard
**Observations**
- Orrik Stonewake (Combat/Rear Guard): avg meaningful Watch marks 4.8, idle-ish rests 0.0, end Strain 0.2, downed/dead rate 100.0%.
- Top activities: {}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
- With two Downed Combat members, Escort lead pressure shifts to remaining fighter + Support Transport.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 03-taran-ashward

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 4.8
- avg_idle_watches: 0.0
- avg_end_strain: 0.2
- downed_or_dead_pct: 100.0
- activity_counts: {}
- team: Combat
- office: Escort Lead
**Observations**
- Taran Ashward (Combat/Escort Lead): avg meaningful Watch marks 4.8, idle-ish rests 0.0, end Strain 0.2, downed/dead rate 100.0%.
- Top activities: {}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
- With two Downed Combat members, Escort lead pressure shifts to remaining fighter + Support Transport.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 04-salira-dusk

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 20.6
- avg_idle_watches: 0.0
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Conceal Trail': 158}
- team: Reconnaissance
- office: Routekeeper
**Observations**
- Salira Dusk (Reconnaissance/Routekeeper): avg meaningful Watch marks 20.6, idle-ish rests 0.0, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 158}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 05-pell-quickstep

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 20.6
- avg_idle_watches: 0.0
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Conceal Trail': 158}
- team: Reconnaissance
- office: Scout
**Observations**
- Pell Quickstep (Reconnaissance/Scout): avg meaningful Watch marks 20.6, idle-ish rests 0.0, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 158}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 06-edrin-vale

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 11.0
- avg_idle_watches: 4.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 110}
- team: Research
- office: Claimant of Record
**Observations**
- Edrin Vale (Research/Claimant of Record): avg meaningful Watch marks 11.0, idle-ish rests 4.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Identify': 110}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 07-ysabel-threadseer

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 11.0
- avg_idle_watches: 4.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 110}
- team: Research
- office: Risk Analyst
**Observations**
- Ysabel Threadseer (Research/Risk Analyst): avg meaningful Watch marks 11.0, idle-ish rests 4.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Identify': 110}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 08-harka-reed

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 11.0
- avg_idle_watches: 4.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Preserve': 110}
- team: Resource
- office: Harvester
**Observations**
- Harka Reed (Resource/Harvester): avg meaningful Watch marks 11.0, idle-ish rests 4.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Preserve': 110}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: 09-zeetes

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 17.3
- avg_idle_watches: 0.0
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 110, 'Establish Camp': 15}
- team: Support
- office: Quartermaster
**Observations**
- Zeetes (Support/Quartermaster): avg meaningful Watch marks 17.3, idle-ish rests 0.0, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Transport': 110, 'Establish Camp': 15}.
- Extraction Tests centered on Quartermaster lead; failures forced visible cargo priority choices.
**Rules questions**
- Is vehicle/tool proficiency intended to replace Survival for Extraction Tests when no vehicle is present?
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 10-durn-stonevow

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 12.5
- avg_idle_watches: 4.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 110, 'Establish Camp': 15}
- team: Support
- office: Surgeon
**Observations**
- Durn Stonevow (Support/Surgeon): avg meaningful Watch marks 12.5, idle-ish rests 4.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Transport': 110, 'Establish Camp': 15}.
- Treat Watches competed with Transport during casualty extraction — real office conflict.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 11-ilse-harrow

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 12.5
- avg_idle_watches: 4.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 110, 'Establish Camp': 15}
- team: Support
- office: Transport Chief
**Observations**
- Ilse Harrow (Support/Transport Chief): avg meaningful Watch marks 12.5, idle-ish rests 4.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Transport': 110, 'Establish Camp': 15}.
- Capacity-constrained Load made Transport assignment meaningful every extract Watch.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 12-toma-glass

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 160.0
- avg_profit_gp: -864.0
- avg_meaningful_watches: 11.0
- avg_idle_watches: 4.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Preserve': 110}
- team: Resource
- office: Preservation Lead
**Observations**
- Toma Glass (Resource/Preservation Lead): avg meaningful Watch marks 11.0, idle-ish rests 4.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Preserve': 110}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: director

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -864.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 160.0
- avg_pressure_peak: 6.0
- avg_supply_end: 44.0
- avg_abandoned_cargo_gp: 0.0
- avg_abandoned_load: 6.0
- avg_downed_or_dead: 2.0
- avg_extraction_test_fails: 1.2
- avg_complications: 12.0
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
**Observations**
- Across 10 seeded runs, outcomes={'haven': 10}; objective_met=0.0%; Haven=100.0%; sealed=0.0%.
- Average elapsed 160.0h; peak Pressure avg 6.0; extraction test failures avg 1.2.
- At-risk cargo was stated before every extraction response (sim enforces Director Quick Procedure §Resolving a cargo loss).
- Pack 01 combat findings unavailable (0 result JSON); assumed class checks use bible tier DC + listed lead mods only.
**Rules questions**
- When evening Rest Watch workers Establish Camp, does their missed Rest grant Strain the same day or only after 24h without Rest (bible §5 vs camp example)?
- Does Attention-tagged cargo increase Pressure every active Watch or once while carried (bible §7 lists condition but not stacking cadence)?
- Extraction Test 'major route transition' interval is undefined numerically — sim used every 4 Progress as a Director ruling.
**Exploits**
- Abort-continue then immediately extract still paid the +1 Pressure once — easy to miss if Directors treat abort as soft advice.
**Recommendations**
- Publish a one-page Watch checklist card matching bible Quick Reference (assignments → 1/3 Supply → activities → Progress → Pressure → d6).
- Define Extraction Test spacing (per Length segment, per Gate, or per N Progress) with a worked table.
- Clarify Attention Pressure cadence and Rest-debt timing for the 3-worker evening camp pattern.

### Agent: quartermaster-auditor

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -864.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 160.0
- avg_pressure_peak: 6.0
- avg_supply_end: 44.0
- avg_abandoned_cargo_gp: 0.0
- avg_abandoned_load: 6.0
- avg_downed_or_dead: 2.0
- avg_extraction_test_fails: 1.2
- avg_complications: 12.0
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- mismatch_notes: []
- avg_supply_shortfalls: 0.2
**Observations**
- Independent recalc: avg abandoned cargo 0.0 gp / 6.0 Load; avg net after sponsor 0.0 gp.
- Daily Supply 12 for 12 Medium PCs matches bible §9; Watch consumption used 1/3 daily (bible worked example Watch One).
- Prep free-Load bookkeeping mismatches noted in 0 run annotations (scenario cargo overrides).
- Living cargo Load 6 + two Downed (12) on Capacity-constrained routes reliably forced Progress-1 and Pressure+1 (bible §6 Load>Capacity).
- Sponsor shares applied per bible table defaults (guild 20% / merchant 30% / noble 35% / sovereign 45%) by scenario.
**Rules questions**
- Are wages paid from net-after-sponsor or before sponsor share? Bible says net is after taxes before wages — wage timing vs profitability tests is ambiguous for 'profitable' definition.
- Does convoy Capacity equal route Capacity or a separate transport rating? Prep example uses convoy 100 vs route Capacity 80.
**Exploits**
- Forage can outpace Supply consumption on Tier I Mapped routes, making Supply tension weak unless complications tax Supply.
- Priority-1 bulk salvage is a 'dump valve' that makes Extraction Failures feel costless when high-priority lots are safe.
**Recommendations**
- Add a profitability definition to the expedition charter: profit after sponsor+wages+repairs vs gross extraction value.
- Cap Forage output by biome and require exposed risk, or Supply will rarely threaten Mapped Tier I runs.
- Require at least one mid-priority lot so Extraction Failures create real choice rather than discarding junk.

### Agent: rules-observer

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -864.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 160.0
- avg_pressure_peak: 6.0
- avg_supply_end: 44.0
- avg_abandoned_cargo_gp: 0.0
- avg_abandoned_load: 6.0
- avg_downed_or_dead: 2.0
- avg_extraction_test_fails: 1.2
- avg_complications: 12.0
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- team_sizes: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}
- undersized_teams: ['Combat']
**Observations**
- All 12 roster agents received Watch assignments every active Watch; evening Rest used 3 workers / 9 resters (bible camp example).
- Team sizes this roster: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}. Undersized vs bible optimal bands: ['Combat'].
- Parallel resolution: 5 team checks per active Watch is manageable; bottleneck is cargo priority + extraction response, not combat initiative.
- SOURCE_MANIFEST gaps: docs/mechanics/GAMEPLAY_LOOP_CANON.md missing; src/data/gameplay-loop.json missing; ExpeditionTracker.tsx missing. Used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt + haven.json + dungeon-mechanics.json.
- Decision bottlenecks recurring: ['Extraction response: abandoned at-risk cargo to save clock/Pressure']
**Rules questions**
- Player Rulebook expedition periods (morning/afternoon/evening) vs Gameplay Loop Watch (8h, two active + one Rest) — confirm they are the same layer or dual systems.
- Combat optimal 4–6 vs this pack's 3 Combat PCs: is the Brass Lantern worked example intentionally below band?
**Exploits**
- Unknown routes with 0 Progress until recon succeeds can soft-lock Horn-adjacent starts if recon fails repeatedly (mitigated by assistants + high mods).
**Recommendations**
- Ship companion ExpeditionTracker matching bible Watch checklist; SOURCE_MANIFEST currently points at a missing component.
- Add explicit crosswalk: Rulebook 'periods' = Loop 'Watches' to prevent dual-system confusion during onboarding.
- Either expand Combat to 4+ in the sample company or revise optimal band examples to include 3-combat professional companies.

## Scenario: EXP-HAVEN-RUN

### Agent: 01-mara-vann

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 11.8
- avg_idle_watches: 5.2
- avg_end_strain: 0.0
- downed_or_dead_pct: 10.0
- activity_counts: {'Advance': 43, 'Patrol': 30, 'Escort': 44}
- team: Combat
- office: Expedition Leader
**Observations**
- Mara Venn (Combat/Expedition Leader): avg meaningful Watch marks 11.8, idle-ish rests 5.2, end Strain 0.0, downed/dead rate 10.0%.
- Top activities: {'Escort': 44, 'Advance': 43, 'Patrol': 30}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 02-orrik-stonewake

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 11.8
- avg_idle_watches: 5.1
- avg_end_strain: 0.0
- downed_or_dead_pct: 10.0
- activity_counts: {'Advance': 43, 'Patrol': 30, 'Escort': 43}
- team: Combat
- office: Rear Guard
**Observations**
- Orrik Stonewake (Combat/Rear Guard): avg meaningful Watch marks 11.8, idle-ish rests 5.1, end Strain 0.0, downed/dead rate 10.0%.
- Top activities: {'Advance': 43, 'Escort': 43, 'Patrol': 30}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 03-taran-ashward

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 11.9
- avg_idle_watches: 5.1
- avg_end_strain: 0.0
- downed_or_dead_pct: 10.0
- activity_counts: {'Advance': 43, 'Patrol': 30, 'Escort': 44}
- team: Combat
- office: Escort Lead
**Observations**
- Taran Ashward (Combat/Escort Lead): avg meaningful Watch marks 11.9, idle-ish rests 5.1, end Strain 0.0, downed/dead rate 10.0%.
- Top activities: {'Escort': 44, 'Advance': 43, 'Patrol': 30}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 04-salira-dusk

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 22.6
- avg_idle_watches: 0.0
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Scout Ahead': 43, 'Conceal Trail': 100, 'Counter-Ambush': 30}
- team: Reconnaissance
- office: Routekeeper
**Observations**
- Salira Dusk (Reconnaissance/Routekeeper): avg meaningful Watch marks 22.6, idle-ish rests 0.0, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 100, 'Scout Ahead': 43, 'Counter-Ambush': 30}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 05-pell-quickstep

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 22.6
- avg_idle_watches: 0.0
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Scout Ahead': 43, 'Conceal Trail': 100, 'Counter-Ambush': 30}
- team: Reconnaissance
- office: Scout
**Observations**
- Pell Quickstep (Reconnaissance/Scout): avg meaningful Watch marks 22.6, idle-ish rests 0.0, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 100, 'Scout Ahead': 43, 'Counter-Ambush': 30}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 06-edrin-vale

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 12.0
- avg_idle_watches: 5.3
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 120}
- team: Research
- office: Claimant of Record
**Observations**
- Edrin Vale (Research/Claimant of Record): avg meaningful Watch marks 12.0, idle-ish rests 5.3, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Identify': 120}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 07-ysabel-threadseer

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 12.0
- avg_idle_watches: 5.3
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 120}
- team: Research
- office: Risk Analyst
**Observations**
- Ysabel Threadseer (Research/Risk Analyst): avg meaningful Watch marks 12.0, idle-ish rests 5.3, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Identify': 120}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 08-harka-reed

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 12.0
- avg_idle_watches: 5.3
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Forage': 43, 'Harvest': 30, 'Preserve': 47}
- team: Resource
- office: Harvester
**Observations**
- Harka Reed (Resource/Harvester): avg meaningful Watch marks 12.0, idle-ish rests 5.3, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Preserve': 47, 'Forage': 43, 'Harvest': 30}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: 09-zeetes

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 17.3
- avg_idle_watches: 0.0
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 43, 'Preserve': 30, 'Transport': 47}
- team: Support
- office: Quartermaster
**Observations**
- Zeetes (Support/Quartermaster): avg meaningful Watch marks 17.3, idle-ish rests 0.0, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Transport': 47, 'Establish Camp': 43, 'Preserve': 30}.
- Extraction Tests centered on Quartermaster lead; failures forced visible cargo priority choices.
**Rules questions**
- Is vehicle/tool proficiency intended to replace Survival for Extraction Tests when no vehicle is present?
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 10-durn-stonevow

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 12.0
- avg_idle_watches: 5.3
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 43, 'Preserve': 30, 'Transport': 47}
- team: Support
- office: Surgeon
**Observations**
- Durn Stonevow (Support/Surgeon): avg meaningful Watch marks 12.0, idle-ish rests 5.3, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Transport': 47, 'Establish Camp': 43, 'Preserve': 30}.
- Treat Watches competed with Transport during casualty extraction — real office conflict.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 11-ilse-harrow

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 12.0
- avg_idle_watches: 5.3
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 43, 'Preserve': 30, 'Transport': 47}
- team: Support
- office: Transport Chief
**Observations**
- Ilse Harrow (Support/Transport Chief): avg meaningful Watch marks 12.0, idle-ish rests 5.3, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Transport': 47, 'Establish Camp': 43, 'Preserve': 30}.
- Capacity-constrained Load made Transport assignment meaningful every extract Watch.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 12-toma-glass

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 147.2
- avg_profit_gp: 342.8
- avg_meaningful_watches: 12.0
- avg_idle_watches: 5.3
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Forage': 43, 'Harvest': 30, 'Preserve': 47}
- team: Resource
- office: Preservation Lead
**Observations**
- Toma Glass (Resource/Preservation Lead): avg meaningful Watch marks 12.0, idle-ish rests 5.3, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Preserve': 47, 'Forage': 43, 'Harvest': 30}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: director

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: 342.8
- avg_net_after_sponsor_gp: 1296.8
- avg_elapsed_hours: 147.2
- avg_pressure_peak: 5.7
- avg_supply_end: 151.6
- avg_abandoned_cargo_gp: 2230.0
- avg_abandoned_load: 16.2
- avg_downed_or_dead: 0.3
- avg_extraction_test_fails: 0.3
- avg_complications: 8.2
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
**Observations**
- Across 10 seeded runs, outcomes={'haven': 10}; objective_met=0.0%; Haven=100.0%; sealed=0.0%.
- Average elapsed 147.2h; peak Pressure avg 5.7; extraction test failures avg 0.3.
- At-risk cargo was stated before every extraction response (sim enforces Director Quick Procedure §Resolving a cargo loss).
- Pack 01 combat findings unavailable (0 result JSON); assumed class checks use bible tier DC + listed lead mods only.
**Rules questions**
- When evening Rest Watch workers Establish Camp, does their missed Rest grant Strain the same day or only after 24h without Rest (bible §5 vs camp example)?
- Does Attention-tagged cargo increase Pressure every active Watch or once while carried (bible §7 lists condition but not stacking cadence)?
- Extraction Test 'major route transition' interval is undefined numerically — sim used every 4 Progress as a Director ruling.
**Exploits**
- Abort-continue then immediately extract still paid the +1 Pressure once — easy to miss if Directors treat abort as soft advice.
**Recommendations**
- Publish a one-page Watch checklist card matching bible Quick Reference (assignments → 1/3 Supply → activities → Progress → Pressure → d6).
- Define Extraction Test spacing (per Length segment, per Gate, or per N Progress) with a worked table.
- Clarify Attention Pressure cadence and Rest-debt timing for the 3-worker evening camp pattern.

### Agent: quartermaster-auditor

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: 342.8
- avg_net_after_sponsor_gp: 1296.8
- avg_elapsed_hours: 147.2
- avg_pressure_peak: 5.7
- avg_supply_end: 151.6
- avg_abandoned_cargo_gp: 2230.0
- avg_abandoned_load: 16.2
- avg_downed_or_dead: 0.3
- avg_extraction_test_fails: 0.3
- avg_complications: 8.2
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- mismatch_notes: []
- avg_supply_shortfalls: 0.0
**Observations**
- Independent recalc: avg abandoned cargo 2230.0 gp / 16.2 Load; avg net after sponsor 1296.8 gp.
- Daily Supply 12 for 12 Medium PCs matches bible §9; Watch consumption used 1/3 daily (bible worked example Watch One).
- Prep free-Load bookkeeping mismatches noted in 0 run annotations (scenario cargo overrides).
- Living cargo Load 6 + two Downed (12) on Capacity-constrained routes reliably forced Progress-1 and Pressure+1 (bible §6 Load>Capacity).
- Sponsor shares applied per bible table defaults (guild 20% / merchant 30% / noble 35% / sovereign 45%) by scenario.
**Rules questions**
- Are wages paid from net-after-sponsor or before sponsor share? Bible says net is after taxes before wages — wage timing vs profitability tests is ambiguous for 'profitable' definition.
- Does convoy Capacity equal route Capacity or a separate transport rating? Prep example uses convoy 100 vs route Capacity 80.
**Exploits**
- Forage can outpace Supply consumption on Tier I Mapped routes, making Supply tension weak unless complications tax Supply.
- Priority-1 bulk salvage is a 'dump valve' that makes Extraction Failures feel costless when high-priority lots are safe.
**Recommendations**
- Add a profitability definition to the expedition charter: profit after sponsor+wages+repairs vs gross extraction value.
- Cap Forage output by biome and require exposed risk, or Supply will rarely threaten Mapped Tier I runs.
- Require at least one mid-priority lot so Extraction Failures create real choice rather than discarding junk.

### Agent: rules-observer

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: 342.8
- avg_net_after_sponsor_gp: 1296.8
- avg_elapsed_hours: 147.2
- avg_pressure_peak: 5.7
- avg_supply_end: 151.6
- avg_abandoned_cargo_gp: 2230.0
- avg_abandoned_load: 16.2
- avg_downed_or_dead: 0.3
- avg_extraction_test_fails: 0.3
- avg_complications: 8.2
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- team_sizes: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}
- undersized_teams: ['Combat']
**Observations**
- All 12 roster agents received Watch assignments every active Watch; evening Rest used 3 workers / 9 resters (bible camp example).
- Team sizes this roster: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}. Undersized vs bible optimal bands: ['Combat'].
- Parallel resolution: 5 team checks per active Watch is manageable; bottleneck is cargo priority + extraction response, not combat initiative.
- SOURCE_MANIFEST gaps: docs/mechanics/GAMEPLAY_LOOP_CANON.md missing; src/data/gameplay-loop.json missing; ExpeditionTracker.tsx missing. Used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt + haven.json + dungeon-mechanics.json.
- Decision bottlenecks recurring: ['Extraction response: abandoned at-risk cargo to save clock/Pressure', 'Extraction response: spent 8h rather than abandon cargo']
**Rules questions**
- Player Rulebook expedition periods (morning/afternoon/evening) vs Gameplay Loop Watch (8h, two active + one Rest) — confirm they are the same layer or dual systems.
- Combat optimal 4–6 vs this pack's 3 Combat PCs: is the Brass Lantern worked example intentionally below band?
**Exploits**
- Unknown routes with 0 Progress until recon succeeds can soft-lock Horn-adjacent starts if recon fails repeatedly (mitigated by assistants + high mods).
**Recommendations**
- Ship companion ExpeditionTracker matching bible Watch checklist; SOURCE_MANIFEST currently points at a missing component.
- Add explicit crosswalk: Rulebook 'periods' = Loop 'Watches' to prevent dual-system confusion during onboarding.
- Either expand Combat to 4+ in the sample company or revise optimal band examples to include 3-combat professional companies.

## Scenario: EXP-HORN-RACE

### Agent: 01-mara-vann

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 8.0
- avg_idle_watches: 3.3
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Escort': 120}
- team: Combat
- office: Expedition Leader
**Observations**
- Mara Venn (Combat/Expedition Leader): avg meaningful Watch marks 8.0, idle-ish rests 3.3, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Escort': 120}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 02-orrik-stonewake

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 7.5
- avg_idle_watches: 2.7
- avg_end_strain: 0.6
- downed_or_dead_pct: 13.3
- activity_counts: {'Escort': 104}
- team: Combat
- office: Rear Guard
**Observations**
- Orrik Stonewake (Combat/Rear Guard): avg meaningful Watch marks 7.5, idle-ish rests 2.7, end Strain 0.6, downed/dead rate 13.3%.
- Top activities: {'Escort': 104}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 03-taran-ashward

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 8.0
- avg_idle_watches: 3.3
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Escort': 120}
- team: Combat
- office: Escort Lead
**Observations**
- Taran Ashward (Combat/Escort Lead): avg meaningful Watch marks 8.0, idle-ish rests 3.3, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Escort': 120}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 04-salira-dusk

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 14.5
- avg_idle_watches: 0.0
- avg_end_strain: 0.67
- downed_or_dead_pct: 0.0
- activity_counts: {'Conceal Trail': 169}
- team: Reconnaissance
- office: Routekeeper
**Observations**
- Salira Dusk (Reconnaissance/Routekeeper): avg meaningful Watch marks 14.5, idle-ish rests 0.0, end Strain 0.67, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 169}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
- Compromised route made Conceal Trail and Progress rate the critical path to beat Horn 1200.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 05-pell-quickstep

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 14.5
- avg_idle_watches: 0.0
- avg_end_strain: 0.67
- downed_or_dead_pct: 0.0
- activity_counts: {'Conceal Trail': 169}
- team: Reconnaissance
- office: Scout
**Observations**
- Pell Quickstep (Reconnaissance/Scout): avg meaningful Watch marks 14.5, idle-ish rests 0.0, end Strain 0.67, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 169}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
- Compromised route made Conceal Trail and Progress rate the critical path to beat Horn 1200.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 06-edrin-vale

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 8.0
- avg_idle_watches: 3.3
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 120}
- team: Research
- office: Claimant of Record
**Observations**
- Edrin Vale (Research/Claimant of Record): avg meaningful Watch marks 8.0, idle-ish rests 3.3, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Identify': 120}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 07-ysabel-threadseer

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 8.0
- avg_idle_watches: 3.3
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 120}
- team: Research
- office: Risk Analyst
**Observations**
- Ysabel Threadseer (Research/Risk Analyst): avg meaningful Watch marks 8.0, idle-ish rests 3.3, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Identify': 120}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 08-harka-reed

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 8.0
- avg_idle_watches: 3.3
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Preserve': 120}
- team: Resource
- office: Harvester
**Observations**
- Harka Reed (Resource/Harvester): avg meaningful Watch marks 8.0, idle-ish rests 3.3, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Preserve': 120}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: 09-zeetes

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 12.4
- avg_idle_watches: 0.0
- avg_end_strain: 0.67
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 120, 'Establish Camp': 17}
- team: Support
- office: Quartermaster
**Observations**
- Zeetes (Support/Quartermaster): avg meaningful Watch marks 12.4, idle-ish rests 0.0, end Strain 0.67, downed/dead rate 0.0%.
- Top activities: {'Transport': 120, 'Establish Camp': 17}.
- Extraction Tests centered on Quartermaster lead; failures forced visible cargo priority choices.
**Rules questions**
- Is vehicle/tool proficiency intended to replace Survival for Extraction Tests when no vehicle is present?
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 10-durn-stonevow

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 9.1
- avg_idle_watches: 3.3
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 120, 'Establish Camp': 17}
- team: Support
- office: Surgeon
**Observations**
- Durn Stonevow (Support/Surgeon): avg meaningful Watch marks 9.1, idle-ish rests 3.3, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Transport': 120, 'Establish Camp': 17}.
- Treat Watches competed with Transport during casualty extraction — real office conflict.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 11-ilse-harrow

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 9.1
- avg_idle_watches: 3.3
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 120, 'Establish Camp': 17}
- team: Support
- office: Transport Chief
**Observations**
- Ilse Harrow (Support/Transport Chief): avg meaningful Watch marks 9.1, idle-ish rests 3.3, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Transport': 120, 'Establish Camp': 17}.
- Capacity-constrained Load made Transport assignment meaningful every extract Watch.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 12-toma-glass

**Metrics**
- iterations: 15
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- avg_elapsed_hours: 107.7
- avg_profit_gp: -216.0
- avg_meaningful_watches: 8.0
- avg_idle_watches: 3.3
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Preserve': 120}
- team: Resource
- office: Preservation Lead
**Observations**
- Toma Glass (Resource/Preservation Lead): avg meaningful Watch marks 8.0, idle-ish rests 3.3, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Preserve': 120}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: director

**Metrics**
- iterations: 15
- outcomes: {'sealed': 9, 'haven': 6}
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- sealed_pct: 60.0
- avg_profit_gp: -216.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 107.7
- avg_pressure_peak: 6.0
- avg_supply_end: 16.1
- avg_abandoned_cargo_gp: 2333.3
- avg_abandoned_load: 30.9
- avg_downed_or_dead: 0.13
- avg_extraction_test_fails: 0.07
- avg_complications: 6.4
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
**Observations**
- Across 15 seeded runs, outcomes={'sealed': 9, 'haven': 6}; objective_met=40.0%; Haven=40.0%; sealed=60.0%.
- Average elapsed 107.7h; peak Pressure avg 6.0; extraction test failures avg 0.07.
- At-risk cargo was stated before every extraction response (sim enforces Director Quick Procedure §Resolving a cargo loss).
- Pack 01 combat findings unavailable (0 result JSON); assumed class checks use bible tier DC + listed lead mods only.
- Horn race from hour 1080→1200: sealed_pct=60.0. Compromised Mapped→Sketched halves Progress and stretches clock.
**Rules questions**
- When evening Rest Watch workers Establish Camp, does their missed Rest grant Strain the same day or only after 24h without Rest (bible §5 vs camp example)?
- Does Attention-tagged cargo increase Pressure every active Watch or once while carried (bible §7 lists condition but not stacking cadence)?
- Extraction Test 'major route transition' interval is undefined numerically — sim used every 4 Progress as a Director ruling.
**Exploits**
- Abort-continue then immediately extract still paid the +1 Pressure once — easy to miss if Directors treat abort as soft advice.
**Recommendations**
- Publish a one-page Watch checklist card matching bible Quick Reference (assignments → 1/3 Supply → activities → Progress → Pressure → d6).
- Define Extraction Test spacing (per Length segment, per Gate, or per N Progress) with a worked table.
- Clarify Attention Pressure cadence and Rest-debt timing for the 3-worker evening camp pattern.

### Agent: quartermaster-auditor

**Metrics**
- iterations: 15
- outcomes: {'sealed': 9, 'haven': 6}
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- sealed_pct: 60.0
- avg_profit_gp: -216.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 107.7
- avg_pressure_peak: 6.0
- avg_supply_end: 16.1
- avg_abandoned_cargo_gp: 2333.3
- avg_abandoned_load: 30.9
- avg_downed_or_dead: 0.13
- avg_extraction_test_fails: 0.07
- avg_complications: 6.4
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- mismatch_notes: []
- avg_supply_shortfalls: 0.67
**Observations**
- Independent recalc: avg abandoned cargo 2333.3 gp / 30.9 Load; avg net after sponsor 0.0 gp.
- Daily Supply 12 for 12 Medium PCs matches bible §9; Watch consumption used 1/3 daily (bible worked example Watch One).
- Prep free-Load bookkeeping mismatches noted in 0 run annotations (scenario cargo overrides).
- Living cargo Load 6 + two Downed (12) on Capacity-constrained routes reliably forced Progress-1 and Pressure+1 (bible §6 Load>Capacity).
- Sponsor shares applied per bible table defaults (guild 20% / merchant 30% / noble 35% / sovereign 45%) by scenario.
**Rules questions**
- Are wages paid from net-after-sponsor or before sponsor share? Bible says net is after taxes before wages — wage timing vs profitability tests is ambiguous for 'profitable' definition.
- Does convoy Capacity equal route Capacity or a separate transport rating? Prep example uses convoy 100 vs route Capacity 80.
**Exploits**
- Forage can outpace Supply consumption on Tier I Mapped routes, making Supply tension weak unless complications tax Supply.
- Priority-1 bulk salvage is a 'dump valve' that makes Extraction Failures feel costless when high-priority lots are safe.
**Recommendations**
- Add a profitability definition to the expedition charter: profit after sponsor+wages+repairs vs gross extraction value.
- Cap Forage output by biome and require exposed risk, or Supply will rarely threaten Mapped Tier I runs.
- Require at least one mid-priority lot so Extraction Failures create real choice rather than discarding junk.

### Agent: rules-observer

**Metrics**
- iterations: 15
- outcomes: {'sealed': 9, 'haven': 6}
- objective_met_pct: 40.0
- haven_arrival_pct: 40.0
- sealed_pct: 60.0
- avg_profit_gp: -216.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 107.7
- avg_pressure_peak: 6.0
- avg_supply_end: 16.1
- avg_abandoned_cargo_gp: 2333.3
- avg_abandoned_load: 30.9
- avg_downed_or_dead: 0.13
- avg_extraction_test_fails: 0.07
- avg_complications: 6.4
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- team_sizes: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}
- undersized_teams: ['Combat']
**Observations**
- All 12 roster agents received Watch assignments every active Watch; evening Rest used 3 workers / 9 resters (bible camp example).
- Team sizes this roster: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}. Undersized vs bible optimal bands: ['Combat'].
- Parallel resolution: 5 team checks per active Watch is manageable; bottleneck is cargo priority + extraction response, not combat initiative.
- SOURCE_MANIFEST gaps: docs/mechanics/GAMEPLAY_LOOP_CANON.md missing; src/data/gameplay-loop.json missing; ExpeditionTracker.tsx missing. Used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt + haven.json + dungeon-mechanics.json.
- Decision bottlenecks recurring: ['Extraction response: abandoned at-risk cargo to save clock/Pressure']
**Rules questions**
- Player Rulebook expedition periods (morning/afternoon/evening) vs Gameplay Loop Watch (8h, two active + one Rest) — confirm they are the same layer or dual systems.
- Combat optimal 4–6 vs this pack's 3 Combat PCs: is the Brass Lantern worked example intentionally below band?
**Exploits**
- Unknown routes with 0 Progress until recon succeeds can soft-lock Horn-adjacent starts if recon fails repeatedly (mitigated by assistants + high mods).
**Recommendations**
- Ship companion ExpeditionTracker matching bible Watch checklist; SOURCE_MANIFEST currently points at a missing component.
- Add explicit crosswalk: Rulebook 'periods' = Loop 'Watches' to prevent dual-system confusion during onboarding.
- Either expand Combat to 4+ in the sample company or revise optimal band examples to include 3-combat professional companies.

## Scenario: EXP-T1-PROFIT

### Agent: 01-mara-vann

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.6
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Advance': 25, 'Patrol': 9, 'Escort': 31}
- team: Combat
- office: Expedition Leader
**Observations**
- Mara Venn (Combat/Expedition Leader): avg meaningful Watch marks 6.5, idle-ish rests 2.6, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Escort': 31, 'Advance': 25, 'Patrol': 9}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 02-orrik-stonewake

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.6
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Advance': 25, 'Patrol': 9, 'Escort': 31}
- team: Combat
- office: Rear Guard
**Observations**
- Orrik Stonewake (Combat/Rear Guard): avg meaningful Watch marks 6.5, idle-ish rests 2.6, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Escort': 31, 'Advance': 25, 'Patrol': 9}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 03-taran-ashward

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.3
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Advance': 23, 'Patrol': 9, 'Escort': 30}
- team: Combat
- office: Escort Lead
**Observations**
- Taran Ashward (Combat/Escort Lead): avg meaningful Watch marks 6.5, idle-ish rests 2.3, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Escort': 30, 'Advance': 23, 'Patrol': 9}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 04-salira-dusk

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 11.7
- avg_idle_watches: 0.0
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Scout Ahead': 25, 'Conceal Trail': 56, 'Counter-Ambush': 10}
- team: Reconnaissance
- office: Routekeeper
**Observations**
- Salira Dusk (Reconnaissance/Routekeeper): avg meaningful Watch marks 11.7, idle-ish rests 0.0, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 56, 'Scout Ahead': 25, 'Counter-Ambush': 10}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 05-pell-quickstep

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 11.7
- avg_idle_watches: 0.0
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Scout Ahead': 25, 'Conceal Trail': 56, 'Counter-Ambush': 10}
- team: Reconnaissance
- office: Scout
**Observations**
- Pell Quickstep (Reconnaissance/Scout): avg meaningful Watch marks 11.7, idle-ish rests 0.0, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 56, 'Scout Ahead': 25, 'Counter-Ambush': 10}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 06-edrin-vale

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.6
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 65}
- team: Research
- office: Claimant of Record
**Observations**
- Edrin Vale (Research/Claimant of Record): avg meaningful Watch marks 6.5, idle-ish rests 2.6, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Identify': 65}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 07-ysabel-threadseer

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.6
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 65}
- team: Research
- office: Risk Analyst
**Observations**
- Ysabel Threadseer (Research/Risk Analyst): avg meaningful Watch marks 6.5, idle-ish rests 2.6, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Identify': 65}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 08-harka-reed

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.6
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Forage': 25, 'Harvest': 10, 'Preserve': 30}
- team: Resource
- office: Harvester
**Observations**
- Harka Reed (Resource/Harvester): avg meaningful Watch marks 6.5, idle-ish rests 2.6, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Preserve': 30, 'Forage': 25, 'Harvest': 10}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: 09-zeetes

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 9.1
- avg_idle_watches: 0.0
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 25, 'Preserve': 9, 'Transport': 30, 'Treat': 1}
- team: Support
- office: Quartermaster
**Observations**
- Zeetes (Support/Quartermaster): avg meaningful Watch marks 9.1, idle-ish rests 0.0, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Transport': 30, 'Establish Camp': 25, 'Preserve': 9, 'Treat': 1}.
- Extraction Tests centered on Quartermaster lead; failures forced visible cargo priority choices.
**Rules questions**
- Is vehicle/tool proficiency intended to replace Survival for Extraction Tests when no vehicle is present?
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 10-durn-stonevow

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.6
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 25, 'Preserve': 9, 'Transport': 30, 'Treat': 1}
- team: Support
- office: Surgeon
**Observations**
- Durn Stonevow (Support/Surgeon): avg meaningful Watch marks 6.5, idle-ish rests 2.6, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Transport': 30, 'Establish Camp': 25, 'Preserve': 9, 'Treat': 1}.
- Treat Watches competed with Transport during casualty extraction — real office conflict.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 11-ilse-harrow

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.6
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 25, 'Preserve': 9, 'Transport': 30, 'Treat': 1}
- team: Support
- office: Transport Chief
**Observations**
- Ilse Harrow (Support/Transport Chief): avg meaningful Watch marks 6.5, idle-ish rests 2.6, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Transport': 30, 'Establish Camp': 25, 'Preserve': 9, 'Treat': 1}.
- Capacity-constrained Load made Transport assignment meaningful every extract Watch.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 12-toma-glass

**Metrics**
- iterations: 10
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 68.0
- avg_profit_gp: -382.9
- avg_meaningful_watches: 6.5
- avg_idle_watches: 2.6
- avg_end_strain: 0.0
- downed_or_dead_pct: 0.0
- activity_counts: {'Forage': 25, 'Harvest': 10, 'Preserve': 30}
- team: Resource
- office: Preservation Lead
**Observations**
- Toma Glass (Resource/Preservation Lead): avg meaningful Watch marks 6.5, idle-ish rests 2.6, end Strain 0.0, downed/dead rate 0.0%.
- Top activities: {'Preserve': 30, 'Forage': 25, 'Harvest': 10}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: director

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -382.9
- avg_net_after_sponsor_gp: 85.1
- avg_elapsed_hours: 68.0
- avg_pressure_peak: 2.0
- avg_supply_end: 104.7
- avg_abandoned_cargo_gp: 0.0
- avg_abandoned_load: 0.0
- avg_downed_or_dead: 0.0
- avg_extraction_test_fails: 0.0
- avg_complications: 1.1
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
**Observations**
- Across 10 seeded runs, outcomes={'haven': 10}; objective_met=0.0%; Haven=100.0%; sealed=0.0%.
- Average elapsed 68.0h; peak Pressure avg 2.0; extraction test failures avg 0.0.
- At-risk cargo was stated before every extraction response (sim enforces Director Quick Procedure §Resolving a cargo loss).
- Pack 01 combat findings unavailable (0 result JSON); assumed class checks use bible tier DC + listed lead mods only.
**Rules questions**
- When evening Rest Watch workers Establish Camp, does their missed Rest grant Strain the same day or only after 24h without Rest (bible §5 vs camp example)?
- Does Attention-tagged cargo increase Pressure every active Watch or once while carried (bible §7 lists condition but not stacking cadence)?
- Extraction Test 'major route transition' interval is undefined numerically — sim used every 4 Progress as a Director ruling.
**Exploits**
- Abort-continue then immediately extract still paid the +1 Pressure once — easy to miss if Directors treat abort as soft advice.
**Recommendations**
- Publish a one-page Watch checklist card matching bible Quick Reference (assignments → 1/3 Supply → activities → Progress → Pressure → d6).
- Define Extraction Test spacing (per Length segment, per Gate, or per N Progress) with a worked table.
- Clarify Attention Pressure cadence and Rest-debt timing for the 3-worker evening camp pattern.

### Agent: quartermaster-auditor

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -382.9
- avg_net_after_sponsor_gp: 85.1
- avg_elapsed_hours: 68.0
- avg_pressure_peak: 2.0
- avg_supply_end: 104.7
- avg_abandoned_cargo_gp: 0.0
- avg_abandoned_load: 0.0
- avg_downed_or_dead: 0.0
- avg_extraction_test_fails: 0.0
- avg_complications: 1.1
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- mismatch_notes: []
- avg_supply_shortfalls: 0.0
**Observations**
- Independent recalc: avg abandoned cargo 0.0 gp / 0.0 Load; avg net after sponsor 85.1 gp.
- Daily Supply 12 for 12 Medium PCs matches bible §9; Watch consumption used 1/3 daily (bible worked example Watch One).
- Prep free-Load bookkeeping mismatches noted in 0 run annotations (scenario cargo overrides).
- Living cargo Load 6 + two Downed (12) on Capacity-constrained routes reliably forced Progress-1 and Pressure+1 (bible §6 Load>Capacity).
- Sponsor shares applied per bible table defaults (guild 20% / merchant 30% / noble 35% / sovereign 45%) by scenario.
**Rules questions**
- Are wages paid from net-after-sponsor or before sponsor share? Bible says net is after taxes before wages — wage timing vs profitability tests is ambiguous for 'profitable' definition.
- Does convoy Capacity equal route Capacity or a separate transport rating? Prep example uses convoy 100 vs route Capacity 80.
**Exploits**
- Forage can outpace Supply consumption on Tier I Mapped routes, making Supply tension weak unless complications tax Supply.
- Priority-1 bulk salvage is a 'dump valve' that makes Extraction Failures feel costless when high-priority lots are safe.
**Recommendations**
- Add a profitability definition to the expedition charter: profit after sponsor+wages+repairs vs gross extraction value.
- Cap Forage output by biome and require exposed risk, or Supply will rarely threaten Mapped Tier I runs.
- Require at least one mid-priority lot so Extraction Failures create real choice rather than discarding junk.

### Agent: rules-observer

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 0.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -382.9
- avg_net_after_sponsor_gp: 85.1
- avg_elapsed_hours: 68.0
- avg_pressure_peak: 2.0
- avg_supply_end: 104.7
- avg_abandoned_cargo_gp: 0.0
- avg_abandoned_load: 0.0
- avg_downed_or_dead: 0.0
- avg_extraction_test_fails: 0.0
- avg_complications: 1.1
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- team_sizes: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}
- undersized_teams: ['Combat']
**Observations**
- All 12 roster agents received Watch assignments every active Watch; evening Rest used 3 workers / 9 resters (bible camp example).
- Team sizes this roster: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}. Undersized vs bible optimal bands: ['Combat'].
- Parallel resolution: 5 team checks per active Watch is manageable; bottleneck is cargo priority + extraction response, not combat initiative.
- SOURCE_MANIFEST gaps: docs/mechanics/GAMEPLAY_LOOP_CANON.md missing; src/data/gameplay-loop.json missing; ExpeditionTracker.tsx missing. Used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt + haven.json + dungeon-mechanics.json.
- Decision bottlenecks recurring: []
**Rules questions**
- Player Rulebook expedition periods (morning/afternoon/evening) vs Gameplay Loop Watch (8h, two active + one Rest) — confirm they are the same layer or dual systems.
- Combat optimal 4–6 vs this pack's 3 Combat PCs: is the Brass Lantern worked example intentionally below band?
**Exploits**
- Unknown routes with 0 Progress until recon succeeds can soft-lock Horn-adjacent starts if recon fails repeatedly (mitigated by assistants + high mods).
**Recommendations**
- Ship companion ExpeditionTracker matching bible Watch checklist; SOURCE_MANIFEST currently points at a missing component.
- Add explicit crosswalk: Rulebook 'periods' = Loop 'Watches' to prevent dual-system confusion during onboarding.
- Either expand Combat to 4+ in the sample company or revise optimal band examples to include 3-combat professional companies.

## Scenario: EXP-T3-LONG

### Agent: 01-mara-vann

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 26.9
- avg_idle_watches: 12.6
- avg_end_strain: 0.2
- downed_or_dead_pct: 10.0
- activity_counts: {'Advance': 102, 'Patrol': 50, 'Escort': 115}
- team: Combat
- office: Expedition Leader
**Observations**
- Mara Venn (Combat/Expedition Leader): avg meaningful Watch marks 26.9, idle-ish rests 12.6, end Strain 0.2, downed/dead rate 10.0%.
- Top activities: {'Escort': 115, 'Advance': 102, 'Patrol': 50}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 02-orrik-stonewake

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 27.1
- avg_idle_watches: 12.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Advance': 102, 'Patrol': 50, 'Escort': 119}
- team: Combat
- office: Rear Guard
**Observations**
- Orrik Stonewake (Combat/Rear Guard): avg meaningful Watch marks 27.1, idle-ish rests 12.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Escort': 119, 'Advance': 102, 'Patrol': 50}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 03-taran-ashward

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 27.1
- avg_idle_watches: 12.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Advance': 102, 'Patrol': 50, 'Escort': 119}
- team: Combat
- office: Escort Lead
**Observations**
- Taran Ashward (Combat/Escort Lead): avg meaningful Watch marks 27.1, idle-ish rests 12.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Escort': 119, 'Advance': 102, 'Patrol': 50}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 04-salira-dusk

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 52.7
- avg_idle_watches: 0.0
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Scout Ahead': 102, 'Conceal Trail': 247, 'Map Route': 38, 'Counter-Ambush': 12}
- team: Reconnaissance
- office: Routekeeper
**Observations**
- Salira Dusk (Reconnaissance/Routekeeper): avg meaningful Watch marks 52.7, idle-ish rests 0.0, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 247, 'Scout Ahead': 102, 'Map Route': 38, 'Counter-Ambush': 12}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 05-pell-quickstep

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 52.7
- avg_idle_watches: 0.0
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Scout Ahead': 102, 'Conceal Trail': 247, 'Map Route': 38, 'Counter-Ambush': 12}
- team: Reconnaissance
- office: Scout
**Observations**
- Pell Quickstep (Reconnaissance/Scout): avg meaningful Watch marks 52.7, idle-ish rests 0.0, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 247, 'Scout Ahead': 102, 'Map Route': 38, 'Counter-Ambush': 12}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 06-edrin-vale

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 27.1
- avg_idle_watches: 12.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 271}
- team: Research
- office: Claimant of Record
**Observations**
- Edrin Vale (Research/Claimant of Record): avg meaningful Watch marks 27.1, idle-ish rests 12.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Identify': 271}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 07-ysabel-threadseer

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 27.1
- avg_idle_watches: 12.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 271}
- team: Research
- office: Risk Analyst
**Observations**
- Ysabel Threadseer (Research/Risk Analyst): avg meaningful Watch marks 27.1, idle-ish rests 12.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Identify': 271}.
- Identify raised cargo priority on EC≥2 lots, feeding extraction triage.
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 08-harka-reed

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 27.1
- avg_idle_watches: 12.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Forage': 102, 'Harvest': 50, 'Preserve': 119}
- team: Resource
- office: Harvester
**Observations**
- Harka Reed (Resource/Harvester): avg meaningful Watch marks 27.1, idle-ish rests 12.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Preserve': 119, 'Forage': 102, 'Harvest': 50}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
- Rare lot objective forced Preserve + Capacity management on Sketched Risk 3.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: 09-zeetes

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 40.0
- avg_idle_watches: 0.0
- avg_end_strain: 0.6
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 103, 'Preserve': 50, 'Transport': 119}
- team: Support
- office: Quartermaster
**Observations**
- Zeetes (Support/Quartermaster): avg meaningful Watch marks 40.0, idle-ish rests 0.0, end Strain 0.6, downed/dead rate 0.0%.
- Top activities: {'Transport': 119, 'Establish Camp': 103, 'Preserve': 50}.
- Extraction Tests centered on Quartermaster lead; failures forced visible cargo priority choices.
**Rules questions**
- Is vehicle/tool proficiency intended to replace Survival for Extraction Tests when no vehicle is present?
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 10-durn-stonevow

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 27.2
- avg_idle_watches: 12.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 103, 'Preserve': 50, 'Transport': 119}
- team: Support
- office: Surgeon
**Observations**
- Durn Stonevow (Support/Surgeon): avg meaningful Watch marks 27.2, idle-ish rests 12.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Transport': 119, 'Establish Camp': 103, 'Preserve': 50}.
- Treat Watches competed with Transport during casualty extraction — real office conflict.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 11-ilse-harrow

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 27.2
- avg_idle_watches: 12.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Establish Camp': 103, 'Preserve': 50, 'Transport': 119}
- team: Support
- office: Transport Chief
**Observations**
- Ilse Harrow (Support/Transport Chief): avg meaningful Watch marks 27.2, idle-ish rests 12.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Transport': 119, 'Establish Camp': 103, 'Preserve': 50}.
- Capacity-constrained Load made Transport assignment meaningful every extract Watch.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 12-toma-glass

**Metrics**
- iterations: 10
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- avg_elapsed_hours: 360.0
- avg_profit_gp: -1223.4
- avg_meaningful_watches: 27.1
- avg_idle_watches: 12.8
- avg_end_strain: 0.2
- downed_or_dead_pct: 0.0
- activity_counts: {'Forage': 102, 'Harvest': 50, 'Preserve': 119}
- team: Resource
- office: Preservation Lead
**Observations**
- Toma Glass (Resource/Preservation Lead): avg meaningful Watch marks 27.1, idle-ish rests 12.8, end Strain 0.2, downed/dead rate 0.0%.
- Top activities: {'Preserve': 119, 'Forage': 102, 'Harvest': 50}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
- Rare lot objective forced Preserve + Capacity management on Sketched Risk 3.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: director

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -1223.4
- avg_net_after_sponsor_gp: 1080.6
- avg_elapsed_hours: 360.0
- avg_pressure_peak: 6.0
- avg_supply_end: 156.6
- avg_abandoned_cargo_gp: 15900.0
- avg_abandoned_load: 24.0
- avg_downed_or_dead: 0.1
- avg_extraction_test_fails: 0.8
- avg_complications: 19.9
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
**Observations**
- Across 10 seeded runs, outcomes={'haven': 10}; objective_met=30.0%; Haven=100.0%; sealed=0.0%.
- Average elapsed 360.0h; peak Pressure avg 6.0; extraction test failures avg 0.8.
- At-risk cargo was stated before every extraction response (sim enforces Director Quick Procedure §Resolving a cargo loss).
- Pack 01 combat findings unavailable (0 result JSON); assumed class checks use bible tier DC + listed lead mods only.
**Rules questions**
- When evening Rest Watch workers Establish Camp, does their missed Rest grant Strain the same day or only after 24h without Rest (bible §5 vs camp example)?
- Does Attention-tagged cargo increase Pressure every active Watch or once while carried (bible §7 lists condition but not stacking cadence)?
- Extraction Test 'major route transition' interval is undefined numerically — sim used every 4 Progress as a Director ruling.
**Exploits**
- Abort-continue then immediately extract still paid the +1 Pressure once — easy to miss if Directors treat abort as soft advice.
**Recommendations**
- Publish a one-page Watch checklist card matching bible Quick Reference (assignments → 1/3 Supply → activities → Progress → Pressure → d6).
- Define Extraction Test spacing (per Length segment, per Gate, or per N Progress) with a worked table.
- Clarify Attention Pressure cadence and Rest-debt timing for the 3-worker evening camp pattern.

### Agent: quartermaster-auditor

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -1223.4
- avg_net_after_sponsor_gp: 1080.6
- avg_elapsed_hours: 360.0
- avg_pressure_peak: 6.0
- avg_supply_end: 156.6
- avg_abandoned_cargo_gp: 15900.0
- avg_abandoned_load: 24.0
- avg_downed_or_dead: 0.1
- avg_extraction_test_fails: 0.8
- avg_complications: 19.9
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- mismatch_notes: []
- avg_supply_shortfalls: 1.0
**Observations**
- Independent recalc: avg abandoned cargo 15900.0 gp / 24.0 Load; avg net after sponsor 1080.6 gp.
- Daily Supply 12 for 12 Medium PCs matches bible §9; Watch consumption used 1/3 daily (bible worked example Watch One).
- Prep free-Load bookkeeping mismatches noted in 0 run annotations (scenario cargo overrides).
- Living cargo Load 6 + two Downed (12) on Capacity-constrained routes reliably forced Progress-1 and Pressure+1 (bible §6 Load>Capacity).
- Sponsor shares applied per bible table defaults (guild 20% / merchant 30% / noble 35% / sovereign 45%) by scenario.
**Rules questions**
- Are wages paid from net-after-sponsor or before sponsor share? Bible says net is after taxes before wages — wage timing vs profitability tests is ambiguous for 'profitable' definition.
- Does convoy Capacity equal route Capacity or a separate transport rating? Prep example uses convoy 100 vs route Capacity 80.
**Exploits**
- Forage can outpace Supply consumption on Tier I Mapped routes, making Supply tension weak unless complications tax Supply.
- Priority-1 bulk salvage is a 'dump valve' that makes Extraction Failures feel costless when high-priority lots are safe.
**Recommendations**
- Add a profitability definition to the expedition charter: profit after sponsor+wages+repairs vs gross extraction value.
- Cap Forage output by biome and require exposed risk, or Supply will rarely threaten Mapped Tier I runs.
- Require at least one mid-priority lot so Extraction Failures create real choice rather than discarding junk.

### Agent: rules-observer

**Metrics**
- iterations: 10
- outcomes: {'haven': 10}
- objective_met_pct: 30.0
- haven_arrival_pct: 100.0
- sealed_pct: 0.0
- avg_profit_gp: -1223.4
- avg_net_after_sponsor_gp: 1080.6
- avg_elapsed_hours: 360.0
- avg_pressure_peak: 6.0
- avg_supply_end: 156.6
- avg_abandoned_cargo_gp: 15900.0
- avg_abandoned_load: 24.0
- avg_downed_or_dead: 0.1
- avg_extraction_test_fails: 0.8
- avg_complications: 19.9
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- team_sizes: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}
- undersized_teams: ['Combat']
**Observations**
- All 12 roster agents received Watch assignments every active Watch; evening Rest used 3 workers / 9 resters (bible camp example).
- Team sizes this roster: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}. Undersized vs bible optimal bands: ['Combat'].
- Parallel resolution: 5 team checks per active Watch is manageable; bottleneck is cargo priority + extraction response, not combat initiative.
- SOURCE_MANIFEST gaps: docs/mechanics/GAMEPLAY_LOOP_CANON.md missing; src/data/gameplay-loop.json missing; ExpeditionTracker.tsx missing. Used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt + haven.json + dungeon-mechanics.json.
- Decision bottlenecks recurring: ['Extraction response: abandoned at-risk cargo to save clock/Pressure', 'Extraction response: spent 8h rather than abandon cargo']
**Rules questions**
- Player Rulebook expedition periods (morning/afternoon/evening) vs Gameplay Loop Watch (8h, two active + one Rest) — confirm they are the same layer or dual systems.
- Combat optimal 4–6 vs this pack's 3 Combat PCs: is the Brass Lantern worked example intentionally below band?
**Exploits**
- Unknown routes with 0 Progress until recon succeeds can soft-lock Horn-adjacent starts if recon fails repeatedly (mitigated by assistants + high mods).
**Recommendations**
- Ship companion ExpeditionTracker matching bible Watch checklist; SOURCE_MANIFEST currently points at a missing component.
- Add explicit crosswalk: Rulebook 'periods' = Loop 'Watches' to prevent dual-system confusion during onboarding.
- Either expand Combat to 4+ in the sample company or revise optimal band examples to include 3-combat professional companies.

## Scenario: EXP-T4-DARK

### Agent: 01-mara-vann

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 31.6
- avg_idle_watches: 15.1
- avg_end_strain: 1.1
- downed_or_dead_pct: 10.0
- activity_counts: {'Advance': 140, 'Escort': 155, 'Patrol': 14}
- team: Combat
- office: Expedition Leader
**Observations**
- Mara Venn (Combat/Expedition Leader): avg meaningful Watch marks 31.6, idle-ish rests 15.1, end Strain 1.1, downed/dead rate 10.0%.
- Top activities: {'Escort': 155, 'Advance': 140, 'Patrol': 14}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 02-orrik-stonewake

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 27.4
- avg_idle_watches: 10.3
- avg_end_strain: 1.1
- downed_or_dead_pct: 50.0
- activity_counts: {'Advance': 101, 'Patrol': 14, 'Escort': 104}
- team: Combat
- office: Rear Guard
**Observations**
- Orrik Stonewake (Combat/Rear Guard): avg meaningful Watch marks 27.4, idle-ish rests 10.3, end Strain 1.1, downed/dead rate 50.0%.
- Top activities: {'Escort': 104, 'Advance': 101, 'Patrol': 14}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 03-taran-ashward

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 31.4
- avg_idle_watches: 14.8
- avg_end_strain: 1.1
- downed_or_dead_pct: 10.0
- activity_counts: {'Advance': 139, 'Escort': 151, 'Patrol': 14}
- team: Combat
- office: Escort Lead
**Observations**
- Taran Ashward (Combat/Escort Lead): avg meaningful Watch marks 31.4, idle-ish rests 14.8, end Strain 1.1, downed/dead rate 10.0%.
- Top activities: {'Escort': 151, 'Advance': 139, 'Patrol': 14}.
- Expedition stakes changed target choice: Escort/Advance preferred over chase kills when cargo or Downed present.
**Rules questions**
- Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
**Recommendations**
- Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.

### Agent: 04-salira-dusk

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 63.8
- avg_idle_watches: 0.0
- avg_end_strain: 3.9
- downed_or_dead_pct: 0.0
- activity_counts: {'Reconnaissance (open route)': 14, 'Scout Ahead': 126, 'Conceal Trail': 326, 'Map Route': 14}
- team: Reconnaissance
- office: Routekeeper
**Observations**
- Salira Dusk (Reconnaissance/Routekeeper): avg meaningful Watch marks 63.8, idle-ish rests 0.0, end Strain 3.9, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 326, 'Scout Ahead': 126, 'Reconnaissance (open route)': 14, 'Map Route': 14}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 05-pell-quickstep

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 63.8
- avg_idle_watches: 0.0
- avg_end_strain: 3.9
- downed_or_dead_pct: 0.0
- activity_counts: {'Reconnaissance (open route)': 14, 'Scout Ahead': 126, 'Conceal Trail': 326, 'Map Route': 14}
- team: Reconnaissance
- office: Scout
**Observations**
- Pell Quickstep (Reconnaissance/Scout): avg meaningful Watch marks 63.8, idle-ish rests 0.0, end Strain 3.9, downed/dead rate 0.0%.
- Top activities: {'Conceal Trail': 326, 'Scout Ahead': 126, 'Reconnaissance (open route)': 14, 'Map Route': 14}.
- Scout/Map/Conceal assignments remained relevant every phase; Mapping upgrades gated progress on Unknown/Sketched routes.
**Rules questions**
- How many Map Route successes are needed when Risk changes mid-expedition after compromise?
**Recommendations**
- Show Mapping upgrade progress as X/Risk on the route card.

### Agent: 06-edrin-vale

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 32.2
- avg_idle_watches: 15.8
- avg_end_strain: 1.1
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 308, 'Analyze Threat': 14}
- team: Research
- office: Claimant of Record
**Observations**
- Edrin Vale (Research/Claimant of Record): avg meaningful Watch marks 32.2, idle-ish rests 15.8, end Strain 1.1, downed/dead rate 0.0%.
- Top activities: {'Identify': 308, 'Analyze Threat': 14}.
- Risk Analyst / Claimant stayed on public-symptom Identify/Analyze; no hidden lore confirmation leaked to players.
**Rules questions**
- What public Research outputs are legal at Tier IV without violating Director dual-layer canon?
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 07-ysabel-threadseer

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 32.2
- avg_idle_watches: 15.8
- avg_end_strain: 1.1
- downed_or_dead_pct: 0.0
- activity_counts: {'Identify': 308, 'Analyze Threat': 14}
- team: Research
- office: Risk Analyst
**Observations**
- Ysabel Threadseer (Research/Risk Analyst): avg meaningful Watch marks 32.2, idle-ish rests 15.8, end Strain 1.1, downed/dead rate 0.0%.
- Top activities: {'Identify': 308, 'Analyze Threat': 14}.
- Risk Analyst / Claimant stayed on public-symptom Identify/Analyze; no hidden lore confirmation leaked to players.
**Rules questions**
- What public Research outputs are legal at Tier IV without violating Director dual-layer canon?
**Recommendations**
- Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.

### Agent: 08-harka-reed

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 32.2
- avg_idle_watches: 15.8
- avg_end_strain: 1.1
- downed_or_dead_pct: 0.0
- activity_counts: {'Forage': 140, 'Preserve': 168, 'Harvest': 14}
- team: Resource
- office: Harvester
**Observations**
- Harka Reed (Resource/Harvester): avg meaningful Watch marks 32.2, idle-ish rests 15.8, end Strain 1.1, downed/dead rate 0.0%.
- Top activities: {'Preserve': 168, 'Forage': 140, 'Harvest': 14}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: 09-zeetes

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 49.0
- avg_idle_watches: 0.0
- avg_end_strain: 3.9
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 308, 'Establish Camp': 10, 'Preserve': 14}
- team: Support
- office: Quartermaster
**Observations**
- Zeetes (Support/Quartermaster): avg meaningful Watch marks 49.0, idle-ish rests 0.0, end Strain 3.9, downed/dead rate 0.0%.
- Top activities: {'Transport': 308, 'Preserve': 14, 'Establish Camp': 10}.
- Extraction Tests centered on Quartermaster lead; failures forced visible cargo priority choices.
**Rules questions**
- Is vehicle/tool proficiency intended to replace Survival for Extraction Tests when no vehicle is present?
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 10-durn-stonevow

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 33.2
- avg_idle_watches: 15.8
- avg_end_strain: 1.1
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 308, 'Establish Camp': 10, 'Preserve': 14}
- team: Support
- office: Surgeon
**Observations**
- Durn Stonevow (Support/Surgeon): avg meaningful Watch marks 33.2, idle-ish rests 15.8, end Strain 1.1, downed/dead rate 0.0%.
- Top activities: {'Transport': 308, 'Preserve': 14, 'Establish Camp': 10}.
- Treat Watches competed with Transport during casualty extraction — real office conflict.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 11-ilse-harrow

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 33.2
- avg_idle_watches: 15.8
- avg_end_strain: 1.1
- downed_or_dead_pct: 0.0
- activity_counts: {'Transport': 308, 'Establish Camp': 10, 'Preserve': 14}
- team: Support
- office: Transport Chief
**Observations**
- Ilse Harrow (Support/Transport Chief): avg meaningful Watch marks 33.2, idle-ish rests 15.8, end Strain 1.1, downed/dead rate 0.0%.
- Top activities: {'Transport': 308, 'Preserve': 14, 'Establish Camp': 10}.
- Capacity-constrained Load made Transport assignment meaningful every extract Watch.
**Recommendations**
- Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.

### Agent: 12-toma-glass

**Metrics**
- iterations: 10
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- avg_elapsed_hours: 457.6
- avg_profit_gp: -1224.0
- avg_meaningful_watches: 32.2
- avg_idle_watches: 15.8
- avg_end_strain: 1.1
- downed_or_dead_pct: 0.0
- activity_counts: {'Forage': 140, 'Preserve': 168, 'Harvest': 14}
- team: Resource
- office: Preservation Lead
**Observations**
- Toma Glass (Resource/Preservation Lead): avg meaningful Watch marks 32.2, idle-ish rests 15.8, end Strain 1.1, downed/dead rate 0.0%.
- Top activities: {'Preserve': 168, 'Forage': 140, 'Harvest': 14}.
- Forage/Harvest/Preserve created the Supply vs cargo-capacity tension central to extraction.
**Exploits**
- On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
**Recommendations**
- Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.

### Agent: director

**Metrics**
- iterations: 10
- outcomes: {'abandoned': 5, 'haven': 5}
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- sealed_pct: 0.0
- avg_profit_gp: -1224.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 457.6
- avg_pressure_peak: 6.0
- avg_supply_end: 5.8
- avg_abandoned_cargo_gp: 6300.0
- avg_abandoned_load: 7.0
- avg_downed_or_dead: 0.7
- avg_extraction_test_fails: 1.1
- avg_complications: 28.6
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
**Observations**
- Across 10 seeded runs, outcomes={'abandoned': 5, 'haven': 5}; objective_met=50.0%; Haven=50.0%; sealed=0.0%.
- Average elapsed 457.6h; peak Pressure avg 6.0; extraction test failures avg 1.1.
- At-risk cargo was stated before every extraction response (sim enforces Director Quick Procedure §Resolving a cargo loss).
- Pack 01 combat findings unavailable (0 result JSON); assumed class checks use bible tier DC + listed lead mods only.
- Hidden lore boundary held: Research logged public symptoms only; no crystal-path / Old God confirmation in public facts.
**Rules questions**
- When evening Rest Watch workers Establish Camp, does their missed Rest grant Strain the same day or only after 24h without Rest (bible §5 vs camp example)?
- Does Attention-tagged cargo increase Pressure every active Watch or once while carried (bible §7 lists condition but not stacking cadence)?
- Extraction Test 'major route transition' interval is undefined numerically — sim used every 4 Progress as a Director ruling.
**Exploits**
- Abort-continue then immediately extract still paid the +1 Pressure once — easy to miss if Directors treat abort as soft advice.
**Recommendations**
- Publish a one-page Watch checklist card matching bible Quick Reference (assignments → 1/3 Supply → activities → Progress → Pressure → d6).
- Define Extraction Test spacing (per Length segment, per Gate, or per N Progress) with a worked table.
- Clarify Attention Pressure cadence and Rest-debt timing for the 3-worker evening camp pattern.

### Agent: quartermaster-auditor

**Metrics**
- iterations: 10
- outcomes: {'abandoned': 5, 'haven': 5}
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- sealed_pct: 0.0
- avg_profit_gp: -1224.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 457.6
- avg_pressure_peak: 6.0
- avg_supply_end: 5.8
- avg_abandoned_cargo_gp: 6300.0
- avg_abandoned_load: 7.0
- avg_downed_or_dead: 0.7
- avg_extraction_test_fails: 1.1
- avg_complications: 28.6
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- mismatch_notes: []
- avg_supply_shortfalls: 4.6
**Observations**
- Independent recalc: avg abandoned cargo 6300.0 gp / 7.0 Load; avg net after sponsor 0.0 gp.
- Daily Supply 12 for 12 Medium PCs matches bible §9; Watch consumption used 1/3 daily (bible worked example Watch One).
- Prep free-Load bookkeeping mismatches noted in 0 run annotations (scenario cargo overrides).
- Living cargo Load 6 + two Downed (12) on Capacity-constrained routes reliably forced Progress-1 and Pressure+1 (bible §6 Load>Capacity).
- Sponsor shares applied per bible table defaults (guild 20% / merchant 30% / noble 35% / sovereign 45%) by scenario.
**Rules questions**
- Are wages paid from net-after-sponsor or before sponsor share? Bible says net is after taxes before wages — wage timing vs profitability tests is ambiguous for 'profitable' definition.
- Does convoy Capacity equal route Capacity or a separate transport rating? Prep example uses convoy 100 vs route Capacity 80.
**Exploits**
- Forage can outpace Supply consumption on Tier I Mapped routes, making Supply tension weak unless complications tax Supply.
- Priority-1 bulk salvage is a 'dump valve' that makes Extraction Failures feel costless when high-priority lots are safe.
**Recommendations**
- Add a profitability definition to the expedition charter: profit after sponsor+wages+repairs vs gross extraction value.
- Cap Forage output by biome and require exposed risk, or Supply will rarely threaten Mapped Tier I runs.
- Require at least one mid-priority lot so Extraction Failures create real choice rather than discarding junk.

### Agent: rules-observer

**Metrics**
- iterations: 10
- outcomes: {'abandoned': 5, 'haven': 5}
- objective_met_pct: 50.0
- haven_arrival_pct: 50.0
- sealed_pct: 0.0
- avg_profit_gp: -1224.0
- avg_net_after_sponsor_gp: 0.0
- avg_elapsed_hours: 457.6
- avg_pressure_peak: 6.0
- avg_supply_end: 5.8
- avg_abandoned_cargo_gp: 6300.0
- avg_abandoned_load: 7.0
- avg_downed_or_dead: 0.7
- avg_extraction_test_fails: 1.1
- avg_complications: 28.6
- combat_team_size: 3
- combat_optimal_band: 4-6
- source_note: GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt (pending promotion); SOURCE_MANIFEST companions partially missing
- team_sizes: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}
- undersized_teams: ['Combat']
**Observations**
- All 12 roster agents received Watch assignments every active Watch; evening Rest used 3 workers / 9 resters (bible camp example).
- Team sizes this roster: {'Combat': 3, 'Reconnaissance': 2, 'Research': 2, 'Resource': 2, 'Support': 3}. Undersized vs bible optimal bands: ['Combat'].
- Parallel resolution: 5 team checks per active Watch is manageable; bottleneck is cargo priority + extraction response, not combat initiative.
- SOURCE_MANIFEST gaps: docs/mechanics/GAMEPLAY_LOOP_CANON.md missing; src/data/gameplay-loop.json missing; ExpeditionTracker.tsx missing. Used GAMEPLAY_LOOP_BIBLE_v1_EXTRACT.txt + haven.json + dungeon-mechanics.json.
- Decision bottlenecks recurring: ['Day cap without Haven arrival — expedition abandoned', 'Extraction response: abandoned at-risk cargo to save clock/Pressure', 'Extraction response: spent 8h rather than abandon cargo']
**Rules questions**
- Player Rulebook expedition periods (morning/afternoon/evening) vs Gameplay Loop Watch (8h, two active + one Rest) — confirm they are the same layer or dual systems.
- Combat optimal 4–6 vs this pack's 3 Combat PCs: is the Brass Lantern worked example intentionally below band?
**Exploits**
- Unknown routes with 0 Progress until recon succeeds can soft-lock Horn-adjacent starts if recon fails repeatedly (mitigated by assistants + high mods).
**Recommendations**
- Ship companion ExpeditionTracker matching bible Watch checklist; SOURCE_MANIFEST currently points at a missing component.
- Add explicit crosswalk: Rulebook 'periods' = Loop 'Watches' to prevent dual-system confusion during onboarding.
- Either expand Combat to 4+ in the sample company or revise optimal band examples to include 3-combat professional companies.

## Scenario: unknown

### Agent: unknown


## Repeated rules questions

- (18) Combat team size 3 is below bible optimal 4–6 — are Escort duties understaffed when two members are Downed?
- (12) How many Map Route successes are needed when Risk changes mid-expedition after compromise?
- (6) Is vehicle/tool proficiency intended to replace Survival for Extraction Tests when no vehicle is present?
- (6) When evening Rest Watch workers Establish Camp, does their missed Rest grant Strain the same day or only after 24h without Rest (bible §5 vs camp example)?
- (6) Does Attention-tagged cargo increase Pressure every active Watch or once while carried (bible §7 lists condition but not stacking cadence)?
- (6) Extraction Test 'major route transition' interval is undefined numerically — sim used every 4 Progress as a Director ruling.
- (6) Are wages paid from net-after-sponsor or before sponsor share? Bible says net is after taxes before wages — wage timing vs profitability tests is ambiguous for 'profitable' definition.
- (6) Does convoy Capacity equal route Capacity or a separate transport rating? Prep example uses convoy 100 vs route Capacity 80.
- (6) Player Rulebook expedition periods (morning/afternoon/evening) vs Gameplay Loop Watch (8h, two active + one Rest) — confirm they are the same layer or dual systems.
- (6) Combat optimal 4–6 vs this pack's 3 Combat PCs: is the Brass Lantern worked example intentionally below band?
- (2) What public Research outputs are legal at Tier IV without violating Director dual-layer canon?

## Repeated exploit findings

- (12) On low-Risk Mapped routes, Forage success can trivialize Supply abort conditions.
- (6) Abort-continue then immediately extract still paid the +1 Pressure once — easy to miss if Directors treat abort as soft advice.
- (6) Forage can outpace Supply consumption on Tier I Mapped routes, making Supply tension weak unless complications tax Supply.
- (6) Priority-1 bulk salvage is a 'dump valve' that makes Extraction Failures feel costless when high-priority lots are safe.
- (6) Unknown routes with 0 Progress until recon succeeds can soft-lock Horn-adjacent starts if recon fails repeatedly (mitigated by assistants + high mods).

## Repeated recommendations

- (18) Keep encounter objectives tied to cargo/casualties so Combat Watches stay expedition-relevant.
- (18) Support should pick one lead activity per Watch with explicit opportunity cost on the tracker UI.
- (12) Show Mapping upgrade progress as X/Risk on the route card.
- (12) Give Research a clear Watch product (tag, EC, buyer hint) so Identify never feels like flavor-only.
- (12) Tie Forage DC/output to biome Pressure so Resource Watches stay risky at Tier I.
- (6) Publish a one-page Watch checklist card matching bible Quick Reference (assignments → 1/3 Supply → activities → Progress → Pressure → d6).
- (6) Define Extraction Test spacing (per Length segment, per Gate, or per N Progress) with a worked table.
- (6) Clarify Attention Pressure cadence and Rest-debt timing for the 3-worker evening camp pattern.
- (6) Add a profitability definition to the expedition charter: profit after sponsor+wages+repairs vs gross extraction value.
- (6) Cap Forage output by biome and require exposed risk, or Supply will rarely threaten Mapped Tier I runs.
- (6) Require at least one mid-priority lot so Extraction Failures create real choice rather than discarding junk.
- (6) Ship companion ExpeditionTracker matching bible Watch checklist; SOURCE_MANIFEST currently points at a missing component.
- (6) Add explicit crosswalk: Rulebook 'periods' = Loop 'Watches' to prevent dual-system confusion during onboarding.
- (6) Either expand Combat to 4+ in the sample company or revise optimal band examples to include 3-combat professional companies.

