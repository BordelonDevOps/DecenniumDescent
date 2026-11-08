# Daily Provisioning and Expedition Strain (schema62, TEST_ONLY)

## Module checkpoint

This is a bounded C# simulation increment on `Engine`, built on the current schema61 checkpoint. The four concrete blockers from GPT's first evidence review are corrected and have regressions. The mandatory review of this corrected commit is pending. Do not begin the successor module until GPT has reviewed the updated evidence, all concrete blockers are resolved, and both reviewers agree on the next dependency.

The increment executes the adopted fixed-profile daily rules over the existing shared world. It is not production authority and does not complete Decennium's engine.

## Responsibilities and source requirements

- Immutable, fingerprinted TEST_ONLY provisioning profile with `RuleTime.Zero` day origin, fixed hero/companion roster, 2 lb food and 8 pint water per actor/day, and half-open 86,400-second days.
- Actual consumed food and water only, backed by existing intake intervals, inventory lots, and consumed WorkLedger reservations; freshness clips credit. One shortfall produces one Strain point per actor/day. Every crossed endpoint settles once, even when one clock command crosses multiple days.
- Source-qualified `expedition.strain` history with the adopted six-level effects and explicit ordinary-death endpoint; no Strain RNG or changes to the authored initiative order.
- The versioned Expedition-check registry admits only existing stationary Map Route and route-reconnaissance completion checks. Other checks are not silently enrolled.
- No retroactive provisioning before the fixed epoch, special diets, roster changes, Strain recovery, offline progress, tactical intake, generalized watches, or production rules.

The pinned requirements and delegated proposal boundaries are documented in [DAILY_PROVISIONING_RULE_DECISIONS.md](../../DAILY_PROVISIONING_RULE_DECISIONS.md). Four exact source snapshots at commit `46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4` are listed in [SOURCE_BINDINGS.json](SOURCE_BINDINGS.json) and retained under [sources](sources/).

## Authoritative records and dependencies

`RuleClock` remains the elapsed-time authority. `IntakeRecord`, `InventoryLotRecord`, and the consumed reservation in `WorkLedger` remain the authorities for intake actor, physical lot, interval, quantity, custody, and actual consumption. The existing inventory and filling procedures continue to own reservations and material settlement.

The new `DailyProvisioningSettlementRecord` and `DailyProvisioningConsumptionRecord` append endpoint results and their per-intake, per-lot attribution. `ExpeditionStrainGainRecord` owns the new cause-bound Strain point history. Existing `ActorCharacterRecord`, `ActorLifeRecord`, condition, movement, world calendar, work assignments, RNG, commands/receipts, and persistence remain their original authorities. The fixed profile is immutable content, not another mutable roster or clock record.

## Runnable acceptance

All thirteen cases below passed in the current full C# run; [MODULE_CASE_RESULTS.json](MODULE_CASE_RESULTS.json) is a selected-case view of the [full report](FULL_TEST_RESULTS.json), not a separate test invocation.

- `daily_provisioning_profile_is_test_only_fingerprinted_and_restorable` checks epoch, roster/fingerprint identity, release rejection, and codec restore.
- `daily_provisioning_exploration_intake_boundary_restore_and_replay` explores to the plot, hands a real ration lot to the companion, saves/restores intake before midnight, credits completion at the boundary, blocks same-time rewriting after closure, and checks idempotent receipt replay.
- `daily_provisioning_full_food_and_water_uses_real_shared_lots` fulfills the companion's complete daily needs from actual food and two water lots filled through the existing two-hand procedure; the hero remains short. It verifies each evidence record links to the real intake and consumed reservation, then saves/restores and compares deterministic continuation.
- `daily_provisioning_single_advance_settles_every_crossed_day` advances three days in one command, validates all six actor/day settlements and three gains per actor, then restores and replays continuation.
- `daily_provisioning_map_route_and_reconnaissance_checks_use_strain` resolves both registered route procedures after the first Strain endpoint and verifies the recorded causal check modifiers.
- `daily_provisioning_level_two_reaches_shared_tactical_attack` explores into a real encounter and verifies the level-two Strain penalty in the actual melee attack record.
- `daily_provisioning_multiday_catchup_projects_strain_and_death` checks effect levels one through six, initiative/RNG invariance, effective HP, ordinary-death settlement, byte-exact restore, and deterministic replay.
- `daily_provisioning_one_intake_is_attributed_across_both_midnight_intervals` saves/restores an intake spanning midnight, verifies separate attribution to both day intervals, and compares deterministic continuation.
- `daily_provisioning_candidate_strain_changes_route_pace_across_one_transaction` crosses a Strain speed boundary in one route command and compares it to split commands, including save/restore at the boundary.
- `daily_provisioning_candidate_strain_interrupts_work_inside_boundary_transaction` crosses the level-five work interruption boundary during intake, then verifies consumed/released quantities and restored replay.
- `daily_provisioning_effective_maximum_bounds_healing_and_dose_attribution` checks dose healing at the effective HP cap while retaining base maximum HP, plus critical healing and damage thresholds at that effective cap.
- `daily_provisioning_dash_deadline_uses_exploration_after_encounter_exit` retains encounter history, exits active tactical control, and checks initiative-based versus exploration Dash deadlines for the hero and an off-calendar companion.
- `daily_provisioning_modified_death_save_gates_d4_and_restores_rng` verifies that the modified save result gates stable recovery, with exact RNG advancement across save/restore.

## Validation

- Full repository C# 9 warnings-as-errors run: **1,255/1,255 passed**; Core, Persistence, LabModel, and headless tests compiled. The final-source run is [FULL_TEST_RESULTS.json](FULL_TEST_RESULTS.json), with source hashes for all 249 C# inputs.
- Static package validation: **18/18 passed**, **275 assets / 275 unique GUIDs** — [PACKAGE_RESULTS.json](PACKAGE_RESULTS.json). This checks static package structure only.
- Fresh source-bound rule audit: **4 source snapshots / 17 profiles / 340 RP cells / 13 named cases passed** — [RULE_BINDINGS_VALIDATION.json](RULE_BINDINGS_VALIDATION.json).
- `git diff --check`: passed.
- Retained actual compiled C# outputs are in [assemblies](assemblies/); every source hash from the full run is retained in `FULL_TEST_RESULTS.json`.
- No Unity import, editor compile, scene, Play Mode, or player build was run; Unity gameplay integration remains deferred by the project goal.

## Reproduced failures and corrections

The retained [development attempts](development-attempts/) show the material failed checks from this increment. All were corrected before the final full run:

- One-command multi-day settlement initially returned `InvalidResult`: historical Strain validation excluded earlier endpoints because all gains from one clock command share a revision. Validation now orders earlier gains by canonical endpoint time; the 3-day reproducer passes.
- A composed route profile initially failed with `RouteTravelSchemaMismatch`: the shared route-travel validator had no opt-in schema62 extension. That gate now allows the existing route profile under the selected daily profile; both route checks pass.
- A tactical test setup initially left a traversal pending because its one-second movement assumption ignored the level-two speed penalty. The acceptance now completes approach before Strain accrues, then enters combat and verifies the attack penalty.
- The first full-provision setup attempted to fill while the hero held a club and correctly received `TwoHandsRequired`. The acceptance now uses the companion's two available hands and does not bypass that adopted rule.
- One intermediate test compile referenced custody on `InventoryLotRecord`; custody is authoritative in `WorkLedger.ResourceLot`, and the test now reads that record.

The no-argument binding validator still points to an older historical evidence directory. This increment uses its explicit fresh manifest; no old source pin was rewritten.

## GPT review corrections

GPT's review of commit `d4662e3` found four concrete blockers. Each was independently reproduced, corrected, and covered by a regression:

- Candidate state is resolved before `Simulation` advances the committed revision. Current Strain projections now include the pending command revision, so same-command endpoint settlement affects later movement and work in that transaction just as it does in split commands.
- Damage and healing now resolve against the effective maximum HP. Persisted `ActorLifeRecord.MaximumHp` remains the base character authority; actual healing attribution uses the HP gained after the effective cap is applied.
- Dash uses an initiative deadline only during active tactical control and only for an actor in the encounter order. A retained encounter snapshot after combat exit, or an off-calendar companion, uses the exploration deadline.
- The stable-recovery d4 gate now tests the modified death-save result and preserves natural 1/20 exceptions, preventing a spurious d4 draw and RNG advance.

GPT also requested a cross-midnight intake acceptance; that case now saves/restores across midnight and verifies both half-open day attributions. The repair evidence README describes Carpenter eligibility as `IsRepairWorker` plus the explicit `SharedRepairFixture.Trained` fixture fact; no qualification is inferred from `SkillTrainingRecord`.

Clean pre-fix reproductions for all four behavioral blockers are retained here: [same-command route pace](development-attempts/gpt-review-reproduction-clean/candidate-route-pace.json), [same-command work interruption](development-attempts/gpt-review-reproduction-clean/candidate-work-interruption.json), [effective-HP healing](development-attempts/gpt-review-reproduction-clean/effective-hp-healing.json), [post-encounter Dash](development-attempts/gpt-review-reproduction-clean/dash-after-encounter-exit.json), and [modified death-save RNG gating](development-attempts/gpt-review-reproduction-clean/modified-death-save.json). These are focused pre-fix results; other early attempts also include test-fixture setup and harness corrections, which are not reported as gameplay defects.

## Limitations

This remains one fixed, TEST_ONLY profile. It does not deliver general provisioning content, special diets, a general camp/watch/rest calendar, production settlement authority, Strain recovery, or every condition/check/action specified by the full rule sources. Tactical intake, generalized roster changes, historical back-assessment, and offline progress remain gated. The C# engine is not complete; GPT review of this increment is the current gate.
