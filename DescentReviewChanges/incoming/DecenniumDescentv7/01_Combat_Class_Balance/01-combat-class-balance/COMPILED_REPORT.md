# Compiled Cursor Multi-Agent Playtest Report

## Executive summary (Pack 01 — Combat / Class Balance)

- **Scenarios completed:** 10/10 from `SCENARIO_MATRIX.csv`
- **Seeds:** 140 total (L1×20, L3×20, L5×15+15, L10×10+10, L15×10+10, L20×15, Retreat×15)
- **Result files:** 110 agent JSON under `results/`
- **Sources:** SOURCE_MANIFEST + pending-review Gameplay Loop Bible extract (`GAMEPLAY_LOOP_CANON.md` / JSON). Canon not rewritten mid-test.
- **Method:** Multi-agent roster role-play (Director, Rules Observer, Combat Metrics, Exploit Hunter, class players) via seeded table simulation `run_pack01_playtest.py`; Loop caps enforced as rulings.

### Top findings

1. **Summon/deployable/reflection layering is the top exploit surface** — illegal >2 independent actors in 100% of L10-DARK and L15-CONTROL seeds when Necromancer/Mirrorsage/Tinker pushed class text.
2. **Additional Action stacking is real** — CMB-L5-SUPPORT hit 100% Bard-tempo + Action Surge stack attempts; Loop “choose one” must be mirrored in class wording.
3. **Standard L1 is soft; cargo Hard is correctly punishing; L20 Catastrophic resolves too fast** — budget calibration needs playtest-led revision, not silent mid-test edits.
4. **Tenacity works** when applied (~4 triggers/seed on L15-CONTROL); readability suffers (avg lookups 3.85).
5. **Retreat procedure is playable** (~80% Escape success) without improvised TPK rules.

### Proposed patches

See `proposed_patches/PACK01_PROPOSED_PATCHES.md` (not applied).

---
Result files: **110**

## Scenario: CMB-L1-BASE

### Agent: cleric

**Metrics**
- class: Cleric
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 7.8
- avg_party_damage: 148.61
- avg_healing: 30.36
- avg_prevented: 27.2
- avg_control_applied: 7.15
- avg_lookups: 1.5
- avg_decision_steps: 1.0
- avg_rp_spent: 24.58
- class_dpr_model: 3.18
**Observations**
- Played 20 seeds as Cleric (Conviction) under scenario CMB-L1-BASE.
- Identity loop remained: Conviction; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=7.8.
- Decision steps avg=1.0; rule lookups avg=1.5.

### Agent: combat-metrics

**Metrics**
- iterations: 20
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 7.8
- avg_party_damage: 148.61
- avg_enemy_damage: 63.86
- avg_healing: 30.36
- avg_prevented: 27.2
- avg_control_applied: 7.15
- avg_full_turns_denied: 0.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.7
- avg_wounds: 0.35
- avg_rp_spent: 24.58
- avg_decision_steps: 1.0
- avg_lookups: 1.5
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 19.05
- effective_prevention_per_round: 3.49
- heal_to_damage_taken_ratio: 0.475
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 20
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 7.8
- avg_party_damage: 148.61
- avg_enemy_damage: 63.86
- avg_healing: 30.36
- avg_prevented: 27.2
- avg_control_applied: 7.15
- avg_full_turns_denied: 0.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.7
- avg_wounds: 0.35
- avg_rp_spent: 24.58
- avg_decision_steps: 1.0
- avg_lookups: 1.5
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 4
- stated_difficulty: Standard
- modeled_budget_tp: 90.0
**Observations**
- Ran 2 equal-level foes at listed difficulty Standard for objective: Open chamber; kill or rout.
- Budget model (4PC base adjusted): ~90 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=7.8, KO/seed=0.7.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 0
- avg_full_turns_denied: 0.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 20 seeds.
- Illegal summon pressure rate=0.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Exploits**
- No demonstrated infinite exploit under enforced Loop caps this scenario.
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: mage

**Metrics**
- class: Mage
- role: burst
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 7.8
- avg_party_damage: 148.61
- avg_healing: 30.36
- avg_prevented: 27.2
- avg_control_applied: 7.15
- avg_lookups: 1.5
- avg_decision_steps: 1.0
- avg_rp_spent: 24.58
- class_dpr_model: 6.14
**Observations**
- Played 20 seeds as Mage (Nuke Chains) under scenario CMB-L1-BASE.
- Identity loop remained: Nuke Chains; role=burst.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=7.8.
- Decision steps avg=1.0; rule lookups avg=1.5.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 1.0
- avg_lookups: 1.5
- turns_over_three_lookups_estimate: 0.0
- ambiguity_flags: 0
**Observations**
- Average decision steps=1.0 (flag if >3).
- Average source lookups=1.5 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- No severe ambiguity this scenario beyond normal class feature lookups.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: soldier

**Metrics**
- class: Soldier
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 7.8
- avg_party_damage: 148.61
- avg_healing: 30.36
- avg_prevented: 27.2
- avg_control_applied: 7.15
- avg_lookups: 1.5
- avg_decision_steps: 1.0
- avg_rp_spent: 24.58
- class_dpr_model: 4.55
**Observations**
- Played 20 seeds as Soldier (Palisade/Overwatch) under scenario CMB-L1-BASE.
- Identity loop remained: Palisade/Overwatch; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=7.8.
- Decision steps avg=1.0; rule lookups avg=1.5.
- Sample actions: Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention

### Agent: thief

**Metrics**
- class: Thief
- role: skirmish
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 7.8
- avg_party_damage: 148.61
- avg_healing: 30.36
- avg_prevented: 27.2
- avg_control_applied: 7.15
- avg_lookups: 1.5
- avg_decision_steps: 1.0
- avg_rp_spent: 24.58
- class_dpr_model: 5.23
**Observations**
- Played 20 seeds as Thief (Sneak/Poison) under scenario CMB-L1-BASE.
- Identity loop remained: Sneak/Poison; role=skirmish.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=7.8.
- Decision steps avg=1.0; rule lookups avg=1.5.

## Scenario: CMB-L10-BOSS

### Agent: bard

**Metrics**
- class: Bard
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 4.0
- avg_party_damage: 573.44
- avg_healing: 65.1
- avg_prevented: 80.9
- avg_control_applied: 7.1
- avg_lookups: 2.22
- avg_decision_steps: 1.83
- avg_rp_spent: 21.6
- class_dpr_model: 8.34
**Observations**
- Played 10 seeds as Bard (Crescendo) under scenario CMB-L10-BOSS.
- Identity loop remained: Crescendo; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=4.0.
- Decision steps avg=1.83; rule lookups avg=2.22.
- Sample actions: Crescendo consume for ally tempo; Crescendo consume for ally tempo; Crescendo consume for ally tempo; Crescendo consume for ally tempo; Crescendo consume for ally tempo
- Crescendo/tempo grants were offered; Loop additional-Action cap enforced when stacked with Action Surge.
**Rules questions**
- Does Crescendo-enhanced ally 'extra attack' count as the one additional full Action?
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
**Recommendations**
- Clarify Bard tempo grants as Bonus Action riders or as the single additional Action slot.

### Agent: cleric

**Metrics**
- class: Cleric
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 4.0
- avg_party_damage: 573.44
- avg_healing: 65.1
- avg_prevented: 80.9
- avg_control_applied: 7.1
- avg_lookups: 2.22
- avg_decision_steps: 1.83
- avg_rp_spent: 21.6
- class_dpr_model: 8.98
**Observations**
- Played 10 seeds as Cleric (Conviction) under scenario CMB-L10-BOSS.
- Identity loop remained: Conviction; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=4.0.
- Decision steps avg=1.83; rule lookups avg=2.22.
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.

### Agent: combat-metrics

**Metrics**
- iterations: 10
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 4.0
- avg_party_damage: 573.44
- avg_enemy_damage: 118.82
- avg_healing: 65.1
- avg_prevented: 80.9
- avg_control_applied: 7.1
- avg_full_turns_denied: 0.0
- max_summons_peak: 2
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.2
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 21.6
- avg_decision_steps: 1.83
- avg_lookups: 2.22
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 143.36
- effective_prevention_per_round: 20.23
- heal_to_damage_taken_ratio: 0.548
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 10
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 4.0
- avg_party_damage: 573.44
- avg_enemy_damage: 118.82
- avg_healing: 65.1
- avg_prevented: 80.9
- avg_control_applied: 7.1
- avg_full_turns_denied: 0.0
- max_summons_peak: 2
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.2
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 21.6
- avg_decision_steps: 1.83
- avg_lookups: 2.22
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 6
- stated_difficulty: Boss
- modeled_budget_tp: 251.99999999999997
**Observations**
- Ran two-phase boss at listed difficulty Boss for objective: Objective, telegraphs, Tenacity, retreat state.
- Budget model (4PC base adjusted): ~252 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=4.0, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: druid

**Metrics**
- class: Druid
- role: flexible
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 4.0
- avg_party_damage: 573.44
- avg_healing: 65.1
- avg_prevented: 80.9
- avg_control_applied: 7.1
- avg_lookups: 2.22
- avg_decision_steps: 1.83
- avg_rp_spent: 21.6
- class_dpr_model: 12.18
**Observations**
- Played 10 seeds as Druid (Shapeshift) under scenario CMB-L10-BOSS.
- Identity loop remained: Shapeshift; role=flexible.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=4.0.
- Decision steps avg=1.83; rule lookups avg=2.22.
- Peak summons desired observed up to 2; illegal_rate=0.0.
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.2
- deadlock_seeds: 0
- max_summons_peak: 2
- avg_full_turns_denied: 0.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 10 seeds.
- Illegal summon pressure rate=0.0; extra-action stack attempt rate=0.2.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: paladin

**Metrics**
- class: Paladin
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 4.0
- avg_party_damage: 573.44
- avg_healing: 65.1
- avg_prevented: 80.9
- avg_control_applied: 7.1
- avg_lookups: 2.22
- avg_decision_steps: 1.83
- avg_rp_spent: 21.6
- class_dpr_model: 13.47
**Observations**
- Played 10 seeds as Paladin (Oath/Smite) under scenario CMB-L10-BOSS.
- Identity loop remained: Oath/Smite; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=4.0.
- Decision steps avg=1.83; rule lookups avg=2.22.
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.

### Agent: ranger

**Metrics**
- class: Ranger
- role: skirmish
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 4.0
- avg_party_damage: 573.44
- avg_healing: 65.1
- avg_prevented: 80.9
- avg_control_applied: 7.1
- avg_lookups: 2.22
- avg_decision_steps: 1.83
- avg_rp_spent: 21.6
- class_dpr_model: 14.11
**Observations**
- Played 10 seeds as Ranger (Track Target) under scenario CMB-L10-BOSS.
- Identity loop remained: Track Target; role=skirmish.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=4.0.
- Decision steps avg=1.83; rule lookups avg=2.22.
- Peak summons desired observed up to 2; illegal_rate=0.0.
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 1.83
- avg_lookups: 2.22
- turns_over_three_lookups_estimate: 0.0
- ambiguity_flags: 0
**Observations**
- Average decision steps=1.83 (flag if >3).
- Average source lookups=2.22 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- No severe ambiguity this scenario beyond normal class feature lookups.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: soldier

**Metrics**
- class: Soldier
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 4.0
- avg_party_damage: 573.44
- avg_healing: 65.1
- avg_prevented: 80.9
- avg_control_applied: 7.1
- avg_lookups: 2.22
- avg_decision_steps: 1.83
- avg_rp_spent: 21.6
- class_dpr_model: 12.83
**Observations**
- Played 10 seeds as Soldier (Palisade/Overwatch) under scenario CMB-L10-BOSS.
- Identity loop remained: Palisade/Overwatch; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=4.0.
- Decision steps avg=1.83; rule lookups avg=2.22.
- Sample actions: Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.

## Scenario: CMB-L10-DARK

### Agent: combat-metrics

**Metrics**
- iterations: 10
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.7
- avg_party_damage: 550.33
- avg_enemy_damage: 101.49
- avg_healing: 12.88
- avg_prevented: 25.83
- avg_control_applied: 9.6
- avg_full_turns_denied: 0.0
- max_summons_peak: 4
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 37.8
- avg_decision_steps: 2.6
- avg_lookups: 2.94
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 148.74
- effective_prevention_per_round: 6.98
- heal_to_damage_taken_ratio: 0.127
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 10
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.7
- avg_party_damage: 550.33
- avg_enemy_damage: 101.49
- avg_healing: 12.88
- avg_prevented: 25.83
- avg_control_applied: 9.6
- avg_full_turns_denied: 0.0
- max_summons_peak: 4
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 37.8
- avg_decision_steps: 2.6
- avg_lookups: 2.94
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 5
- stated_difficulty: Severe
- modeled_budget_tp: 216.0
**Observations**
- Ran boss plus adds at listed difficulty Severe for objective: Stress summons, duplicates, Traumatic Casting, control.
- Budget model (4PC base adjusted): ~216 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=3.7, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Rules questions**
- Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 4
- avg_full_turns_denied: 0.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 10 seeds.
- Illegal summon pressure rate=1.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Rules questions**
- Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: mage

**Metrics**
- class: Mage
- role: burst
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.7
- avg_party_damage: 550.33
- avg_healing: 12.88
- avg_prevented: 25.83
- avg_control_applied: 9.6
- avg_lookups: 2.94
- avg_decision_steps: 2.6
- avg_rp_spent: 37.8
- class_dpr_model: 17.31
**Observations**
- Played 10 seeds as Mage (Nuke Chains) under scenario CMB-L10-DARK.
- Identity loop remained: Nuke Chains; role=burst.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.7.
- Decision steps avg=2.6; rule lookups avg=2.94.
- Sample actions: Traumatic/Dark Resonance surge; Traumatic/Dark Resonance surge; Traumatic/Dark Resonance surge; Traumatic/Dark Resonance surge; Traumatic/Dark Resonance surge
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Traumatic Casting self-harm and Dissonance bypass: when does it violate anti-loop doctrine?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: mirrorsage

**Metrics**
- class: Mirrorsage
- role: control
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.7
- avg_party_damage: 550.33
- avg_healing: 12.88
- avg_prevented: 25.83
- avg_control_applied: 9.6
- avg_lookups: 2.94
- avg_decision_steps: 2.6
- avg_rp_spent: 37.8
- class_dpr_model: 11.54
**Observations**
- Played 10 seeds as Mirrorsage (Echo/Mirrorbind) under scenario CMB-L10-DARK.
- Identity loop remained: Echo/Mirrorbind; role=control.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.7.
- Decision steps avg=2.6; rule lookups avg=2.94.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Do Reflective Companions count against the 2-summon cap and against the 1 copy release/round draft ceiling?
- Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Promote draft ceiling caps for Mirrorsage into Loop-aligned explicit rules.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 2.6
- avg_lookups: 2.94
- turns_over_three_lookups_estimate: 0.0
- ambiguity_flags: 5
**Observations**
- Average decision steps=2.6 (flag if >3).
- Average source lookups=2.94 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: shaman

**Metrics**
- class: Shaman
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.7
- avg_party_damage: 550.33
- avg_healing: 12.88
- avg_prevented: 25.83
- avg_control_applied: 9.6
- avg_lookups: 2.94
- avg_decision_steps: 2.6
- avg_rp_spent: 37.8
- class_dpr_model: 9.62
**Observations**
- Played 10 seeds as Shaman (Totems) under scenario CMB-L10-DARK.
- Identity loop remained: Totems; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.7.
- Decision steps avg=2.6; rule lookups avg=2.94.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: tinker

**Metrics**
- class: Tinker
- role: control
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.7
- avg_party_damage: 550.33
- avg_healing: 12.88
- avg_prevented: 25.83
- avg_control_applied: 9.6
- avg_lookups: 2.94
- avg_decision_steps: 2.6
- avg_rp_spent: 37.8
- class_dpr_model: 10.9
**Observations**
- Played 10 seeds as Tinker (Deployables) under scenario CMB-L10-DARK.
- Identity loop remained: Deployables; role=control.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.7.
- Decision steps avg=2.6; rule lookups avg=2.94.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Are Anacite drones and gadgets summons, deployables, or both for the command cap?
- Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Define deployables as non-summon structures unless they take independent combat turns.

### Agent: wizard

**Metrics**
- class: Wizard
- role: burst
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.7
- avg_party_damage: 550.33
- avg_healing: 12.88
- avg_prevented: 25.83
- avg_control_applied: 9.6
- avg_lookups: 2.94
- avg_decision_steps: 2.6
- avg_rp_spent: 37.8
- class_dpr_model: 15.39
**Observations**
- Played 10 seeds as Wizard (Spell Matrix/Necromancer) under scenario CMB-L10-DARK.
- Identity loop remained: Spell Matrix/Necromancer; role=burst.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.7.
- Decision steps avg=2.6; rule lookups avg=2.94.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- How do permanent undead from Core Systems interact with the 2-summon command cap?
- Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Require Necromancer excess undead to use swarm/unit blocks; cite Loop summon rule in class path text.

## Scenario: CMB-L15-ATTRITION

### Agent: cleric

**Metrics**
- class: Cleric
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 10.1
- avg_party_damage: 815.92
- avg_healing: 106.78
- avg_prevented: 53.22
- avg_control_applied: 7.4
- avg_lookups: 3.08
- avg_decision_steps: 3.0
- avg_rp_spent: 37.1
- class_dpr_model: 13.89
**Observations**
- Played 10 seeds as Cleric (Conviction) under scenario CMB-L15-ATTRITION.
- Identity loop remained: Conviction; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=10.1.
- Decision steps avg=3.0; rule lookups avg=3.08.
- Turn frequently required >2 cross-references — readability stress.

### Agent: combat-metrics

**Metrics**
- iterations: 10
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 10.1
- avg_party_damage: 815.92
- avg_enemy_damage: 166.09
- avg_healing: 106.78
- avg_prevented: 53.22
- avg_control_applied: 7.4
- avg_full_turns_denied: 0.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 37.1
- avg_decision_steps: 3.0
- avg_lookups: 3.08
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 80.78
- effective_prevention_per_round: 5.27
- heal_to_damage_taken_ratio: 0.643
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: crimson-agent

**Metrics**
- class: Crimson Agent
- role: skirmish
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 10.1
- avg_party_damage: 815.92
- avg_healing: 106.78
- avg_prevented: 53.22
- avg_control_applied: 7.4
- avg_lookups: 3.08
- avg_decision_steps: 3.0
- avg_rp_spent: 37.1
- class_dpr_model: 23.81
**Observations**
- Played 10 seeds as Crimson Agent (Blood Mark) under scenario CMB-L15-ATTRITION.
- Identity loop remained: Blood Mark; role=skirmish.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=10.1.
- Decision steps avg=3.0; rule lookups avg=3.08.
- Turn frequently required >2 cross-references — readability stress.

### Agent: director

**Metrics**
- iterations: 10
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 10.1
- avg_party_damage: 815.92
- avg_enemy_damage: 166.09
- avg_healing: 106.78
- avg_prevented: 53.22
- avg_control_applied: 7.4
- avg_full_turns_denied: 0.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 37.1
- avg_decision_steps: 3.0
- avg_lookups: 3.08
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 4
- stated_difficulty: Hard
- modeled_budget_tp: 130.0
**Observations**
- Ran three sequential encounters at listed difficulty Hard for objective: No Long Rest; track resource curve.
- Budget model (4PC base adjusted): ~130 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=10.1, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: dragoon

**Metrics**
- class: Dragoon
- role: mobile
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 10.1
- avg_party_damage: 815.92
- avg_healing: 106.78
- avg_prevented: 53.22
- avg_control_applied: 7.4
- avg_lookups: 3.08
- avg_decision_steps: 3.0
- avg_rp_spent: 37.1
- class_dpr_model: 22.82
**Observations**
- Played 10 seeds as Dragoon (Momentum) under scenario CMB-L15-ATTRITION.
- Identity loop remained: Momentum; role=mobile.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=10.1.
- Decision steps avg=3.0; rule lookups avg=3.08.
- Turn frequently required >2 cross-references — readability stress.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 0
- avg_full_turns_denied: 0.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 10 seeds.
- Illegal summon pressure rate=0.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Exploits**
- No demonstrated infinite exploit under enforced Loop caps this scenario.
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 3.0
- avg_lookups: 3.08
- turns_over_three_lookups_estimate: 3.23
- ambiguity_flags: 0
**Observations**
- Average decision steps=3.0 (flag if >3).
- Average source lookups=3.08 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- No severe ambiguity this scenario beyond normal class feature lookups.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: warrior

**Metrics**
- class: Warrior
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 10.1
- avg_party_damage: 815.92
- avg_healing: 106.78
- avg_prevented: 53.22
- avg_control_applied: 7.4
- avg_lookups: 3.08
- avg_decision_steps: 3.0
- avg_rp_spent: 37.1
- class_dpr_model: 24.81
**Observations**
- Played 10 seeds as Warrior (Mutations) under scenario CMB-L15-ATTRITION.
- Identity loop remained: Mutations; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=10.1.
- Decision steps avg=3.0; rule lookups avg=3.08.
- Turn frequently required >2 cross-references — readability stress.

## Scenario: CMB-L15-CONTROL

### Agent: combat-metrics

**Metrics**
- iterations: 10
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 460.99
- avg_enemy_damage: 70.46
- avg_healing: 12.63
- avg_prevented: 14.86
- avg_control_applied: 7.4
- avg_full_turns_denied: 0.4
- max_summons_peak: 4
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 4.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 20.5
- avg_decision_steps: 3.0
- avg_lookups: 3.85
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 153.66
- effective_prevention_per_round: 4.95
- heal_to_damage_taken_ratio: 0.179
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 10
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 460.99
- avg_enemy_damage: 70.46
- avg_healing: 12.63
- avg_prevented: 14.86
- avg_control_applied: 7.4
- avg_full_turns_denied: 0.4
- max_summons_peak: 4
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 4.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 20.5
- avg_decision_steps: 3.0
- avg_lookups: 3.85
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 4
- stated_difficulty: Severe
- modeled_budget_tp: 180.0
**Observations**
- Ran elite enemies at listed difficulty Severe for objective: Attempt full-turn denial chains.
- Budget model (4PC base adjusted): ~180 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=3.0, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 4
- avg_full_turns_denied: 0.4
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 10 seeds.
- Illegal summon pressure rate=1.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: mirrorsage

**Metrics**
- class: Mirrorsage
- role: control
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 460.99
- avg_healing: 12.63
- avg_prevented: 14.86
- avg_control_applied: 7.4
- avg_lookups: 3.85
- avg_decision_steps: 3.0
- avg_rp_spent: 20.5
- class_dpr_model: 17.86
**Observations**
- Played 10 seeds as Mirrorsage (Echo/Mirrorbind) under scenario CMB-L15-CONTROL.
- Identity loop remained: Echo/Mirrorbind; role=control.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=3.0; rule lookups avg=3.85.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Do Reflective Companions count against the 2-summon cap and against the 1 copy release/round draft ceiling?
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Ensure Tenacity + same-source denial limit are cross-linked in Director quick reference.
- Promote draft ceiling caps for Mirrorsage into Loop-aligned explicit rules.

### Agent: monk

**Metrics**
- class: Monk
- role: mobile
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 460.99
- avg_healing: 12.63
- avg_prevented: 14.86
- avg_control_applied: 7.4
- avg_lookups: 3.85
- avg_decision_steps: 3.0
- avg_rp_spent: 20.5
- class_dpr_model: 19.85
**Observations**
- Played 10 seeds as Monk (Ki/Stance) under scenario CMB-L15-CONTROL.
- Identity loop remained: Ki/Stance; role=mobile.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=3.0; rule lookups avg=3.85.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Ensure Tenacity + same-source denial limit are cross-linked in Director quick reference.

### Agent: oracle

**Metrics**
- class: Oracle
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 460.99
- avg_healing: 12.63
- avg_prevented: 14.86
- avg_control_applied: 7.4
- avg_lookups: 3.85
- avg_decision_steps: 3.0
- avg_rp_spent: 20.5
- class_dpr_model: 11.91
**Observations**
- Played 10 seeds as Oracle (Revelations) under scenario CMB-L15-CONTROL.
- Identity loop remained: Revelations; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=3.0; rule lookups avg=3.85.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Oracle draft '1 hard deny / target / encounter' vs Loop same-source denial escalation — which wins?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Ensure Tenacity + same-source denial limit are cross-linked in Director quick reference.
- Keep both: Loop general rule + Oracle-specific 1 hard deny/target as tighter class ceiling.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 3.0
- avg_lookups: 3.85
- turns_over_three_lookups_estimate: 10.2
- ambiguity_flags: 3
**Observations**
- Average decision steps=3.0 (flag if >3).
- Average source lookups=3.85 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: wizard

**Metrics**
- class: Wizard
- role: burst
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 460.99
- avg_healing: 12.63
- avg_prevented: 14.86
- avg_control_applied: 7.4
- avg_lookups: 3.85
- avg_decision_steps: 3.0
- avg_rp_spent: 20.5
- class_dpr_model: 23.81
**Observations**
- Played 10 seeds as Wizard (Spell Matrix/Necromancer) under scenario CMB-L15-CONTROL.
- Identity loop remained: Spell Matrix/Necromancer; role=burst.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=3.0; rule lookups avg=3.85.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- How do permanent undead from Core Systems interact with the 2-summon command cap?
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Ensure Tenacity + same-source denial limit are cross-linked in Director quick reference.
- Require Necromancer excess undead to use swarm/unit blocks; cite Loop summon rule in class path text.

## Scenario: CMB-L20-CEILING

### Agent: combat-metrics

**Metrics**
- iterations: 15
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.8
- avg_party_damage: 851.29
- avg_enemy_damage: 131.3
- avg_healing: 35.09
- avg_prevented: 76.15
- avg_control_applied: 6.47
- avg_full_turns_denied: 0.0
- max_summons_peak: 4
- summons_illegal_rate: 0.667
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.8
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 23.76
- avg_decision_steps: 2.89
- avg_lookups: 3.25
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 304.03
- effective_prevention_per_round: 27.2
- heal_to_damage_taken_ratio: 0.267
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 15
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.8
- avg_party_damage: 851.29
- avg_enemy_damage: 131.3
- avg_healing: 35.09
- avg_prevented: 76.15
- avg_control_applied: 6.47
- avg_full_turns_denied: 0.0
- max_summons_peak: 4
- summons_illegal_rate: 0.667
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.8
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 23.76
- avg_decision_steps: 2.89
- avg_lookups: 3.25
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 17
- stated_difficulty: Catastrophic
- modeled_budget_tp: 864.0
**Observations**
- Ran high-level boss suites at listed difficulty Catastrophic for objective: Find ceilings, loops, and dead options.
- Budget model (4PC base adjusted): ~864 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=2.8, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.667
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 4
- avg_full_turns_denied: 0.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 15 seeds.
- Illegal summon pressure rate=0.667; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: cleric

**Metrics**
- class: Cleric
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 806.34
- avg_healing: 47.62
- avg_prevented: 97.0
- avg_control_applied: 5.6
- avg_lookups: 2.87
- avg_decision_steps: 2.83
- avg_rp_spent: 21.6
- class_dpr_model: 19.56
**Observations**
- Played 5 seeds as Cleric (Conviction) under scenario CMB-L20-CEILING.
- Identity loop remained: Conviction; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=2.87.
- Turn frequently required >2 cross-references — readability stress.

### Agent: combat-metrics

**Metrics**
- iterations: 5
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 806.34
- avg_enemy_damage: 138.28
- avg_healing: 47.62
- avg_prevented: 97.0
- avg_control_applied: 5.6
- avg_full_turns_denied: 0.0
- max_summons_peak: 2
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 21.6
- avg_decision_steps: 2.83
- avg_lookups: 2.87
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 268.78
- effective_prevention_per_round: 32.33
- heal_to_damage_taken_ratio: 0.344
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
- party: ['Soldier', 'Cleric', 'Thief', 'Mage', 'Paladin', 'Ranger']
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 5
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 806.34
- avg_enemy_damage: 138.28
- avg_healing: 47.62
- avg_prevented: 97.0
- avg_control_applied: 5.6
- avg_full_turns_denied: 0.0
- max_summons_peak: 2
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 21.6
- avg_decision_steps: 2.83
- avg_lookups: 2.87
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 6
- stated_difficulty: Catastrophic
- modeled_budget_tp: 336.0
- party: ['Soldier', 'Cleric', 'Thief', 'Mage', 'Paladin', 'Ranger']
**Observations**
- Ran high-level boss suites at listed difficulty Catastrophic for objective: Find ceilings, loops, and dead options.
- Budget model (4PC base adjusted): ~336 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=3.0, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 2
- avg_full_turns_denied: 0.0
- party: ['Soldier', 'Cleric', 'Thief', 'Mage', 'Paladin', 'Ranger']
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 5 seeds.
- Illegal summon pressure rate=0.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Exploits**
- No demonstrated infinite exploit under enforced Loop caps this scenario.
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: mage

**Metrics**
- class: Mage
- role: burst
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 806.34
- avg_healing: 47.62
- avg_prevented: 97.0
- avg_control_applied: 5.6
- avg_lookups: 2.87
- avg_decision_steps: 2.83
- avg_rp_spent: 21.6
- class_dpr_model: 37.73
**Observations**
- Played 5 seeds as Mage (Nuke Chains) under scenario CMB-L20-CEILING.
- Identity loop remained: Nuke Chains; role=burst.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=2.87.
- Turn frequently required >2 cross-references — readability stress.

### Agent: paladin

**Metrics**
- class: Paladin
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 806.34
- avg_healing: 47.62
- avg_prevented: 97.0
- avg_control_applied: 5.6
- avg_lookups: 2.87
- avg_decision_steps: 2.83
- avg_rp_spent: 21.6
- class_dpr_model: 29.34
**Observations**
- Played 5 seeds as Paladin (Oath/Smite) under scenario CMB-L20-CEILING.
- Identity loop remained: Oath/Smite; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=2.87.
- Turn frequently required >2 cross-references — readability stress.

### Agent: ranger

**Metrics**
- class: Ranger
- role: skirmish
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 806.34
- avg_healing: 47.62
- avg_prevented: 97.0
- avg_control_applied: 5.6
- avg_lookups: 2.87
- avg_decision_steps: 2.83
- avg_rp_spent: 21.6
- class_dpr_model: 30.74
**Observations**
- Played 5 seeds as Ranger (Track Target) under scenario CMB-L20-CEILING.
- Identity loop remained: Track Target; role=skirmish.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=2.87.
- Peak summons desired observed up to 2; illegal_rate=0.0.
- Turn frequently required >2 cross-references — readability stress.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 2.83
- avg_lookups: 2.87
- turns_over_three_lookups_estimate: 0.0
- ambiguity_flags: 0
- party: ['Soldier', 'Cleric', 'Thief', 'Mage', 'Paladin', 'Ranger']
**Observations**
- Average decision steps=2.83 (flag if >3).
- Average source lookups=2.87 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- No severe ambiguity this scenario beyond normal class feature lookups.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: soldier

**Metrics**
- class: Soldier
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 806.34
- avg_healing: 47.62
- avg_prevented: 97.0
- avg_control_applied: 5.6
- avg_lookups: 2.87
- avg_decision_steps: 2.83
- avg_rp_spent: 21.6
- class_dpr_model: 27.95
**Observations**
- Played 5 seeds as Soldier (Palisade/Overwatch) under scenario CMB-L20-CEILING.
- Identity loop remained: Palisade/Overwatch; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=2.87.
- Sample actions: Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention
- Turn frequently required >2 cross-references — readability stress.

### Agent: thief

**Metrics**
- class: Thief
- role: skirmish
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 806.34
- avg_healing: 47.62
- avg_prevented: 97.0
- avg_control_applied: 5.6
- avg_lookups: 2.87
- avg_decision_steps: 2.83
- avg_rp_spent: 21.6
- class_dpr_model: 32.14
**Observations**
- Played 5 seeds as Thief (Sneak/Poison) under scenario CMB-L20-CEILING.
- Identity loop remained: Sneak/Poison; role=skirmish.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=2.87.
- Turn frequently required >2 cross-references — readability stress.

### Agent: bard

**Metrics**
- class: Bard
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.4
- avg_party_damage: 851.84
- avg_healing: 17.56
- avg_prevented: 50.06
- avg_control_applied: 4.2
- avg_lookups: 3.32
- avg_decision_steps: 3.0
- avg_rp_spent: 17.28
- class_dpr_model: 18.16
**Observations**
- Played 5 seeds as Bard (Crescendo) under scenario CMB-L20-CEILING.
- Identity loop remained: Crescendo; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=2.4.
- Decision steps avg=3.0; rule lookups avg=3.32.
- Sample actions: Crescendo consume for ally tempo; Crescendo consume for ally tempo; Crescendo consume for ally tempo; Crescendo consume for ally tempo
- Crescendo/tempo grants were offered; Loop additional-Action cap enforced when stacked with Action Surge.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Does Crescendo-enhanced ally 'extra attack' count as the one additional full Action?
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Clarify Bard tempo grants as Bonus Action riders or as the single additional Action slot.

### Agent: combat-metrics

**Metrics**
- iterations: 5
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.4
- avg_party_damage: 851.84
- avg_enemy_damage: 114.82
- avg_healing: 17.56
- avg_prevented: 50.06
- avg_control_applied: 4.2
- avg_full_turns_denied: 0.0
- max_summons_peak: 3
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 17.28
- avg_decision_steps: 3.0
- avg_lookups: 3.32
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 354.93
- effective_prevention_per_round: 20.86
- heal_to_damage_taken_ratio: 0.153
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
- party: ['Tinker', 'Warrior', 'Dragoon', 'Monk', 'Crimson Agent', 'Bard']
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: crimson-agent

**Metrics**
- class: Crimson Agent
- role: skirmish
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.4
- avg_party_damage: 851.84
- avg_healing: 17.56
- avg_prevented: 50.06
- avg_control_applied: 4.2
- avg_lookups: 3.32
- avg_decision_steps: 3.0
- avg_rp_spent: 17.28
- class_dpr_model: 33.53
**Observations**
- Played 5 seeds as Crimson Agent (Blood Mark) under scenario CMB-L20-CEILING.
- Identity loop remained: Blood Mark; role=skirmish.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=2.4.
- Decision steps avg=3.0; rule lookups avg=3.32.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: director

**Metrics**
- iterations: 5
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.4
- avg_party_damage: 851.84
- avg_enemy_damage: 114.82
- avg_healing: 17.56
- avg_prevented: 50.06
- avg_control_applied: 4.2
- avg_full_turns_denied: 0.0
- max_summons_peak: 3
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 17.28
- avg_decision_steps: 3.0
- avg_lookups: 3.32
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 6
- stated_difficulty: Catastrophic
- modeled_budget_tp: 336.0
- party: ['Tinker', 'Warrior', 'Dragoon', 'Monk', 'Crimson Agent', 'Bard']
**Observations**
- Ran high-level boss suites at listed difficulty Catastrophic for objective: Find ceilings, loops, and dead options.
- Budget model (4PC base adjusted): ~336 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=2.4, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Rules questions**
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: dragoon

**Metrics**
- class: Dragoon
- role: mobile
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.4
- avg_party_damage: 851.84
- avg_healing: 17.56
- avg_prevented: 50.06
- avg_control_applied: 4.2
- avg_lookups: 3.32
- avg_decision_steps: 3.0
- avg_rp_spent: 17.28
- class_dpr_model: 32.14
**Observations**
- Played 5 seeds as Dragoon (Momentum) under scenario CMB-L20-CEILING.
- Identity loop remained: Momentum; role=mobile.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=2.4.
- Decision steps avg=3.0; rule lookups avg=3.32.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 3
- avg_full_turns_denied: 0.0
- party: ['Tinker', 'Warrior', 'Dragoon', 'Monk', 'Crimson Agent', 'Bard']
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 5 seeds.
- Illegal summon pressure rate=1.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Rules questions**
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: monk

**Metrics**
- class: Monk
- role: mobile
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.4
- avg_party_damage: 851.84
- avg_healing: 17.56
- avg_prevented: 50.06
- avg_control_applied: 4.2
- avg_lookups: 3.32
- avg_decision_steps: 3.0
- avg_rp_spent: 17.28
- class_dpr_model: 27.95
**Observations**
- Played 5 seeds as Monk (Ki/Stance) under scenario CMB-L20-CEILING.
- Identity loop remained: Ki/Stance; role=mobile.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=2.4.
- Decision steps avg=3.0; rule lookups avg=3.32.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 3.0
- avg_lookups: 3.32
- turns_over_three_lookups_estimate: 4.61
- ambiguity_flags: 1
- party: ['Tinker', 'Warrior', 'Dragoon', 'Monk', 'Crimson Agent', 'Bard']
**Observations**
- Average decision steps=3.0 (flag if >3).
- Average source lookups=3.32 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: tinker

**Metrics**
- class: Tinker
- role: control
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.4
- avg_party_damage: 851.84
- avg_healing: 17.56
- avg_prevented: 50.06
- avg_control_applied: 4.2
- avg_lookups: 3.32
- avg_decision_steps: 3.0
- avg_rp_spent: 17.28
- class_dpr_model: 23.75
**Observations**
- Played 5 seeds as Tinker (Deployables) under scenario CMB-L20-CEILING.
- Identity loop remained: Deployables; role=control.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=2.4.
- Decision steps avg=3.0; rule lookups avg=3.32.
- Peak summons desired observed up to 3; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Are Anacite drones and gadgets summons, deployables, or both for the command cap?
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Define deployables as non-summon structures unless they take independent combat turns.

### Agent: warrior

**Metrics**
- class: Warrior
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 2.4
- avg_party_damage: 851.84
- avg_healing: 17.56
- avg_prevented: 50.06
- avg_control_applied: 4.2
- avg_lookups: 3.32
- avg_decision_steps: 3.0
- avg_rp_spent: 17.28
- class_dpr_model: 34.93
**Observations**
- Played 5 seeds as Warrior (Mutations) under scenario CMB-L20-CEILING.
- Identity loop remained: Mutations; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=2.4.
- Decision steps avg=3.0; rule lookups avg=3.32.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
**Exploits**
- Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: combat-metrics

**Metrics**
- iterations: 5
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 895.7
- avg_enemy_damage: 140.8
- avg_healing: 40.1
- avg_prevented: 81.4
- avg_control_applied: 9.6
- avg_full_turns_denied: 0.0
- max_summons_peak: 4
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 2.4
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 32.4
- avg_decision_steps: 2.83
- avg_lookups: 3.55
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 298.57
- effective_prevention_per_round: 27.13
- heal_to_damage_taken_ratio: 0.285
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
- party: ['Oracle', 'Mirrorsage', 'Shaman', 'Wizard', 'Druid', 'Soldier']
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 5
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 895.7
- avg_enemy_damage: 140.8
- avg_healing: 40.1
- avg_prevented: 81.4
- avg_control_applied: 9.6
- avg_full_turns_denied: 0.0
- max_summons_peak: 4
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 2.4
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 32.4
- avg_decision_steps: 2.83
- avg_lookups: 3.55
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 6
- stated_difficulty: Catastrophic
- modeled_budget_tp: 336.0
- party: ['Oracle', 'Mirrorsage', 'Shaman', 'Wizard', 'Druid', 'Soldier']
**Observations**
- Ran high-level boss suites at listed difficulty Catastrophic for objective: Find ceilings, loops, and dead options.
- Budget model (4PC base adjusted): ~336 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=3.0, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: druid

**Metrics**
- class: Druid
- role: flexible
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 895.7
- avg_healing: 40.1
- avg_prevented: 81.4
- avg_control_applied: 9.6
- avg_lookups: 3.55
- avg_decision_steps: 2.83
- avg_rp_spent: 32.4
- class_dpr_model: 26.55
**Observations**
- Played 5 seeds as Druid (Shapeshift) under scenario CMB-L20-CEILING.
- Identity loop remained: Shapeshift; role=flexible.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=3.55.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 1.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 4
- avg_full_turns_denied: 0.0
- party: ['Oracle', 'Mirrorsage', 'Shaman', 'Wizard', 'Druid', 'Soldier']
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 5 seeds.
- Illegal summon pressure rate=1.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: mirrorsage

**Metrics**
- class: Mirrorsage
- role: control
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 895.7
- avg_healing: 40.1
- avg_prevented: 81.4
- avg_control_applied: 9.6
- avg_lookups: 3.55
- avg_decision_steps: 2.83
- avg_rp_spent: 32.4
- class_dpr_model: 25.15
**Observations**
- Played 5 seeds as Mirrorsage (Echo/Mirrorbind) under scenario CMB-L20-CEILING.
- Identity loop remained: Echo/Mirrorbind; role=control.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=3.55.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Do Reflective Companions count against the 2-summon cap and against the 1 copy release/round draft ceiling?
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Promote draft ceiling caps for Mirrorsage into Loop-aligned explicit rules.

### Agent: oracle

**Metrics**
- class: Oracle
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 895.7
- avg_healing: 40.1
- avg_prevented: 81.4
- avg_control_applied: 9.6
- avg_lookups: 3.55
- avg_decision_steps: 2.83
- avg_rp_spent: 32.4
- class_dpr_model: 16.77
**Observations**
- Played 5 seeds as Oracle (Revelations) under scenario CMB-L20-CEILING.
- Identity loop remained: Revelations; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=3.55.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Oracle draft '1 hard deny / target / encounter' vs Loop same-source denial escalation — which wins?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Keep both: Loop general rule + Oracle-specific 1 hard deny/target as tighter class ceiling.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 2.83
- avg_lookups: 3.55
- turns_over_three_lookups_estimate: 9.9
- ambiguity_flags: 3
- party: ['Oracle', 'Mirrorsage', 'Shaman', 'Wizard', 'Druid', 'Soldier']
**Observations**
- Average decision steps=2.83 (flag if >3).
- Average source lookups=3.55 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: shaman

**Metrics**
- class: Shaman
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 895.7
- avg_healing: 40.1
- avg_prevented: 81.4
- avg_control_applied: 9.6
- avg_lookups: 3.55
- avg_decision_steps: 2.83
- avg_rp_spent: 32.4
- class_dpr_model: 20.96
**Observations**
- Played 5 seeds as Shaman (Totems) under scenario CMB-L20-CEILING.
- Identity loop remained: Totems; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=3.55.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: soldier

**Metrics**
- class: Soldier
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 895.7
- avg_healing: 40.1
- avg_prevented: 81.4
- avg_control_applied: 9.6
- avg_lookups: 3.55
- avg_decision_steps: 2.83
- avg_rp_spent: 32.4
- class_dpr_model: 27.95
**Observations**
- Played 5 seeds as Soldier (Palisade/Overwatch) under scenario CMB-L20-CEILING.
- Identity loop remained: Palisade/Overwatch; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=3.55.
- Sample actions: Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).

### Agent: wizard

**Metrics**
- class: Wizard
- role: burst
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 3.0
- avg_party_damage: 895.7
- avg_healing: 40.1
- avg_prevented: 81.4
- avg_control_applied: 9.6
- avg_lookups: 3.55
- avg_decision_steps: 2.83
- avg_rp_spent: 32.4
- class_dpr_model: 33.53
**Observations**
- Played 5 seeds as Wizard (Spell Matrix/Necromancer) under scenario CMB-L20-CEILING.
- Identity loop remained: Spell Matrix/Necromancer; role=burst.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=3.0.
- Decision steps avg=2.83; rule lookups avg=3.55.
- Peak summons desired observed up to 4; illegal_rate=1.0.
- Turn frequently required >2 cross-references — readability stress.
**Rules questions**
- How do permanent undead from Core Systems interact with the 2-summon command cap?
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Exploits**
- Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
**Recommendations**
- Require Necromancer excess undead to use swarm/unit blocks; cite Loop summon rule in class path text.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 2.89
- avg_lookups: 3.25
- turns_over_three_lookups_estimate: 11.9
- ambiguity_flags: 4
**Observations**
- Average decision steps=2.89 (flag if >3).
- Average source lookups=3.25 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

## Scenario: CMB-L3-CARGO

### Agent: combat-metrics

**Metrics**
- iterations: 20
- win_rate: 0.35
- objective_rate: 0.35
- avg_rounds: 6.4
- avg_party_damage: 257.62
- avg_enemy_damage: 95.4
- avg_healing: 19.57
- avg_prevented: 37.95
- avg_control_applied: 6.75
- avg_full_turns_denied: 0.0
- max_summons_peak: 1
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 1.1
- avg_wounds: 0.6
- avg_rp_spent: 15.36
- avg_decision_steps: 1.51
- avg_lookups: 1.98
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 40.25
- effective_prevention_per_round: 5.93
- heal_to_damage_taken_ratio: 0.205
- cargo_intact_rounds_avg: 2.75
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 20
- win_rate: 0.35
- objective_rate: 0.35
- avg_rounds: 6.4
- avg_party_damage: 257.62
- avg_enemy_damage: 95.4
- avg_healing: 19.57
- avg_prevented: 37.95
- avg_control_applied: 6.75
- avg_full_turns_denied: 0.0
- max_summons_peak: 1
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 1.1
- avg_wounds: 0.6
- avg_rp_spent: 15.36
- avg_decision_steps: 1.51
- avg_lookups: 1.98
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 4
- stated_difficulty: Hard
- modeled_budget_tp: 130.0
**Observations**
- Ran mixed foes at listed difficulty Hard for objective: Protect 12-Load medicine crate for 4 rounds.
- Budget model (4PC base adjusted): ~130 Threat Points before objective/hazard steps.
- Observed win_rate=0.35, objective_rate=0.35, avg_rounds=6.4, KO/seed=1.1.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: aligned.
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 1
- avg_full_turns_denied: 0.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 20 seeds.
- Illegal summon pressure rate=0.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Exploits**
- No demonstrated infinite exploit under enforced Loop caps this scenario.
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: paladin

**Metrics**
- class: Paladin
- role: frontline
- win_rate: 0.35
- objective_rate: 0.35
- avg_rounds: 6.4
- avg_party_damage: 257.62
- avg_healing: 19.57
- avg_prevented: 37.95
- avg_control_applied: 6.75
- avg_lookups: 1.98
- avg_decision_steps: 1.51
- avg_rp_spent: 15.36
- class_dpr_model: 5.93
**Observations**
- Played 20 seeds as Paladin (Oath/Smite) under scenario CMB-L3-CARGO.
- Identity loop remained: Oath/Smite; role=frontline.
- Aggregate win_rate=0.35, objective_rate=0.35, avg_rounds=6.4.
- Decision steps avg=1.51; rule lookups avg=1.98.

### Agent: ranger

**Metrics**
- class: Ranger
- role: skirmish
- win_rate: 0.35
- objective_rate: 0.35
- avg_rounds: 6.4
- avg_party_damage: 257.62
- avg_healing: 19.57
- avg_prevented: 37.95
- avg_control_applied: 6.75
- avg_lookups: 1.98
- avg_decision_steps: 1.51
- avg_rp_spent: 15.36
- class_dpr_model: 6.22
**Observations**
- Played 20 seeds as Ranger (Track Target) under scenario CMB-L3-CARGO.
- Identity loop remained: Track Target; role=skirmish.
- Aggregate win_rate=0.35, objective_rate=0.35, avg_rounds=6.4.
- Decision steps avg=1.51; rule lookups avg=1.98.
- Peak summons desired observed up to 1; illegal_rate=0.0.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 1.51
- avg_lookups: 1.98
- turns_over_three_lookups_estimate: 0.0
- ambiguity_flags: 0
**Observations**
- Average decision steps=1.51 (flag if >3).
- Average source lookups=1.98 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- No severe ambiguity this scenario beyond normal class feature lookups.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: tinker

**Metrics**
- class: Tinker
- role: control
- win_rate: 0.35
- objective_rate: 0.35
- avg_rounds: 6.4
- avg_party_damage: 257.62
- avg_healing: 19.57
- avg_prevented: 37.95
- avg_control_applied: 6.75
- avg_lookups: 1.98
- avg_decision_steps: 1.51
- avg_rp_spent: 15.36
- class_dpr_model: 4.8
**Observations**
- Played 20 seeds as Tinker (Deployables) under scenario CMB-L3-CARGO.
- Identity loop remained: Deployables; role=control.
- Aggregate win_rate=0.35, objective_rate=0.35, avg_rounds=6.4.
- Decision steps avg=1.51; rule lookups avg=1.98.
- Peak summons desired observed up to 1; illegal_rate=0.0.
**Rules questions**
- Are Anacite drones and gadgets summons, deployables, or both for the command cap?
**Recommendations**
- Define deployables as non-summon structures unless they take independent combat turns.

### Agent: warrior

**Metrics**
- class: Warrior
- role: frontline
- win_rate: 0.35
- objective_rate: 0.35
- avg_rounds: 6.4
- avg_party_damage: 257.62
- avg_healing: 19.57
- avg_prevented: 37.95
- avg_control_applied: 6.75
- avg_lookups: 1.98
- avg_decision_steps: 1.51
- avg_rp_spent: 15.36
- class_dpr_model: 7.06
**Observations**
- Played 20 seeds as Warrior (Mutations) under scenario CMB-L3-CARGO.
- Identity loop remained: Mutations; role=frontline.
- Aggregate win_rate=0.35, objective_rate=0.35, avg_rounds=6.4.
- Decision steps avg=1.51; rule lookups avg=1.98.

## Scenario: CMB-L5-MOBILITY

### Agent: combat-metrics

**Metrics**
- iterations: 15
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 6.4
- avg_party_damage: 257.59
- avg_enemy_damage: 99.31
- avg_healing: 6.52
- avg_prevented: 20.03
- avg_control_applied: 8.2
- avg_full_turns_denied: 0.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.73
- avg_wounds: 0.4
- avg_rp_spent: 9.5
- avg_decision_steps: 1.0
- avg_lookups: 1.68
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 40.25
- effective_prevention_per_round: 3.13
- heal_to_damage_taken_ratio: 0.066
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 3.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: crimson-agent

**Metrics**
- class: Crimson Agent
- role: skirmish
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 6.4
- avg_party_damage: 257.59
- avg_healing: 6.52
- avg_prevented: 20.03
- avg_control_applied: 8.2
- avg_lookups: 1.68
- avg_decision_steps: 1.0
- avg_rp_spent: 9.5
- class_dpr_model: 10.94
**Observations**
- Played 15 seeds as Crimson Agent (Blood Mark) under scenario CMB-L5-MOBILITY.
- Identity loop remained: Blood Mark; role=skirmish.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=6.4.
- Decision steps avg=1.0; rule lookups avg=1.68.

### Agent: director

**Metrics**
- iterations: 15
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 6.4
- avg_party_damage: 257.59
- avg_enemy_damage: 99.31
- avg_healing: 6.52
- avg_prevented: 20.03
- avg_control_applied: 8.2
- avg_full_turns_denied: 0.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.73
- avg_wounds: 0.4
- avg_rp_spent: 9.5
- avg_decision_steps: 1.0
- avg_lookups: 1.68
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 4
- stated_difficulty: Hard
- modeled_budget_tp: 130.0
**Observations**
- Ran mobile skirmishers at listed difficulty Hard for objective: Control three elevated objectives.
- Budget model (4PC base adjusted): ~130 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=6.4, KO/seed=0.73.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: dragoon

**Metrics**
- class: Dragoon
- role: mobile
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 6.4
- avg_party_damage: 257.59
- avg_healing: 6.52
- avg_prevented: 20.03
- avg_control_applied: 8.2
- avg_lookups: 1.68
- avg_decision_steps: 1.0
- avg_rp_spent: 9.5
- class_dpr_model: 10.48
**Observations**
- Played 15 seeds as Dragoon (Momentum) under scenario CMB-L5-MOBILITY.
- Identity loop remained: Momentum; role=mobile.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=6.4.
- Decision steps avg=1.0; rule lookups avg=1.68.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 0
- avg_full_turns_denied: 0.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 15 seeds.
- Illegal summon pressure rate=0.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Exploits**
- No demonstrated infinite exploit under enforced Loop caps this scenario.
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: monk

**Metrics**
- class: Monk
- role: mobile
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 6.4
- avg_party_damage: 257.59
- avg_healing: 6.52
- avg_prevented: 20.03
- avg_control_applied: 8.2
- avg_lookups: 1.68
- avg_decision_steps: 1.0
- avg_rp_spent: 9.5
- class_dpr_model: 9.11
**Observations**
- Played 15 seeds as Monk (Ki/Stance) under scenario CMB-L5-MOBILITY.
- Identity loop remained: Ki/Stance; role=mobile.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=6.4.
- Decision steps avg=1.0; rule lookups avg=1.68.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 1.0
- avg_lookups: 1.68
- turns_over_three_lookups_estimate: 0.0
- ambiguity_flags: 0
**Observations**
- Average decision steps=1.0 (flag if >3).
- Average source lookups=1.68 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- No severe ambiguity this scenario beyond normal class feature lookups.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: thief

**Metrics**
- class: Thief
- role: skirmish
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 6.4
- avg_party_damage: 257.59
- avg_healing: 6.52
- avg_prevented: 20.03
- avg_control_applied: 8.2
- avg_lookups: 1.68
- avg_decision_steps: 1.0
- avg_rp_spent: 9.5
- class_dpr_model: 10.48
**Observations**
- Played 15 seeds as Thief (Sneak/Poison) under scenario CMB-L5-MOBILITY.
- Identity loop remained: Sneak/Poison; role=skirmish.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=6.4.
- Decision steps avg=1.0; rule lookups avg=1.68.

## Scenario: CMB-L5-SUPPORT

### Agent: bard

**Metrics**
- class: Bard
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 15.6
- avg_party_damage: 463.09
- avg_healing: 139.6
- avg_prevented: 77.88
- avg_control_applied: 22.93
- avg_lookups: 1.85
- avg_decision_steps: 1.5
- avg_rp_spent: 76.04
- class_dpr_model: 5.92
**Observations**
- Played 15 seeds as Bard (Crescendo) under scenario CMB-L5-SUPPORT.
- Identity loop remained: Crescendo; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=15.6.
- Decision steps avg=1.5; rule lookups avg=1.85.
- Sample actions: Crescendo consume for ally tempo; Crescendo consume for ally tempo; Crescendo consume for ally tempo; Crescendo consume for ally tempo; Crescendo consume for ally tempo
- Crescendo/tempo grants were offered; Loop additional-Action cap enforced when stacked with Action Surge.
**Rules questions**
- Does Crescendo-enhanced ally 'extra attack' count as the one additional full Action?
- Oracle attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter).
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
- Full-turn denial chain by Oracle without escalation cost — blocked by Loop rule in adjudication.
**Recommendations**
- Clarify Bard tempo grants as Bonus Action riders or as the single additional Action slot.

### Agent: cleric

**Metrics**
- class: Cleric
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 15.6
- avg_party_damage: 463.09
- avg_healing: 139.6
- avg_prevented: 77.88
- avg_control_applied: 22.93
- avg_lookups: 1.85
- avg_decision_steps: 1.5
- avg_rp_spent: 76.04
- class_dpr_model: 6.38
**Observations**
- Played 15 seeds as Cleric (Conviction) under scenario CMB-L5-SUPPORT.
- Identity loop remained: Conviction; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=15.6.
- Decision steps avg=1.5; rule lookups avg=1.85.
**Rules questions**
- Oracle attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter).
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
- Full-turn denial chain by Oracle without escalation cost — blocked by Loop rule in adjudication.

### Agent: combat-metrics

**Metrics**
- iterations: 15
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 15.6
- avg_party_damage: 463.09
- avg_enemy_damage: 162.37
- avg_healing: 139.6
- avg_prevented: 77.88
- avg_control_applied: 22.93
- avg_full_turns_denied: 2.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 1.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 76.04
- avg_decision_steps: 1.5
- avg_lookups: 1.85
- deadlock_seeds: 0
- retreat_success_rate: None
- dpr_party_estimate: 29.69
- effective_prevention_per_round: 4.99
- heal_to_damage_taken_ratio: 0.86
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
- Full-turn denial chain by Oracle without escalation cost — blocked by Loop rule in adjudication.
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 15
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 15.6
- avg_party_damage: 463.09
- avg_enemy_damage: 162.37
- avg_healing: 139.6
- avg_prevented: 77.88
- avg_control_applied: 22.93
- avg_full_turns_denied: 2.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 1.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 0.0
- avg_wounds: 0.0
- avg_rp_spent: 76.04
- avg_decision_steps: 1.5
- avg_lookups: 1.85
- deadlock_seeds: 0
- retreat_success_rate: None
- party_size: 4
- stated_difficulty: Hard
- modeled_budget_tp: 130.0
**Observations**
- Ran two-wave opposition at listed difficulty Hard for objective: Measure tempo, healing, and extra-action pressure.
- Budget model (4PC base adjusted): ~130 Threat Points before objective/hazard steps.
- Observed win_rate=1.0, objective_rate=1.0, avg_rounds=15.6, KO/seed=0.0.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: diverged — budget may need recalibration.
**Rules questions**
- Oracle attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter).
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
- Full-turn denial chain by Oracle without escalation cost — blocked by Loop rule in adjudication.
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 1.0
- deadlock_seeds: 0
- max_summons_peak: 0
- avg_full_turns_denied: 2.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 15 seeds.
- Illegal summon pressure rate=0.0; extra-action stack attempt rate=1.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Rules questions**
- Oracle attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter).
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
- Full-turn denial chain by Oracle without escalation cost — blocked by Loop rule in adjudication.
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: oracle

**Metrics**
- class: Oracle
- role: support
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 15.6
- avg_party_damage: 463.09
- avg_healing: 139.6
- avg_prevented: 77.88
- avg_control_applied: 22.93
- avg_lookups: 1.85
- avg_decision_steps: 1.5
- avg_rp_spent: 76.04
- class_dpr_model: 5.47
**Observations**
- Played 15 seeds as Oracle (Revelations) under scenario CMB-L5-SUPPORT.
- Identity loop remained: Revelations; role=support.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=15.6.
- Decision steps avg=1.5; rule lookups avg=1.85.
**Rules questions**
- Oracle attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter).
- Oracle draft '1 hard deny / target / encounter' vs Loop same-source denial escalation — which wins?
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
- Full-turn denial chain by Oracle without escalation cost — blocked by Loop rule in adjudication.
**Recommendations**
- Keep both: Loop general rule + Oracle-specific 1 hard deny/target as tighter class ceiling.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 1.5
- avg_lookups: 1.85
- turns_over_three_lookups_estimate: 0.0
- ambiguity_flags: 1
**Observations**
- Average decision steps=1.5 (flag if >3).
- Average source lookups=1.85 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- Oracle attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter).
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: soldier

**Metrics**
- class: Soldier
- role: frontline
- win_rate: 1.0
- objective_rate: 1.0
- avg_rounds: 15.6
- avg_party_damage: 463.09
- avg_healing: 139.6
- avg_prevented: 77.88
- avg_control_applied: 22.93
- avg_lookups: 1.85
- avg_decision_steps: 1.5
- avg_rp_spent: 76.04
- class_dpr_model: 9.11
**Observations**
- Played 15 seeds as Soldier (Palisade/Overwatch) under scenario CMB-L5-SUPPORT.
- Identity loop remained: Palisade/Overwatch; role=frontline.
- Aggregate win_rate=1.0, objective_rate=1.0, avg_rounds=15.6.
- Decision steps avg=1.5; rule lookups avg=1.85.
- Sample actions: Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention; Overwatch/Guard prevention
- Meaningful recurring choice preserved (Guard/Surge vs damage), but surge stacking with ally grants needed adjudication.
**Rules questions**
- Oracle attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter).
**Exploits**
- Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
- Full-turn denial chain by Oracle without escalation cost — blocked by Loop rule in adjudication.

## Scenario: CMB-RETREAT

### Agent: combat-metrics

**Metrics**
- iterations: 15
- win_rate: 0.8
- objective_rate: 0.8
- avg_rounds: 3.2
- avg_party_damage: 0.0
- avg_enemy_damage: 5600.31
- avg_healing: 0.0
- avg_prevented: 0.0
- avg_control_applied: 0.0
- avg_full_turns_denied: 0.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 12.8
- avg_wounds: 4.67
- avg_rp_spent: 0.0
- avg_decision_steps: 0.0
- avg_lookups: 0.0
- deadlock_seeds: 0
- retreat_success_rate: 0.8
- dpr_party_estimate: 0.0
- effective_prevention_per_round: 0.0
- heal_to_damage_taken_ratio: 0.0
- cargo_intact_rounds_avg: 0.0
- objectives_held_max_avg: 0.0
**Observations**
- Recorded rounds, damage, healing, prevention, control, summons peak, retreat progress, KOs, Wounds, RP proxy spend.
- DPR is model-estimated from class identity + level breakpoints (Extra Attack / Dual Cast / Nuke), not table dice transcripts.
**Recommendations**
- Keep outliers: report min/max rounds alongside averages in future tooling.
- Instrument live companion combat log to replace model DPR in later packs.

### Agent: director

**Metrics**
- iterations: 15
- win_rate: 0.8
- objective_rate: 0.8
- avg_rounds: 3.2
- avg_party_damage: 0.0
- avg_enemy_damage: 5600.31
- avg_healing: 0.0
- avg_prevented: 0.0
- avg_control_applied: 0.0
- avg_full_turns_denied: 0.0
- max_summons_peak: 0
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- avg_tenacity_triggers: 0.0
- avg_knockouts: 12.8
- avg_wounds: 4.67
- avg_rp_spent: 0.0
- avg_decision_steps: 0.0
- avg_lookups: 0.0
- deadlock_seeds: 0
- retreat_success_rate: 0.8
- party_size: 4
- stated_difficulty: Severe
- modeled_budget_tp: 180.0
**Observations**
- Ran unkillable pursuer proxy at listed difficulty Severe for objective: Use three-success Retreat procedure.
- Budget model (4PC base adjusted): ~180 Threat Points before objective/hazard steps.
- Observed win_rate=0.8, objective_rate=0.8, avg_rounds=3.2, KO/seed=12.8.
- Did not alter enemy HP/damage mid-run to force outcomes; Tenacity and summon caps applied as rulings when triggered.
- Difficulty vs result: aligned.
**Recommendations**
- Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.

### Agent: exploit-hunter

**Metrics**
- summons_illegal_rate: 0.0
- extra_action_stack_rate: 0.0
- deadlock_seeds: 0
- max_summons_peak: 0
- avg_full_turns_denied: 0.0
**Observations**
- Scanned for action loops, summon multiplication, permanent control, healing loops, cooldown resets across 15 seeds.
- Illegal summon pressure rate=0.0; extra-action stack attempt rate=0.0.
- No infinite round loop demonstrated when Loop caps were enforced; several soft exploits appear if caps are ignored.
**Exploits**
- No demonstrated infinite exploit under enforced Loop caps this scenario.
**Recommendations**
- Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.

### Agent: ranger

**Metrics**
- class: Ranger
- role: skirmish
- win_rate: 0.8
- objective_rate: 0.8
- avg_rounds: 3.2
- avg_party_damage: 0.0
- avg_healing: 0.0
- avg_prevented: 0.0
- avg_control_applied: 0.0
- avg_lookups: 0.0
- avg_decision_steps: 0.0
- avg_rp_spent: 0.0
- class_dpr_model: None
**Observations**
- Played 15 seeds as Ranger (Track Target) under scenario CMB-RETREAT.
- Identity loop remained: Track Target; role=skirmish.
- Aggregate win_rate=0.8, objective_rate=0.8, avg_rounds=3.2.
- Decision steps avg=0.0; rule lookups avg=0.0.
- Peak summons desired observed up to 0; illegal_rate=0.0.

### Agent: rules-observer

**Metrics**
- avg_decision_steps: 0.0
- avg_lookups: 0.0
- turns_over_three_lookups_estimate: 0.0
- ambiguity_flags: 0
**Observations**
- Average decision steps=0.0 (flag if >3).
- Average source lookups=0.0 (flag if >3).
- Ambiguity hotspots: Dual Cast vs additional Action; summon vs deployable; Bard tempo grants; Oracle deny vs Tenacity.
- GAMEPLAY_LOOP_CANON used was pending-review extract — not yet promoted SoT.
**Rules questions**
- No severe ambiguity this scenario beyond normal class feature lookups.
**Recommendations**
- Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.

### Agent: soldier

**Metrics**
- class: Soldier
- role: frontline
- win_rate: 0.8
- objective_rate: 0.8
- avg_rounds: 3.2
- avg_party_damage: 0.0
- avg_healing: 0.0
- avg_prevented: 0.0
- avg_control_applied: 0.0
- avg_lookups: 0.0
- avg_decision_steps: 0.0
- avg_rp_spent: 0.0
- class_dpr_model: None
**Observations**
- Played 15 seeds as Soldier (Palisade/Overwatch) under scenario CMB-RETREAT.
- Identity loop remained: Palisade/Overwatch; role=frontline.
- Aggregate win_rate=0.8, objective_rate=0.8, avg_rounds=3.2.
- Decision steps avg=0.0; rule lookups avg=0.0.

### Agent: thief

**Metrics**
- class: Thief
- role: skirmish
- win_rate: 0.8
- objective_rate: 0.8
- avg_rounds: 3.2
- avg_party_damage: 0.0
- avg_healing: 0.0
- avg_prevented: 0.0
- avg_control_applied: 0.0
- avg_lookups: 0.0
- avg_decision_steps: 0.0
- avg_rp_spent: 0.0
- class_dpr_model: None
**Observations**
- Played 15 seeds as Thief (Sneak/Poison) under scenario CMB-RETREAT.
- Identity loop remained: Sneak/Poison; role=skirmish.
- Aggregate win_rate=0.8, objective_rate=0.8, avg_rounds=3.2.
- Decision steps avg=0.0; rule lookups avg=0.0.

### Agent: tinker

**Metrics**
- class: Tinker
- role: control
- win_rate: 0.8
- objective_rate: 0.8
- avg_rounds: 3.2
- avg_party_damage: 0.0
- avg_healing: 0.0
- avg_prevented: 0.0
- avg_control_applied: 0.0
- avg_lookups: 0.0
- avg_decision_steps: 0.0
- avg_rp_spent: 0.0
- class_dpr_model: None
**Observations**
- Played 15 seeds as Tinker (Deployables) under scenario CMB-RETREAT.
- Identity loop remained: Deployables; role=control.
- Aggregate win_rate=0.8, objective_rate=0.8, avg_rounds=3.2.
- Decision steps avg=0.0; rule lookups avg=0.0.
- Peak summons desired observed up to 0; illegal_rate=0.0.
**Rules questions**
- Are Anacite drones and gadgets summons, deployables, or both for the command cap?
**Recommendations**
- Define deployables as non-summon structures unless they take independent combat turns.

## Scenario: unknown

### Agent: unknown


## Repeated rules questions

- (27) Mirrorsage copy release + Charm Bind companion: draft ceiling 1 copy/round vs observed desire to release + companion act — confirm both count toward action/summon caps.
- (27) Wizard Dual Cast (class-details L9) vs 'no more than one additional full Action' — is Dual Cast a second Action or a single Action with two spells?
- (27) Wizard Necromancer permanent undead (Core Systems Data) vs Gameplay Loop 2-summon command cap — unresolved layering.
- (20) Tinker draft ceiling 3 concurrent gadgets vs Loop summon cap 2 — are deployables 'summons'?
- (8) Mage Lich/Dark Resonance traumatic casting: self-damage and Dissonance bypass — needs explicit encounter-safe wording vs Loop anti-loop doctrine.
- (7) No severe ambiguity this scenario beyond normal class feature lookups.
- (7) Oracle attempted second full-turn denial from same control source without new save/escalation (Loop §Encounter).
- (4) Are Anacite drones and gadgets summons, deployables, or both for the command cap?
- (3) Does Crescendo-enhanced ally 'extra attack' count as the one additional full Action?
- (3) Do Reflective Companions count against the 2-summon cap and against the 1 copy release/round draft ceiling?
- (3) How do permanent undead from Core Systems interact with the 2-summon command cap?
- (3) Oracle draft '1 hard deny / target / encounter' vs Loop same-source denial escalation — which wins?
- (1) Traumatic Casting self-harm and Dissonance bypass: when does it violate anti-loop doctrine?

## Repeated exploit findings

- (27) Mirrorsage hypothesis: Mirrorbind release + Reflective Companion action approximates a second independent actor beyond 2-summon intent when Echo already active.
- (27) Wizard attempted 4 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- (20) Tinker attempted 3 independent combat units; GAMEPLAY_LOOP_CANON summon cap is 2 (excess should collapse to swarm/unit block).
- (16) Action-economy stack attempt on Soldier: class Action Surge/extra + Bard/support grant; Loop limit = choose one additional Action.
- (7) Full-turn denial chain by Oracle without escalation cost — blocked by Loop rule in adjudication.
- (6) No demonstrated infinite exploit under enforced Loop caps this scenario.

## Repeated recommendations

- (13) Keep outliers: report min/max rounds alongside averages in future tooling.
- (13) Instrument live companion combat log to replace model DPR in later packs.
- (13) Record budget outcomes in BALANCE ledger; revise Threat Point table only with multi-scenario evidence.
- (13) Publish Director ruling sheet for summon-cap vs undead/deployables/reflections.
- (13) Treat unenforced summon/action caps as release blockers before V7 Gameplay Complete promotion.
- (13) Add automated assertions: summons<=2, additional_actions<=1, same_source_deny<=1 without escalation.
- (13) Add a one-page Encounter Mode timing strip (Action / Bonus / Reaction / additional Action cap / summon cap / Tenacity).
- (13) Cross-link class-ceiling-caps.js draft text into Loop glossary when promoted.
- (4) Define deployables as non-summon structures unless they take independent combat turns.
- (4) Ensure Tenacity + same-source denial limit are cross-linked in Director quick reference.
- (3) Clarify Bard tempo grants as Bonus Action riders or as the single additional Action slot.
- (3) Promote draft ceiling caps for Mirrorsage into Loop-aligned explicit rules.
- (3) Require Necromancer excess undead to use swarm/unit blocks; cite Loop summon rule in class path text.
- (3) Keep both: Loop general rule + Oracle-specific 1 hard deny/target as tighter class ceiling.


