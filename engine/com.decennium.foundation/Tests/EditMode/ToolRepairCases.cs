#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static TestOnlySharedWorldPolicy RepairPolicy(uint seed = 1, SharedRepairFixture facts = null, SharedCraftingFixture crafting = null,
            SharedResearchFixture research = null, ConditionCombatFixture conditions = null)
            => new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed), research, crafting ?? new SharedCraftingFixture(toolHp: 0), facts ?? new SharedRepairFixture(), conditions: conditions);
        private static Command RepairCommand(Simulation s, CommandKind kind = CommandKind.StartToolRepair, string target = SharedCraftingFixture.ToolId, string actor = TestOnlyPolicy.CompanionId)
            => new Command("repair-command." + (s.Capture().Revision + 1), actor, s.Capture().Revision, kind, target);
        private static void RepairStart(Simulation s, string worker = TestOnlyPolicy.CompanionId) => WorldCommit(s, RepairCommand(s, actor: worker));
        private static RepairWorkRecord RepairJob(Simulation s) => s.Capture().RepairWork.Last();
        private static void RepairControl(Simulation s, CommandKind kind, string worker = TestOnlyPolicy.CompanionId) => WorldCommit(s, RepairCommand(s, kind, RepairJob(s).Id, worker));
        private static RuleQuantity RepairStock(Simulation s) => s.Capture().Work.Lots.Single(x => x.Id == SharedRepairFixture.Materials).Amount;
        private static ObjectStructureRecord RepairTarget(Simulation s) => s.Capture().Structures.Single(x => x.Id == SharedCraftingFixture.ToolId);
        private static uint WoundedCheckSeed(Injury injury, int natural)
        {
            for (uint seed = 1; seed < 2000000; seed++) {
                var d4 = DiceStream.Draw(seed, 4); var damage = PlaytestDamageDice.Resolve(new LifeState(26, 1), d4.Value + 1, default, d4.NextState);
                if (damage.InjuryD6 != (int)injury) continue;
                var recovery = PlaytestDice.RollD20(damage.NextRandomState);
                if (recovery.Natural == 20 && PlaytestDice.RollD20(recovery.NextRandomState).Natural == natural) return seed;
            }
            throw new Exception("No wounded check fixture seed.");
        }
        private static void AddToolRepairCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host(); const string worker = TestOnlyPolicy.CompanionId, hero = TestOnlyPolicy.ActorId;
            cases.Add("tool_repair_active_target_blocks_another_workers_calibration", () => {
                var s = World(RepairPolicy(crafting: new SharedCraftingFixture(toolHp: 4, heroProficient: true, events: new[] { new CraftingMishapFact("calibrate", 2) })));
                CraftEvent(s, "calibrate"); RepairStart(s); HeroToWorkshop(s);
                RejectUnchanged(s, host, CraftCommand(s, "calibrate", CommandKind.StartCraftRemedy, hero), "CraftRemedyWorkerIneligible"); WorldAdvance(s, 10);
                Require(Incident(s, "calibrate").Labor == default && RepairJob(s).Work.Labor == T(15), "Same kit was calibrated during physical repair.");
            });
            cases.Add("tool_repair_acquisition_preempts_actual_calibration_preserving_labor", () => {
                foreach (string calibrator in new[] { worker, hero }) {
                    var s = World(RepairPolicy(crafting: new SharedCraftingFixture(toolHp: 4, heroProficient: true, events: new[] { new CraftingMishapFact("calibrate", 2) })));
                    CraftEvent(s, "calibrate"); if (calibrator == hero) HeroToWorkshop(s); Remedy(s, "calibrate", calibrator); WorldAdvance(s, 10); RepairStart(s); WorldAdvance(s, 10);
                    Require(Incident(s, "calibrate").Labor == T(10) && Incident(s, "calibrate").Workers.Count == 0 && RepairJob(s).Work.Labor == T(10), "Repair overlapped or discarded calibration.");
                    RepairControl(s, CommandKind.PauseToolRepair); WorldAdvance(s, 1); Require(Incident(s, "calibrate").Labor == T(10), "Calibration auto-resumed.");
                    Remedy(s, "calibrate", calibrator); WorldAdvance(s, 1); RepairControl(s, CommandKind.ResumeToolRepair);
                    Require(Incident(s, "calibrate").Workers.Count == 0 && Incident(s, "calibrate").Labor == T(11), "Repair resume did not reacquire the same target.");
                }
            });
            cases.Add("tool_repair_rejected_acquisition_keeps_calibration_work_and_inputs", () => {
                var s = World(RepairPolicy(facts: new SharedRepairFixture(trained: false), crafting: new SharedCraftingFixture(toolHp: 4, events: new[] { new CraftingMishapFact("calibrate", 2) })));
                CraftEvent(s, "calibrate"); Remedy(s, "calibrate"); WorldAdvance(s, 10); RejectUnchanged(s, host, RepairCommand(s), "RepairTrainingMissing"); WorldAdvance(s, 1);
                Require(Incident(s, "calibrate").Labor == T(11) && RepairStock(s) == new RuleQuantity(2), "Rejected repair interrupted real work.");
            });
            cases.Add("tool_repair_recovered_workers_linked_injury_changes_actual_dc_edge", () => {
                foreach (var injury in new[] { Injury.FineMotorTrauma, Injury.ExertionTrauma }) {
                    var s = World(RepairPolicy(WoundedCheckSeed(injury, 8), crafting: new SharedCraftingFixture(companionHp: 1, toolHp: 4, events: new[] { new CraftingMishapFact("acid", 4) })));
                    CraftEvent(s, "acid"); WorldAdvance(s, 6); Require(s.Capture().Lives.Single(x => x.ActorId == worker).Hp == 1, "Fixture did not recover through real life marker.");
                    RepairStart(s); WorldAdvance(s, 3600);
                    Require(RepairJob(s).Natural == 8 && RepairJob(s).Status == RepairWorkStatus.Failure && RepairTarget(s).Hp == 4, "Repair omitted linked Injury penalty or granted failed HP.");
                }
            });
            cases.Add("ability_check_injury_penalties_apply_strongest_matching_once", () => {
                var both = new LifeState(26, 10, wounds: new[] { Injury.FineMotorTrauma, Injury.FineMotorTrauma, Injury.ExertionTrauma });
                Require(PlaytestLife.AbilityCheckInjuryPenalty(both, 1, toolCheck: true) == -1 && PlaytestLife.AbilityCheckInjuryPenalty(both, 2) == 0
                    && PlaytestLife.AbilityCheckInjuryPenalty(new LifeState(26, 10, wounds: new[] { Injury.None }), 1, toolCheck: true) == 0, "Stacked Injury or generic Wound penalty.");
                var cognitive = new LifeState(26, 10, wounds: new[] { Injury.CognitiveTrauma });
                for (int ability = 0; ability < 6; ability++) Require(PlaytestLife.AbilityCheckInjuryPenalty(cognitive, ability) == (ability >= 3 ? -1 : 0), "Wrong cognitive ability.");
                var concussion = new LifeState(26, 10, wounds: new[] { Injury.Concussion });
                Require(PlaytestLife.AbilityCheckInjuryPenalty(concussion, 1, initiative: true) == -1 && PlaytestLife.AbilityCheckInjuryPenalty(concussion, 4, perception: true) == -1
                    && PlaytestLife.AbilityCheckInjuryPenalty(concussion, 1) == 0, "Concussion became general ability penalty.");
                var fine = new LifeState(26, 10, wounds: new[] { Injury.FineMotorTrauma });
                Require(PlaytestLife.AbilityCheckInjuryPenalty(fine, 1, manipulatesObject: true) == -1 && PlaytestLife.AbilityCheckInjuryPenalty(fine, 0, manipulatesObject: true) == 0, "Manipulation ability misclassified.");
            });
            cases.Add("tool_repair_schema17_copy_uses_writing_supplies_without_alchemy_kit", () => {
                var s = World(RepairPolicy(research: new SharedResearchFixture())); ResearchStart(s, copy: true); WorldAdvance(s, 3600);
                Require(ResearchJob(s).Status == FormulaWorkStatus.Success && RepairTarget(s).Broken && WritingStock(s) == new RuleQuantity(2), "Copy incorrectly depended on broken Alchemy kit.");
                var legacy = World(CraftPolicy(new SharedCraftingFixture(toolHp: 0), research: new SharedResearchFixture()));
                RejectUnchanged(legacy, host, ResearchCommand(legacy, CommandKind.StartFormulaCopy, SharedResearchFixture.LegibleFormula), "ResearchToolsOrStationUnavailable");
            });
            cases.Add("tool_repair_copy_break_history_retains_legacy16_semantics", () => {
                foreach (bool current in new[] { false, true }) {
                    var facts = new SharedCraftingFixture(toolHp: 1, events: new[] { new CraftingMishapFact("break", 3, at: T(10)) });
                    var p = current ? RepairPolicy(crafting: facts, research: new SharedResearchFixture()) : CraftPolicy(facts, research: new SharedResearchFixture());
                    var s = World(p); ResearchStart(s, copy: true); WorldAdvance(s, 10); CraftEvent(s, "break");
                    Require(ResearchJob(s).Status == (current ? FormulaWorkStatus.Working : FormulaWorkStatus.Paused), "Versioned copying eligibility drifted.");
                    var restored = new Simulation(p, new SnapshotCodec().Decode(Bytes(s)), ExecutionProfile.Laboratory);
                    Require(Bytes(s).SequenceEqual(Bytes(restored)), "Copy break history did not replay.");
                }
            });
            cases.Add("tool_repair_shared_bench_supports_distinct_worker_copy_and_repair", () => {
                var s = World(RepairPolicy(SeedForDeath(8), research: new SharedResearchFixture(workerId: hero))); HeroToWorkshop(s); ResearchStart(s, copy: true, worker: hero); RepairStart(s); WorldAdvance(s, 3600);
                Require(ResearchJob(s).Status == FormulaWorkStatus.Success && RepairJob(s).Status == RepairWorkStatus.Success && RepairTarget(s).Hp == 5
                    && WritingStock(s) == new RuleQuantity(2) && RepairStock(s) == new RuleQuantity(1), "Compatible distinct workers did not each pay and complete actual work.");
            });
            cases.Add("tool_repair_same_worker_copy_must_pause_explicitly", () => {
                var s = World(RepairPolicy(research: new SharedResearchFixture())); ResearchStart(s, copy: true); WorldAdvance(s, 10);
                RejectUnchanged(s, host, RepairCommand(s), "WorkerBusy"); Require(ResearchJob(s).Status == FormulaWorkStatus.Working, "Repair implicitly took over independent copying.");
                ResearchControl(s, CommandKind.PauseFormulaWork); RepairStart(s); WorldAdvance(s, 10);
                Require(ResearchJob(s).Work.Labor == T(10) && RepairJob(s).Work.Labor == T(10), "Worker overlapped copying and repair.");
            });
            cases.Add("tool_repair_schema17_research_injury_penalty_preserves_legacy16_outcomes", () => {
                foreach (var injury in new[] { Injury.CognitiveTrauma, Injury.FineMotorTrauma }) foreach (bool current in new[] { false, true }) {
                    var facts = new SharedCraftingFixture(companionHp: 1, events: new[] { new CraftingMishapFact("acid", 4) }); uint seed = WoundedCheckSeed(injury, 6);
                    var p = current ? RepairPolicy(seed, crafting: facts, research: new SharedResearchFixture()) : CraftPolicy(facts, seed, research: new SharedResearchFixture());
                    var s = World(p); CraftEvent(s, "acid"); WorldAdvance(s, 6); ResearchStart(s); WorldAdvance(s, 28794); ResearchControl(s, CommandKind.ResumeFormulaWork); WorldAdvance(s, 6);
                    Require(ResearchJob(s).Natural == 6 && ResearchJob(s).Status == (current ? FormulaWorkStatus.Failure : FormulaWorkStatus.Success), "Research injury fix changed legacy history or missed actual injury.");
                    Require(Bytes(new Simulation(p, new SnapshotCodec().Decode(Bytes(s)), ExecutionProfile.Laboratory)).SequenceEqual(Bytes(s)), "Wounded research outcome cannot replay.");
                }
            });
            cases.Add("tool_repair_explicit_schema17_and_separate_physical_toolkit", () => {
                var p = RepairPolicy(); var s = World(p); var kit = s.Capture().Structures.Single(x => x.Id == SharedRepairFixture.Toolkit);
                Require(s.Capture().SchemaVersion == 17 && CraftPolicy(new SharedCraftingFixture()).Initial().SchemaVersion == 16 && kit.Id != RepairTarget(s).Id
                    && kit.Hp == 5 && kit.BaselineCopper == 800 && kit.MassPounds == new RuleQuantity(6) && RepairTarget(s).Broken, "Repair borrowed its broken target or altered old profile.");
                Throws<InvalidOperationException>(() => new Simulation(p, p.Initial(), ExecutionProfile.Release));
            });
            cases.Add("tool_repair_requires_actual_qualification_body_implements_tools_and_access", () => {
                foreach (var row in new[] {
                    (new SharedRepairFixture(trained:false),"RepairTrainingMissing"), (new SharedRepairFixture(usableToolkit:false),"RepairToolkitUnavailable"),
                    (new SharedRepairFixture(recoverableBody:false),"RepairTargetUnsupported"), (new SharedRepairFixture(intactImplements:false),"RepairTargetUnsupported"),
                    (new SharedRepairFixture(accessible:false),"RepairAccessUnavailable") }) {
                    var s = World(RepairPolicy(facts: row.Item1)); RejectUnchanged(s, host, RepairCommand(s), row.Item2);
                }
                var valid = World(RepairPolicy()); RejectUnchanged(valid, host, RepairCommand(valid, target: SharedRepairFixture.Toolkit), "RepairTargetUnsupported");
                var intact = World(RepairPolicy(crafting: new SharedCraftingFixture())); RejectUnchanged(intact, host, RepairCommand(intact), "TargetDoesNotNeedRepair");
            });
            cases.Add("tool_repair_current_owner_grants_checked_before_start_resume_and_duplicate", () => {
                var s = World(RepairPolicy()); var revoked = new Authority(host.Principal, new[] { worker }); var start = RepairCommand(s);
                RejectUnchanged(s, revoked, start, "InventoryNotAuthorized"); WorldCommit(s, start); RejectUnchanged(s, revoked, start, "InventoryNotAuthorized");
                RepairControl(s, CommandKind.PauseToolRepair); RejectUnchanged(s, revoked, RepairCommand(s, CommandKind.ResumeToolRepair, RepairJob(s).Id), "InventoryNotAuthorized");
                RepairControl(s, CommandKind.ResumeToolRepair); Require(RepairStock(s) == new RuleQuantity(2), "Authority retry consumed supplies before labor.");
            });
            cases.Add("tool_repair_reserves_then_consumes_first_positive_labor_only_once", () => {
                var s = World(RepairPolicy(SeedForDeath(8))); RepairStart(s);
                Require(RepairStock(s) == new RuleQuantity(2) && s.Capture().Work.AvailableAmount(SharedRepairFixture.Materials) == new RuleQuantity(1), "Scheduled repair consumed supplies.");
                RepairControl(s, CommandKind.PauseToolRepair); WorldAdvance(s, 10); RepairControl(s, CommandKind.ResumeToolRepair); WorldAdvance(s, 1, 3);
                Require(RepairStock(s) == new RuleQuantity(1) && RepairTarget(s).Hp == 0, "Positive labor failed whole debit or granted partial repair.");
                RepairControl(s, CommandKind.PauseToolRepair); RepairControl(s, CommandKind.ResumeToolRepair); WorldAdvance(s, 10799, 3);
                Require(RepairJob(s).Status == RepairWorkStatus.Success && RepairJob(s).Natural == 8 && RepairStock(s) == new RuleQuantity(1) && RepairTarget(s).Hp == 5, "Repair charged twice or failed DC edge.");
            });
            cases.Add("tool_repair_exact_hour_restores_existing_object_only_after_success", () => {
                var s = World(RepairPolicy(SeedForDeath(8), crafting: new SharedCraftingFixture(toolHp: 2))); var before = RepairTarget(s); RepairStart(s); uint rng = s.Capture().RandomState; WorldAdvance(s, 3599);
                Require(RepairTarget(s).Hp == 2 && s.Capture().RandomState == rng, "Unfinished labor repaired HP or rolled early."); WorldAdvance(s, 1); var after = RepairTarget(s);
                Require(after.Hp == 5 && after.MaximumHp == 5 && after.Id == before.Id && after.LocationId == before.LocationId && after.OwnerId == before.OwnerId && after.CustodianId == before.CustodianId
                    && after.MassPounds == before.MassPounds && s.Capture().Structures.Length == 2 && !RepairJob(s).Open, "Success recreated or moved the object.");
                RejectUnchanged(s, host, RepairCommand(s), "TargetDoesNotNeedRepair");
            });
            cases.Add("tool_repair_failure_spends_material_and_time_retry_starts_fresh", () => {
                var s = World(RepairPolicy(TacticalSeed(7, 8))); RepairStart(s); WorldAdvance(s, 3600);
                Require(RepairJob(s).Status == RepairWorkStatus.Failure && RepairTarget(s).Broken && RepairStock(s) == new RuleQuantity(1), "Failure repaired or refunded.");
                RepairStart(s); Require(RepairJob(s).Work.Labor == default && s.Capture().RepairWork.Length == 2, "Retry borrowed failed labor."); WorldAdvance(s, 3600);
                Require(RepairJob(s).Status == RepairWorkStatus.Success && RepairTarget(s).Hp == 5 && RepairStock(s) == default, "Retry did not settle its new full cost.");
            });
            cases.Add("tool_repair_cancellation_releases_unspent_inputs_and_never_refunds_labor", () => {
                var s = World(RepairPolicy()); RepairStart(s); RepairControl(s, CommandKind.CancelToolRepair);
                Require(s.Capture().Work.AvailableAmount(SharedRepairFixture.Materials) == new RuleQuantity(2), "Unstarted cancellation lost materials.");
                RepairStart(s); WorldAdvance(s, 1); RepairControl(s, CommandKind.CancelToolRepair); RepairStart(s);
                Require(RepairStock(s) == new RuleQuantity(1) && RepairJob(s).Work.Labor == default && RepairTarget(s).Broken, "Cancellation refunded material or transferred progress.");
                WorldAdvance(s, 1); RepairControl(s, CommandKind.CancelToolRepair); RejectUnchanged(s, host, RepairCommand(s), "RepairMaterialsUnavailable");
            });
            cases.Add("tool_repair_partial_disk_restore_continues_without_extra_charge", () => {
                var p = RepairPolicy(SeedForDeath(8)); var s = World(p); RepairStart(s); WorldAdvance(s, 123, 7); RepairControl(s, CommandKind.PauseToolRepair);
                string path = Path.Combine(directory, "tool-repair-partial.bin"); new FileSaveStore().Save(path, s.Capture()); var restored = new Simulation(p, new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                foreach (var sim in new[] { s, restored }) { RepairControl(sim, CommandKind.ResumeToolRepair); WorldAdvance(sim, 25077, 7); }
                Require(Bytes(s).SequenceEqual(Bytes(restored)) && RepairJob(s).Status == RepairWorkStatus.Success && RepairStock(s) == new RuleQuantity(1), "Disk repair duplicated cost or changed outcome.");
            });
            cases.Add("tool_repair_target_claim_survives_pause_and_releases_on_cancel", () => {
                var s = World(RepairPolicy()); HeroToWorkshop(s); RepairStart(s); RepairControl(s, CommandKind.PauseToolRepair);
                RejectUnchanged(s, host, RepairCommand(s, actor: hero), "RepairTargetClaimed"); RepairControl(s, CommandKind.CancelToolRepair); RepairStart(s, hero);
                Require(RepairJob(s).WorkerId == hero && RepairStock(s) == new RuleQuantity(2), "Cancellation failed to release target or consumed unstarted inputs.");
            });
            cases.Add("tool_repair_incapacity_retains_work_until_explicit_resume", () => {
                var p = RepairPolicy(SeedForDeath(8), conditions: new ConditionCombatFixture(CCApply("stun", "Stunned", worker, new ConditionStamp(T(20)), new ConditionStamp(T(10)))));
                var s = World(p); RepairStart(s); WorldAdvance(s, 10); CCDispatch(s, "stun", worker); WorldAdvance(s, 10);
                Require(RepairJob(s).Status == RepairWorkStatus.Paused && RepairJob(s).Work.Labor == T(10) && RepairStock(s) == new RuleQuantity(1), "Incapacity lost work, refunded or auto-resumed.");
                RepairControl(s, CommandKind.ResumeToolRepair); WorldAdvance(s, 3590); Require(RepairTarget(s).Hp == 5, "Recovered worker could not finish actual remainder.");
            });
            cases.Add("tool_repair_poisoned_check_uses_actual_completion_state", () => {
                var s = World(RepairPolicy(TacticalSeed(18, 3), conditions: new ConditionCombatFixture(CCApply("poison", "Poisoned", worker)))); CCDispatch(s, "poison", worker); RepairStart(s); WorldAdvance(s, 3600);
                Require(RepairJob(s).First == 18 && RepairJob(s).Second == 3 && RepairJob(s).Natural == 3 && RepairJob(s).Status == RepairWorkStatus.Failure && RepairTarget(s).Broken, "Repair ignored current disadvantage.");
            });
            cases.Add("tool_repair_complete_incapacity_keeps_target_claim_without_worker_booking", () => {
                var cure = new ConditionFixtureEvent(worker, ConditionOperation.Cure("event.cure", new ConditionStamp(T(3601)), "Stunned"));
                var p = RepairPolicy(SeedForDeath(8), conditions: new ConditionCombatFixture(CCApply("stun", "Stunned", worker), CCGrant("ward", worker, new ConditionStamp(T(3600)), "Stunned"), cure)); var s = World(p);
                CCDispatch(s, "stun", worker); CCDispatch(s, "ward", worker); RepairStart(s); uint rng = s.Capture().RandomState; WorldAdvance(s, 3600);
                Require(RepairJob(s).Status == RepairWorkStatus.AwaitingCheck && RepairTarget(s).Broken && s.Capture().RandomState == rng && !OrdinaryInventory.Busy(s.Capture(), worker), "Endpoint incapacity repaired, rolled or retained labor booking.");
                string path = Path.Combine(directory, "tool-repair-awaiting.bin"); new FileSaveStore().Save(path, s.Capture()); s = new Simulation(p, new FileSaveStore().Load(path), ExecutionProfile.Laboratory);
                RejectUnchanged(s, host, RepairCommand(s, CommandKind.ResumeToolRepair, RepairJob(s).Id), "RepairWorkerIncapable"); WorldAdvance(s, 1); CCDispatch(s, "cure", worker);
                var completion = RepairCommand(s, CommandKind.ResumeToolRepair, RepairJob(s).Id); WorldCommit(s, completion); byte[] bytes = Bytes(s);
                Require(RepairTarget(s).Hp == 5 && RepairJob(s).Work.Labor == T(3600) && s.Capture().RuleClock == T(3601) && s.Execute(host, completion).Outcome == Outcome.Duplicate && Bytes(s).SequenceEqual(bytes), "Deferred check added hours or repeated outcome.");
            });
            cases.Add("tool_repair_deferred_check_after_final_window_needs_no_new_labor_window", () => {
                var cure = new ConditionFixtureEvent(worker, ConditionOperation.Cure("event.cure", new ConditionStamp(T(57601)), "Stunned"));
                var p = RepairPolicy(SeedForDeath(8), conditions: new ConditionCombatFixture(CCApply("stun", "Stunned", worker), CCGrant("ward", worker, new ConditionStamp(T(57600)), "Stunned"), cure)); var s = World(p);
                CCDispatch(s, "stun", worker); CCDispatch(s, "ward", worker); WorldAdvance(s, 54000); RepairStart(s); WorldAdvance(s, 3600); WorldAdvance(s, 1); CCDispatch(s, "cure", worker); RepairControl(s, CommandKind.ResumeToolRepair);
                Require(RepairJob(s).Status == RepairWorkStatus.Success && s.Capture().RuleClock == T(57601) && RepairStock(s) == new RuleQuantity(1), "Earned repair check required a new work window or payment.");
            });
            cases.Add("tool_repair_success_preserves_calibration_fouling_and_trade_log_debts", () => {
                var facts = new SharedCraftingFixture(toolHp: 0, events: new[] { new CraftingMishapFact("calibration", 2), new CraftingMishapFact("fouling", 5), new CraftingMishapFact("log", 6) }); var s = World(RepairPolicy(SeedForDeath(8), crafting: facts));
                foreach (string id in new[] { "calibration", "fouling", "log" }) CraftEvent(s, id); RepairStart(s); WorldAdvance(s, 3600);
                Require(RepairTarget(s).Hp == 5 && s.Capture().CraftingIncidents.All(x => !x.Remedied) && CraftingRestrictions.CraftingCheckBlocked(s.Capture(), SharedCraftingFixture.ToolId)
                    && CraftingRestrictions.OrderWorkBlocked(s.Capture(), SharedCraftingFixture.StationId) && CraftingRestrictions.NewOrderBlocked(s.Capture(), worker, SharedCraftingFixture.StationId, "Alchemy"), "Structural success cleared unrelated obligations.");
            });
            cases.Add("tool_repair_spill_blocks_actual_shared_station_until_cleanup", () => {
                var s = World(RepairPolicy(SeedForDeath(8), crafting: new SharedCraftingFixture(toolHp: 0, events: new[] { new CraftingMishapFact("spill", 1) }))); CraftEvent(s, "spill");
                RejectUnchanged(s, host, RepairCommand(s), "RepairStationUnavailable"); Remedy(s, "spill"); WorldAdvance(s, 3600); RepairStart(s); WorldAdvance(s, 3600); Require(RepairTarget(s).Hp == 5, "Clean station could not support repair.");
            });
            cases.Add("tool_repair_active_target_access_pauses_research_after_validated_start", () => {
                var s = World(RepairPolicy(SeedForDeath(8), crafting: new SharedCraftingFixture(toolHp: 4), research: new SharedResearchFixture())); ResearchStart(s); WorldAdvance(s, 10); RepairStart(s);
                Require(ResearchJob(s).Status == FormulaWorkStatus.Paused && ResearchJob(s).Work.Labor == T(10) && RepairJob(s).Status == RepairWorkStatus.Working, "Repair did not atomically take over actual tool use.");
                RejectUnchanged(s, host, ResearchCommand(s, CommandKind.ResumeFormulaWork, ResearchJob(s).Id), "ResearchToolInRepair"); RepairControl(s, CommandKind.PauseToolRepair); ResearchControl(s, CommandKind.ResumeFormulaWork); WorldAdvance(s, 1);
                Require(ResearchJob(s).Work.Labor == T(11) && RepairJob(s).Work.Labor == default && RepairStock(s) == new RuleQuantity(2), "Paused claim disabled usable target or spent materials.");
                RepairControl(s, CommandKind.ResumeToolRepair); WorldAdvance(s, 3600); Require(RepairTarget(s).Hp == 5 && ResearchJob(s).Status == FormulaWorkStatus.Paused, "Completed repair auto-resumed interrupted research.");
            });
            cases.Add("tool_repair_rejected_start_does_not_interrupt_research_or_reserve_materials", () => {
                var s = World(RepairPolicy(facts: new SharedRepairFixture(trained: false), crafting: new SharedCraftingFixture(toolHp: 4), research: new SharedResearchFixture())); ResearchStart(s); WorldAdvance(s, 10);
                RejectUnchanged(s, host, RepairCommand(s), "RepairTrainingMissing"); WorldAdvance(s, 1);
                Require(ResearchJob(s).Status == FormulaWorkStatus.Working && ResearchJob(s).Work.Labor == T(11) && s.Capture().Work.AvailableAmount(SharedRepairFixture.Materials) == new RuleQuantity(2), "Rejected repair paused or charged unrelated work.");
            });
            cases.Add("tool_repair_work_windows_and_participant_pause_preserve_actual_credit", () => {
                var s = World(RepairPolicy()); HeroToWorkshop(s); WorldAdvance(s, 27995); RepairStart(s, hero); WorldAdvance(s, 900);
                Require(RepairJob(s).Status == RepairWorkStatus.Paused && RepairJob(s).Work.Labor == T(800), "Repair crossed unscheduled work window."); RepairControl(s, CommandKind.ResumeToolRepair, hero); WorldAdvance(s, 10); BeginEncounter(s);
                Require(RepairJob(s).Status == RepairWorkStatus.Paused && RepairJob(s).Work.Labor == T(810), "Combat participant kept repairing.");
                RejectUnchanged(s, host, RepairCommand(s, CommandKind.ResumeToolRepair, RepairJob(s).Id, hero), "RepairParticipantInCombat");
            });
            cases.Add("tool_repair_remote_labor_continues_during_actual_tactical_slots", () => {
                var s = World(RepairPolicy()); RepairStart(s); BeginEncounter(s); ConnectedEnd(s); ConnectedEnd(s);
                Require(RepairJob(s).Work.Labor == T(6) && RepairStock(s) == new RuleQuantity(1) && RepairTarget(s).Broken, "Tactical decisions advanced time or remote labor stopped.");
            });
            cases.Add("tool_repair_canonical_restore_rejects_forged_hp_and_result", () => {
                var p = RepairPolicy(SeedForDeath(8)); var s = World(p); RepairStart(s); WorldAdvance(s, 10); var bad = s.Capture(); bad.Structures = bad.Structures.Select(x => x.Id == SharedCraftingFixture.ToolId ? x.WithHp(5) : x).ToArray();
                Throws<ArgumentException>(() => new Simulation(p, bad, ExecutionProfile.Laboratory)); WorldAdvance(s, 3590); bad = s.Capture(); var job = bad.RepairWork[0];
                bad.RepairWork[0] = new RepairWorkRecord(job.Id, job.WorkerId, job.TargetId, job.ToolkitId, job.MaterialsId, RepairWorkStatus.Failure, job.StartedAt, job.UpdatedAt, job.Work, 7, 0, 7);
                Throws<ArgumentException>(() => new Simulation(p, bad, ExecutionProfile.Laboratory));
            });
        }
    }
}
#endif
