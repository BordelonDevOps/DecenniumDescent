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
        private const string FormulaCompanion = TestOnlyPolicy.CompanionId;

        private static Command FormulaControl(Simulation sim, CommandKind kind)
            => ResearchCommand(sim, kind, ResearchJob(sim).Id);

        private static void FormulaDenial(Simulation sim, Authority host, Command command, string code)
        {
            byte[] before = Bytes(sim);
            var query = sim.QueryCommand(host, command);
            Require(query.Supported && !query.Admissible && query.Code == code,
                "Expected formula query " + code + ", got " + query.Code + ".");
            Require(Bytes(sim).SequenceEqual(before), "Formula query changed the live state.");
            RejectUnchanged(sim, host, command, code);
        }

        private static Command FormulaOption(Simulation sim, Authority host, CommandKind kind)
        {
            byte[] before = Bytes(sim);
            var result = sim.DiscoverCommands(host, FormulaCompanion).Single(x => x.Command.Kind == kind);
            Require(result.Query.Admissible && Bytes(sim).SequenceEqual(before),
                "Formula discovery changed live state or disagreed with admission.");
            return result.Command;
        }

        private static Simulation SaveConnectedResearch(Simulation sim, TestOnlySharedWorldPolicy policy, string directory, string name)
            => SaveBill(sim, policy, directory, "mgt09-connected-research-" + name);

        private static void AddConnectedFormulaResearchCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("mgt09_connected_formula_research_real_work_stock_and_later_combat_replay", () =>
            {
                var policy = ConnectedObservationPolicy().EnableConnectedFormulaResearch();
                var sim = LaterPrepared(policy);
                PlanWalk(sim, -1, 0, FormulaCompanion);
                var atSite = sim.Capture();
                Require(atSite.WireSchemaVersion == 93 && atSite.SchemaVersion == 90 && atSite.RuleClock == T(11584)
                    && Body(sim, FormulaCompanion).X == 3 && Body(sim, FormulaCompanion).Y == 3
                    && atSite.LaterEncounter.FirstExit.ClosedAt == T(15) && atSite.HavenSales.Single().PaymentCopper == 2
                    && atSite.HavenMealPurchases.Length == 1 && atSite.ExpeditionBills.Length == 1
                    && atSite.CharterAttempt.Outcome == CharterAttemptOutcome.ReturnedComplete
                    && atSite.Trades.Single(x => x.WorkerId == FormulaCompanion && x.TradeId == "Alchemy").Level == 5
                    && atSite.Structures.Any(x => x.Id == SharedCraftingFixture.ToolId && x.CustodianId == FormulaCompanion && !x.Broken)
                    && !FormulaResearchRules.Knows(atSite, FormulaCompanion, SharedResearchFixture.Recipe),
                    "The qualified companion must reach the actual workshop after the genuine expedition.");
                var oldStock = atSite.Work.Lots.Where(x => x.Id.StartsWith("manufacture.", StringComparison.Ordinal)).ToArray();
                Require(oldStock.Length == 9 && policy.BloodUnprotectedAge(atSite, 0) == atSite.RuleClock,
                    "The original finite stock and origin were not selected from initialization.");
                SaveConnectedResearch(sim, policy, directory, "workshop-unknown");
                FormulaDenial(sim, host, ManufactureCommand(sim), "ManufacturingCredentialMissing");

                var start = FormulaOption(sim, host, CommandKind.StartFormulaResearch);
                LaterCommit(sim, start);
                var started = ResearchJob(sim);
                Require(sim.Execute(host, start).Outcome == Outcome.Duplicate && sim.Capture().FormulaWork.Length == 1,
                    "Duplicate research opened a second project.");
                FormulaDenial(sim, host, new Command("research.move-while-working", FormulaCompanion, sim.Capture().Revision,
                    CommandKind.BeginWorldStep, "walk", 0, -1), "WorkerBusy");
                WorldAdvance(sim, 17216);
                var paused = sim.Capture();
                var pausedJob = ResearchJob(sim);
                Require(paused.RuleClock == T(28800) && pausedJob.Id == started.Id
                    && pausedJob.Status == FormulaWorkStatus.Paused && pausedJob.Work.Labor == T(17216)
                    && paused.Work.WorkerIntervals.Single(x => x.JobId == started.Id).End == paused.RuleClock
                    && paused.RandomState == atSite.RandomState, "The first actual work window did not close with retained labor.");
                var restored = SaveConnectedResearch(sim, policy, directory, "first-window-paused");
                foreach (var run in new[] { sim, restored }) {
                    LaterCommit(run, FormulaOption(run, host, CommandKind.ResumeFormulaWork));
                    WorldAdvance(run, 11584);
                    var learned = run.Capture();
                    var job = ResearchJob(run);
                    var liveDraw = PlaytestDice.RollD20(paused.RandomState);
                    var actor = CharacterStateFacts.ForActor(learned, FormulaCompanion);
                    int modifier = actor.Rules.AbilityModifier(CharacterAbility.Intelligence) + actor.Rules.ProficiencyBonus
                        + actor.InjuryPenalty(CharacterAbility.Intelligence, toolCheck: true);
                    var work = learned.Work.WorkerIntervals.Where(x => x.JobId == started.Id).OrderBy(x => x.Start).ToArray();
                    Require(learned.RuleClock == T(40384) && job.Id == started.Id && job.Work.Labor == T(28800)
                        && job.Status == FormulaWorkStatus.Success && job.Natural == liveDraw.Natural
                        && FormulaResearchRules.Succeeds(job.Natural, modifier, 8) && learned.RandomState == liveDraw.NextRandomState
                        && work.Length == 2 && work[0].Start == T(11584) && work[0].End == T(28800)
                        && work[1].Start == T(28800) && work[1].End == T(40384)
                        && FormulaResearchRules.Knows(learned, FormulaCompanion, SharedResearchFixture.Recipe),
                        "The actual shared check must grant knowledge once after exactly eight eligible hours.");
                    FormulaDenial(run, host, ResearchCommand(run), "FormulaAlreadyKnown");
                    FormulaDenial(run, host, ManufactureCommand(run), "ManufacturingIngredientSpoiled");
                    FormulaDenial(run, host, ManufactureCommand(run, x: 1), "ManufacturingIngredientSpoiled");
                    Require(learned.ManufacturingOrders.Length == 0 && learned.AlchemyDoses.Length == 0
                        && learned.Trades.Single().Xp == atSite.Trades.Single().Xp
                        && policy.BloodUnprotectedAge(learned, 0) == learned.RuleClock
                        && learned.Work.Lots.Where(x => x.Id.StartsWith("manufacture.", StringComparison.Ordinal))
                            .Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))
                            .SequenceEqual(oldStock.Select(x => (x.Id, x.Amount, x.LocationId, x.CustodianId))),
                        "Research or the eligibility checks changed the original stock, orders, output, or trade XP.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(restored)), "Research after the pause diverged on restore.");
                SaveConnectedResearch(sim, policy, directory, "learned");
                foreach (var run in new[] { sim, restored }) {
                    PlanWalk(run, 0, -1, FormulaCompanion);
                    for (int i = 0; i < 3; i++) PlanWalk(run, 0, -1);
                    WorldAdvance(run, 2);
                    FinishPaidHide(run);
                    LaterCommit(run, ExplorationSearchCommand(run));
                    SearchAdvance(run, 18);
                    var observation = run.Capture();
                    Require(observation.ExplorationHide.Attempts.Single().End != null
                        && observation.ExplorationSearch.Attempts.Single().End != null
                        && ResearchJob(run).Id == started.Id, "The selected host lost its live ordinary Hide or Search.");
                    if (run == sim) SaveConnectedResearch(sim, policy, directory, "after-observation");
                    ReturnToConnectedApproach(run);
                    var beforeEntry = run.Capture();
                    var entered = EnterLater(run);
                    Require(entered.Draws[0].RandomBefore == beforeEntry.RandomState
                        && run.Capture().SurpriseEntry.Binding.Outcome == SurpriseAwareness.Warned
                        && ResearchJob(run).Id == started.Id, "Actual later combat did not carry the acquired formula and shared RNG.");
                    if (run == sim) SaveConnectedResearch(sim, policy, directory, "later-entry");
                    FinishLaterFight(run, false);
                }
                Require(Bytes(sim).SequenceEqual(Bytes(restored)), "Actual later combat diverged after restoring the research.");
                var postCombat = SaveConnectedResearch(sim, policy, directory, "post-combat");
                foreach (var run in new[] { sim, postCombat }) {
                    PlanWalk(run, 1, 0);
                    var continued = run.Capture();
                    Require(!continued.InventoryCombat && continued.ClosedEncounters.Length == 2
                        && Body(run).X == 1 && ResearchJob(run).Id == started.Id
                        && FormulaResearchRules.Knows(continued, FormulaCompanion, SharedResearchFixture.Recipe)
                        && continued.CharterAttempt.Outcome == CharterAttemptOutcome.ReturnedComplete,
                        "The actual acquisition did not survive ordinary continuation after combat.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(postCombat)), "Ordinary continuation after combat diverged on restore.");
                SaveConnectedResearch(sim, policy, directory, "continued");
                File.WriteAllLines(Path.Combine(directory, "mgt09-connected-research-gameplay.tsv"), new[] {
                    "worksite\t" + atSite.RuleClock + "\t" + atSite.Revision + "\t" + atSite.RandomState,
                    "paused\t" + paused.RuleClock + "\t" + pausedJob.Id + "\t" + pausedJob.Work.Labor,
                    "learned\t" + ResearchJob(sim).UpdatedAt + "\t" + ResearchJob(sim).Natural + "\t" + ResearchJob(sim).Work.Labor,
                    "continued\t" + sim.Capture().RuleClock + "\t" + sim.Capture().Revision
                });
            });

            cases.Add("mgt09_connected_formula_research_scope_access_and_profile_compatibility", () =>
            {
                var oldPolicy = ConnectedObservationPolicy();
                var policy = ConnectedObservationPolicy().EnableConnectedFormulaResearch();
                var original = oldPolicy.Initial();
                var initial = policy.Initial();
                var codec = new SnapshotCodec();
                Require(initial.ContentFingerprint != original.ContentFingerprint
                    && ConnectedExplorationObservation.IsSelected(initial) && initial.WireSchemaVersion == original.WireSchemaVersion,
                    "Research selection lost connected observation recognition or changed the wire.");
                var oldBytes = codec.Encode(original);
                var newBytes = codec.Encode(initial);
                Throws<ArgumentException>(() => new Simulation(policy, codec.Decode(oldBytes), ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(oldPolicy, codec.Decode(newBytes), ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => policy.EnableConnectedFormulaResearch());
                Throws<InvalidOperationException>(() => oldPolicy.EnableConnectedFormulaResearch());
                Throws<InvalidOperationException>(() => LaterPolicy().EnableConnectedFormulaResearch());

                var early = new Simulation(policy, initial, ExecutionProfile.Laboratory);
                FormulaDenial(early, host, ResearchCommand(early), "ConnectedResearchStageClosed");
                var sim = LaterPrepared(policy);
                WorldStep(sim, -1, 0, actor: FormulaCompanion);
                FormulaDenial(sim, host, ResearchCommand(sim), "ResearchStationOutOfReach");
                WorldAdvance(sim, 6);
                FormulaDenial(sim, host, ResearchCommand(sim, worker: PlanHero), "ResearchCredentialMissing");
                FormulaDenial(sim, host, ResearchCommand(sim, target: SharedResearchFixture.FreshEvidence), "ConnectedFormulaOperationNotSelected");
                FormulaDenial(sim, host, ResearchCommand(sim, method: 1), "ConnectedFormulaOperationNotSelected");
                FormulaDenial(sim, host, ResearchCommand(sim, recipe: SharedResearchFixture.Recipe14), "ConnectedFormulaOperationNotSelected");
                FormulaDenial(sim, host, ResearchCommand(sim, CommandKind.StartFormulaCopy), "ConnectedFormulaOperationNotSelected");
                Require(sim.DiscoverCommands(host, FormulaCompanion).Count(x => x.Command.Kind == CommandKind.StartFormulaResearch
                    || x.Command.Kind == CommandKind.StartFormulaCopy) == 1, "Discovery exposed another evidence, method or copy.");

                uint rng = sim.Capture().RandomState;
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.StartFormulaResearch));
                WorldAdvance(sim, 2);
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.PauseFormulaWork));
                var paused = ResearchJob(sim);
                PlanWalk(sim, 0, -1, FormulaCompanion);
                PlanWalk(sim, 0, -1, FormulaCompanion);
                FormulaDenial(sim, host, FormulaControl(sim, CommandKind.ResumeFormulaWork), "ResearchStationOutOfReach");
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.CancelFormulaWork));
                PlanWalk(sim, 0, 1, FormulaCompanion);
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.StartFormulaResearch));
                var after = sim.Capture();
                Require(after.RandomState == rng && after.FormulaWork.Length == 2
                    && after.FormulaWork[0].Status == FormulaWorkStatus.Cancelled && after.FormulaWork[0].Work.Labor == T(2)
                    && after.FormulaWork[0].Id == paused.Id && ResearchJob(sim).Work.Labor == default
                    && !FormulaResearchRules.Knows(after, FormulaCompanion, SharedResearchFixture.Recipe),
                    "Paused time or a cancelled project leaked labor or knowledge into a new project.");
                SaveConnectedResearch(sim, policy, directory, "scope-cancel-and-new-project");
            });

            cases.Add("mgt09_connected_formula_research_endpoint_incapacity_defers_one_check", () =>
            {
                var stun = CCApply("research-stun", "Stunned", FormulaCompanion, at: new ConditionStamp(T(28800)));
                var ward = new ConditionFixtureEvent(FormulaCompanion, ConditionOperation.Grant("event.research-ward",
                    new ConditionStamp(T(28800)), new ConditionImmunityData("research-ward", "owner", "ward",
                        new[] { "Stunned" }, new ConditionStamp(T(57600)), "ward-end")));
                var cure = new ConditionFixtureEvent(FormulaCompanion, ConditionOperation.Cure("event.research-cure",
                    new ConditionStamp(T(57601)), "Stunned"));
                var policy = ConnectedObservationPolicy(stun, ward, cure).EnableConnectedFormulaResearch();
                var sim = LaterPrepared(policy);
                PlanWalk(sim, -1, 0, FormulaCompanion);
                WorldAdvance(sim, 17216);
                LaterCommit(sim, CCCommand(sim, "research-stun", FormulaCompanion));
                FormulaDenial(sim, host, ResearchCommand(sim), "ResearchWorkerIncapable");
                LaterCommit(sim, CCCommand(sim, "research-ward", FormulaCompanion));
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.StartFormulaResearch));
                uint rng = sim.Capture().RandomState;
                WorldAdvance(sim, 28800);
                Require(ResearchJob(sim).Status == FormulaWorkStatus.AwaitingCheck && ResearchJob(sim).Work.Complete
                    && sim.Capture().RuleClock == T(57600) && sim.Capture().RandomState == rng,
                    "The due condition expiry must defer the check after retaining the final labor.");
                FormulaDenial(sim, host, FormulaControl(sim, CommandKind.ResumeFormulaWork), "ResearchWorkerIncapable");
                var restored = SaveConnectedResearch(sim, policy, directory, "awaiting-check");
                foreach (var run in new[] { sim, restored }) {
                    WorldAdvance(run, 1);
                    LaterCommit(run, CCCommand(run, "research-cure", FormulaCompanion));
                    Require(ResearchJob(run).Status == FormulaWorkStatus.AwaitingCheck && run.Capture().RandomState == rng,
                        "Restored eligibility drew RNG before the explicit check.");
                    var check = FormulaOption(run, host, CommandKind.ResumeFormulaWork);
                    LaterCommit(run, check);
                    var after = run.Capture();
                    var rolled = PlaytestDice.RollD20(rng);
                    Require(ResearchJob(run).Status == FormulaWorkStatus.Success && ResearchJob(run).Natural == rolled.Natural
                        && ResearchJob(run).Work.Labor == T(28800) && after.RuleClock == T(57601)
                        && after.RandomState == rolled.NextRandomState && run.Execute(host, check).Outcome == Outcome.Duplicate,
                        "The deferred check did not resolve once after the last window without adding labor.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(restored)), "Deferred check changed under replay.");
                SaveConnectedResearch(sim, policy, directory, "deferred-check-completed");
            });

            cases.Add("mgt09_connected_formula_research_remote_work_and_actual_reinforced_roster", () =>
            {
                var policy = ConnectedObservationPolicy().EnableConnectedFormulaResearch();
                var sim = LaterPrepared(policy);
                PlanWalk(sim, -1, 0, FormulaCompanion);
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.StartFormulaResearch));
                var staged = SaveConnectedResearch(sim, policy, directory, "remote-before-entry");
                var entry = EnterLater(sim);
                EndReinforcementTurn(sim);
                var remote = sim.Capture();
                var remoteJob = ResearchJob(sim);
                Require(remote.InventoryCombat && !WorldTiming.ForEncounter(remote).Order.Contains(FormulaCompanion)
                    && remoteJob.Status == FormulaWorkStatus.Working
                    && remoteJob.Work.Labor == T(remote.RuleClock.Numerator - remoteJob.StartedAt.Numerator * remote.RuleClock.Denominator,
                        remote.RuleClock.Denominator)
                    && remoteJob.UpdatedAt >= entry.Epoch.Origin,
                    "Compatible remote work did not use the shared elapsed time exactly once.");
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.PauseFormulaWork));
                FormulaDenial(sim, host, FormulaControl(sim, CommandKind.ResumeFormulaWork), "ConnectedResearchStageClosed");
                SaveConnectedResearch(sim, policy, directory, "paused-remotely-in-combat");

                WorldAdvance(staged, 2);
                LaterCommit(staged, FormulaOption(staged, host, CommandKind.PauseFormulaWork));
                var paused = ResearchJob(staged);
                StageReinforcingCompanion(staged);
                EnterLater(staged);
                LaterCommit(staged, ReinforcementCommand(staged));
                EndReinforcementTurn(staged);
                var prior = SaveConnectedResearch(staged, policy, directory, "before-reinforcement-admission");
                foreach (var run in new[] { staged, prior }) {
                    EndReinforcementTurn(run);
                    var admitted = run.Capture();
                    var phase = admitted.Reinforcement.Admission.Phase;
                    Require(admitted.InventoryCombat && !admitted.WorldSchedule.Order.Contains(FormulaCompanion)
                        && WorldTiming.ForEncounter(admitted).Id == phase.Epoch.Id
                        && WorldTiming.ForActor(admitted, FormulaCompanion).Id == phase.Epoch.Id
                        && !admitted.WorldActivityIntervals.Any(x => x.ActorId == FormulaCompanion)
                        && ResearchJob(run).Id == paused.Id && ResearchJob(run).Work.Labor == T(2),
                        "The actual new roster did not retain the paused project and retire the off-calendar row.");
                    FormulaDenial(run, host, FormulaControl(run, CommandKind.ResumeFormulaWork), "ResearchParticipantInCombat");
                    LaterCommit(run, FormulaOption(run, host, CommandKind.CancelFormulaWork));
                }
                Require(Bytes(staged).SequenceEqual(Bytes(prior)), "Research history changed on replay across actual admission.");
                SaveConnectedResearch(staged, policy, directory, "after-reinforcement-admission");
            });
        }
    }
}
#endif
