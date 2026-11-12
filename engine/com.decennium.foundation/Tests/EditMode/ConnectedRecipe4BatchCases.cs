#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string BatchWorker = ConnectedBloodSpecimen.Worker;

        private static TestOnlySharedWorldPolicy BatchPolicy(ConditionFixtureEvent[] events = null, uint? seed = null)
            => ReengagementPolicy(seed, events == null ? null : new ConditionCombatFixture(events))
                .EnableSurpriseAwareEntry(SurpriseAwareness.Warned).EnableConnectedExplorationObservation()
                .EnableConnectedFormulaResearch().EnableConnectedBloodSpecimen().EnableConnectedRecipe4Batch();

        private static TestOnlySharedWorldPolicy BatchDeferredPolicy()
        {
            var admission = new ConditionStamp(T(42248));
            var stun = CCApply("batch-stun", "Stunned", BatchWorker, at: admission);
            var ward = new ConditionFixtureEvent(BatchWorker, ConditionOperation.Grant("event.batch-ward", admission,
                new ConditionImmunityData("batch-ward", "owner", "ward", new[] { "Stunned" },
                    new ConditionStamp(T(56648)), "ward-end")));
            var cure = new ConditionFixtureEvent(BatchWorker, ConditionOperation.Cure("event.batch-cure",
                new ConditionStamp(T(56649)), "Stunned"));
            return BatchPolicy(new[] { stun, ward, cure });
        }

        private static TestOnlySharedWorldPolicy BatchInjuryPolicy()
        {
            var occurrence = new CraftingMishapFact(TestOnlySharedWorldPolicy.Recipe4InjuryWitnessId, 4,
                at: TestOnlySharedWorldPolicy.Recipe4InjuryWitnessAt);
            var crafting = new SharedCraftingFixture(companionHp: 1, events: new[] { occurrence });
            return MakeLaterPolicy(350794, null, Array.Empty<TacticalTerrainCell>(), crafting)
                .EnableCompanionReinforcement(new TestOnlyReinforcementProfile())
                .EnableLivingOpponentRetreat(new TestOnlyLivingOpponentRetreatProfile())
                .EnablePhysicalReengagement(true, true).EnableSurpriseAwareEntry(SurpriseAwareness.Warned)
                .EnableConnectedExplorationObservation().EnableConnectedRecipe4InjuryWitness();
        }

        private static Simulation BatchReady(TestOnlySharedWorldPolicy policy, int preliminaryResearch = 0,
            Action<Simulation> beforePreparation = null)
        {
            var host = LaterHost();
            var sim = LaterPrepared(policy);
            beforePreparation?.Invoke(sim);
            if (preliminaryResearch > 0) {
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.StartFormulaResearch));
                WorldAdvance(sim, preliminaryResearch);
                LaterCommit(sim, FormulaOption(sim, host, CommandKind.PauseFormulaWork));
                WorldAdvance(sim, 6);
            }
            LaterCommit(sim, BloodVesselCommand(sim, CommandKind.OpenPortableContainer));
            LaterCommit(sim, BloodTreatmentCommand(sim));
            WorldAdvance(sim, 1800);
            var treated = BloodTreatment(sim);
            Require(treated.Status == HarvestPreservationTreatmentStatus.Success,
                "The selected connected batch route did not actually preserve its specimen.");

            LaterCommit(sim, FormulaOption(sim, host, preliminaryResearch == 0
                ? CommandKind.StartFormulaResearch : CommandKind.ResumeFormulaWork));
            AdvanceBloodTo(sim, T(28800));
            Require(ResearchJob(sim).Status == FormulaWorkStatus.Paused, "The first real research Watch did not pause.");
            LaterCommit(sim, FormulaOption(sim, host, CommandKind.ResumeFormulaWork));
            var remaining = ResearchJob(sim).Work.Remaining;
            WorldAdvance(sim, checked((int)remaining.Numerator), checked((int)remaining.Denominator));
            Require(FormulaResearchRules.Knows(sim.Capture(), BatchWorker, ConnectedRecipe4Batch.RecipeId),
                "The connected batch cannot proceed without the actual learned formula.");
            LaterCommit(sim, BloodVesselCommand(sim, CommandKind.HandlePortableEquipment, HandlingKind.Pickup));
            PlanWalk(sim, -1, 0, BatchWorker);
            LaterCommit(sim, BloodVesselCommand(sim, CommandKind.HandlePortableEquipment, HandlingKind.Drop));
            LaterCommit(sim, BloodVesselCommand(sim, CommandKind.OpenPortableContainer));
            WorldAdvance(sim, 60);
            return sim;
        }

        private static ManufacturingOrderRecord BatchOrder(Simulation sim)
            => sim.Capture().ManufacturingOrders.Single();

        private static Command BatchCommand(Simulation sim, CommandKind kind, int x = 0, int y = 0, string actor = BatchWorker)
        {
            var state = sim.Capture();
            return new Command("recipe4.batch." + state.Revision, actor, state.Revision, kind,
                kind == CommandKind.StartManufacturing ? ConnectedRecipe4Batch.RecipeId : state.ConnectedBatch.OrderId, x, y);
        }

        private static Simulation SaveBatch(Simulation run, TestOnlySharedWorldPolicy policy, string directory, string stage)
            => SaveBill(run, policy, directory, "mgt04-connected-batch-" + stage);

        private static ResourceReservation BatchClaim(Simulation run, string suffix)
        {
            var state = run.Capture();
            string order = state.ConnectedBatch.OrderId;
            return state.Work.Reservations.Single(x => x.JobId == order && x.Id == order + "." + suffix);
        }

        private static ManufacturingOrderRecord ChangeBatchEvidence(ManufacturingOrderRecord order, RuleTime? stabilization, int natural)
            => new ManufacturingOrderRecord(order.Id, order.WorkerId, order.RecipeId, order.MaterialSet, order.ExtraVials,
                order.TakeTen, order.Status, order.Work, order.StartedAt, order.UpdatedAt, stabilization,
                order.First, order.Second, natural, order.Quality, order.Choice, order.RetainedCatalyst, order.Mishap,
                order.XpAward, order.FindingId, order.MishapIncidentId);

        private static void MoveToBatchBench(Simulation sim, bool acceptOpportunity)
        {
            LaterStance(sim, CombatStance.Aggressive);
            LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 1, y: 3));
            LaterCommit(sim, Tac(sim, CommandKind.TacticalStep, x: 2, y: 3));
            Require(TestOnlyClubAttackPolicy.PendingMove(sim.Capture()) != null,
                "The actual route out of the defender's reach did not create its opportunity.");
            LaterCommit(sim, Opportunity(sim, acceptOpportunity, LaterClub));
        }

        private static void AddConnectedRecipe4BatchCases(Dictionary<string, Action> cases, string directory)
        {
            var host = LaterHost();
            cases.Add("mgt04_connected_recipe4_real_charge_stabilization_and_native_output", () =>
            {
                var policy = BatchPolicy();
                var codec = new SnapshotCodec();
                var sim = BatchReady(policy, beforePreparation: run =>
                    FormulaDenial(run, host, BatchCommand(run, CommandKind.StartManufacturing), "ManufacturingCredentialMissing"));
                var before = sim.Capture();
                var specimen = before.BloodSpecimen;
                Require(before.WireSchemaVersion == 95 && before.SchemaVersion == 90
                    && before.RuleClock == T(42248) && before.LaterEncounter.FirstExit.ClosedAt == T(15)
                    && before.HavenSales.Single().PaymentCopper == 2
                    && BloodAge(sim).UnprotectedAge == T(13379) && before.ManufacturingOrders.Length == 0,
                    "The actual exploration, trade, treatment and research route did not reach its accepted batch cutoff.");
                FormulaDenial(sim, host, BatchCommand(sim, CommandKind.StartManufacturing, x: 1), "ConnectedRecipe4RequestNotSelected");
                FormulaDenial(sim, host, BatchCommand(sim, CommandKind.StartManufacturing, y: 3), "ConnectedRecipe4RequestNotSelected");
                var withoutStock = new Authority("TEST_ONLY.batch-no-inventory", new[] { BatchWorker }, true, true);
                FormulaDenial(sim, withoutStock, BatchCommand(sim, CommandKind.StartManufacturing), "InventoryNotAuthorized");
                var manipulate = new Command("recipe4.apparatus.open", BatchWorker, before.Revision,
                    CommandKind.OpenPortableContainer, before.ConnectedBatch.ApparatusId);
                FormulaDenial(sim, host, manipulate, "ConnectedRecipe4ApparatusIsFixed");
                Require(policy.BloodUnprotectedAge(before, "recipe-4", 0) >= T(28800)
                    && policy.BloodUnprotectedAge(before, "recipe-4", 1) >= T(28800), "Original blood slots did not retain independent aging.");
                var option = sim.DiscoverCommands(host, BatchWorker)
                    .Single(x => x.Command.Kind == CommandKind.StartManufacturing && x.Command.Y == 2);
                Require(option.Query.Admissible && option.Query.Costs.Any(x => x.ResourceId == specimen.LotId && x.Amount == 1)
                    && option.Query.Costs.Any(x => x.Kind == "work-seconds" && x.Amount == 14400),
                    "Discovery omitted the exact material claim or active work cost.");
                byte[] beforeQuery = Bytes(sim);
                Require(sim.QueryCommand(host, option.Command).Admissible && Bytes(sim).SequenceEqual(beforeQuery),
                    "The executable start query charged the apparatus.");
                LaterCommit(sim, option.Command);
                var charged = sim.Capture();
                Require(charged.ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Charged
                    && charged.Work.Lots.Single(x => x.Id == specimen.LotId).LocationId == charged.ConnectedBatch.ApparatusId
                    && charged.Work.Lots.Single(x => x.Id == specimen.LotId).Amount == Q(1)
                    && charged.PortableEquipment.All(x => x.Id != specimen.LotId)
                    && charged.PortableEquipment.Single(x => x.Id == ConnectedBloodSpecimen.Packing).ParentId == specimen.VesselId
                    && BatchClaim(sim, "component3").LotId == specimen.LotId && BatchClaim(sim, "component3").RemainingAmount == Q(1)
                    && BatchClaim(sim, "packaging").RemainingAmount == Q(2)
                    && BatchOrder(sim).Work.Labor == default && !BatchOrder(sim).StabilizedAt.HasValue
                    && charged.RandomState == before.RandomState,
                    "Start did not atomically charge the original specimen and book exact unspent claims.");
                Require(sim.Execute(host, option.Command).Outcome == Outcome.Duplicate,
                    "Duplicate loading attempted another material claim.");
                var stale = new Command("recipe4.stale", BatchWorker, before.Revision,
                    CommandKind.StartManufacturing, ConnectedRecipe4Batch.RecipeId);
                var chargedBytes = Bytes(sim);
                Require(!sim.QueryCommand(host, stale).Admissible && sim.Execute(host, stale).Outcome != Outcome.Committed
                    && Bytes(sim).SequenceEqual(chargedBytes), "A stale declaration changed the charged batch.");
                var displaced = charged.Copy();
                displaced.Work = new WorkLedger(displaced.Work.Lots.Select(x => x.Id == specimen.LotId
                    ? new ResourceLot(x.Id, x.UnitId, x.Amount, specimen.VesselId, x.CustodianId) : x),
                    displaced.Work.WorkerIntervals, displaced.Work.Reservations);
                Throws<ArgumentException>(() => codec.Encode(displaced));
                var substituted = charged.Copy();
                string claimId = BatchClaim(sim, "component3").Id;
                substituted.Work = new WorkLedger(substituted.Work.Lots, substituted.Work.WorkerIntervals,
                    substituted.Work.Reservations.Select(x => x.Id == claimId
                        ? new ResourceReservation(x.Id, x.JobId, SharedManufacturingFixture.Lot(0, 3), x.Amount) : x));
                Throws<ArgumentException>(() => codec.Encode(substituted));
                FormulaDenial(sim, host, BloodVesselCommand(sim, CommandKind.ClosePortableContainer), "ConnectedRecipe4ReturnVesselClaimed");
                FormulaDenial(sim, host, LaterApproach(sim), "HarvestPreservationOpenLifecycleTacticalUnsupported");
                SaveBatch(sim, policy, directory, "charged");
                WorldAdvance(sim, 899);
                Require(BatchOrder(sim).Work.Partial == T(899) && !BatchOrder(sim).StabilizedAt.HasValue
                    && BloodAge(sim).UnprotectedAge == T(14278), "Partial work illegally suspended specimen aging.");
                var replay = SaveBatch(sim, policy, directory, "partial");
                foreach (var run in new[] { sim, replay }) {
                    WorldAdvance(run, 1);
                    Require(BatchOrder(run).StabilizedAt == T(43148) && BloodAge(run).UnprotectedAge == T(14279)
                        && run.Capture().RandomState == before.RandomState, "The first phase did not actually earn stabilization.");
                    if (run == sim) {
                        var forged = run.Capture();
                        forged.ManufacturingOrders = new[] { ChangeBatchEvidence(BatchOrder(run), T(43147), 0) };
                        Throws<ArgumentException>(() => codec.Encode(forged));
                        SaveBatch(run, policy, directory, "stabilized");
                    }
                    WorldAdvance(run, 13500);
                    var check = BatchOrder(run);
                    Require(check.Work.Labor == T(14400) && check.Status == ManufacturingStatus.AwaitingChoice
                        && check.Quality == CraftQuality.Exceptional && check.Natural == 15
                        && run.Capture().RuleClock == T(56648) && BloodAge(run).UnprotectedAge == T(14279)
                        && run.Capture().AlchemyDoses.Length == 0, "The live native check or pending choice changed.");
                    if (run == sim) {
                        var forged = run.Capture();
                        forged.ManufacturingOrders = new[] { ChangeBatchEvidence(check, check.StabilizedAt, check.Natural + 1) };
                        Throws<ArgumentException>(() => codec.Encode(forged));
                        SaveBatch(run, policy, directory, "quality-choice");
                    }
                    FormulaDenial(run, host, BatchCommand(run, CommandKind.ResolveManufacturingQuality,
                        (int)CraftQualityChoice.FullYield, y: 4), "InvalidRetainedCatalyst");
                    var choice = BatchCommand(run, CommandKind.ResolveManufacturingQuality, (int)CraftQualityChoice.FullYield);
                    LaterCommit(run, choice);
                    var settled = run.Capture();
                    Require(settled.ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Consumed
                        && BatchClaim(run, "component3").ConsumedAmount == Q(1)
                        && BatchClaim(run, "packaging").ConsumedAmount == Q(1) && BatchClaim(run, "packaging").ReleasedAmount == Q(1)
                        && settled.AlchemyDoses.Length == 6 && settled.AlchemyDoses.All(x => x.OrderId == check.Id
                            && x.OwnerId == BatchWorker && x.CustodianId == BatchWorker && x.MassPounds == new RuleQuantity(1, 5))
                        && BatchOrder(run).XpAward == 4 && settled.Trades.Single().Xp == 4
                        && settled.Work.Lots.Single(x => x.Id == specimen.LotId).Amount == default,
                        "Native settlement did not consume one specimen, release an unused vial and produce six finite doses.");
                    var bytes = Bytes(run);
                    Require(run.Execute(host, choice).Outcome == Outcome.Duplicate && Bytes(run).SequenceEqual(bytes),
                        "Duplicate quality choice changed terminal resources or output.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "The charged order diverged across disk restoration and replay.");
                var forgedOutput = sim.Capture();
                var dose = forgedOutput.AlchemyDoses[0];
                forgedOutput.AlchemyDoses[0] = new AlchemyDoseRecord(dose.Id, dose.OrderId, dose.RecipeId, dose.MakerId,
                    dose.OwnerId, dose.CustodianId, "forged.workshop", dose.CreatedAt, dose.MaximumHp, dose.Hp);
                Throws<ArgumentException>(() => codec.Encode(forgedOutput));
                var forgedSettlement = sim.Capture();
                var batch = forgedSettlement.ConnectedBatch;
                forgedSettlement.ConnectedBatch = new ConnectedRecipe4Batch(batch.ApparatusId, batch.FitId, batch.ReturnVesselId,
                    batch.OrderId, batch.ChargeRevision, batch.SettlementRevision, ConnectedSpecimenDisposition.Returned);
                Throws<ArgumentException>(() => codec.Encode(forgedSettlement));
                SaveBatch(sim, policy, directory, "settled");
                foreach (var run in new[] { sim, replay }) {
                    FormulaDenial(run, host, LaterApproach(run), "HarvestPreservationOpenLifecycleTacticalUnsupported");
                    LaterCommit(run, BloodVesselCommand(run, CommandKind.ClosePortableContainer));
                    EnterLater(run);
                    string doseId = run.Capture().AlchemyDoses[0].Id;
                    FormulaDenial(run, host, DoseCommand(run, doseId), "AlchemyDoseOutOfReach");
                    if (run == sim) {
                        var fullHp = SaveBatch(run, policy, directory, "later-entry");
                        MoveToBatchBench(fullHp, false);
                        var fullDose = DoseCommand(fullHp, doseId);
                        LaterCommit(fullHp, fullDose);
                        var spentAtFullHp = fullHp.Capture().AlchemyDoses[0];
                        Require(spentAtFullHp.Spent && spentAtFullHp.ActualHealing == 0
                            && spentAtFullHp.PotentialHealing == spentAtFullHp.FirstD4 + spentAtFullHp.SecondD4 + 2
                            && fullHp.Capture().WorldIntervals.Single(x => x.ActorId == PlanHero).ActionSpent,
                            "Legal use at full HP incorrectly refunded the finite dose or Action.");
                    }
                    MoveToBatchBench(run, true);
                    var wounded = run.Capture();
                    long hpBefore = wounded.Lives.Single(x => x.ActorId == PlanHero).Hp;
                    Require(hpBefore == 23 && Body(run).X == 2 && Body(run).Y == 3,
                        "The bench approach did not take the actual opportunity hit and reach its support.");
                    if (run == sim) SaveBatch(run, policy, directory, "bench-before-use");
                    var doseOption = run.DiscoverCommands(host, PlanHero).Single(x => x.Command.Kind == CommandKind.UseAlchemyDose
                        && x.Command.Target == doseId && x.Command.Inventory.Destination == PlanHero);
                    Require(doseOption.Query.Admissible && doseOption.Query.Costs.Any(x => x.Kind == "action")
                        && doseOption.Query.Costs.Any(x => x.ResourceId == doseId && x.Amount == 1),
                        "The actual dose was absent from the authorized result command interface.");
                    var use = doseOption.Command;
                    LaterCommit(run, use);
                    var after = run.Capture();
                    var spent = after.AlchemyDoses[0];
                    Require(spent.Spent && spent.UsedAt == wounded.RuleClock
                        && spent.PotentialHealing == spent.FirstD4 + spent.SecondD4 + 2 && spent.ActualHealing == 3
                        && after.Lives.Single(x => x.ActorId == PlanHero).Hp == hpBefore + spent.ActualHealing
                        && spent.MassPounds == new RuleQuantity(1, 10) && spent.Hp == wounded.AlchemyDoses[0].Hp
                        && spent.OwnerId == wounded.AlchemyDoses[0].OwnerId && spent.LocationId == wounded.AlchemyDoses[0].LocationId
                        && after.AlchemyDoses.Count(x => !x.Spent) == 5
                        && after.WorldIntervals.Single(x => x.ActorId == PlanHero).ActionSpent,
                        "Actual use lost source healing, its Action, exact empty vial or remaining doses.");
                    byte[] used = Bytes(run);
                    Require(run.Execute(host, use).Outcome == Outcome.Duplicate && Bytes(run).SequenceEqual(used),
                        "Duplicate dose use changed the RNG, effect or stock.");
                    if (run == sim) SaveBatch(run, policy, directory, "dose-used");
                    LaterCommit(run, Tac(run, CommandKind.TacticalStep, x: 1, y: 3));
                    LaterCommit(run, Tac(run, CommandKind.EndRegularTurn));
                    FinishLaterFight(run, defenderAttacked: true);
                    PlanWalk(run, 0, -1);
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)) && !sim.Capture().InventoryCombat,
                    "Actual dose use, later combat closure and ordinary continuation did not replay exactly.");
                SaveBatch(sim, policy, directory, "continued");
            });

            cases.Add("mgt04_connected_recipe4_pause_cancel_and_exact_spoilage_tie", () =>
            {
                var policy = BatchPolicy();
                var sim = BatchReady(policy, preliminaryResearch: 900);
                var cutoff = sim.Capture();
                var lotId = cutoff.BloodSpecimen.LotId;
                var originAge = BloodAge(sim).UnprotectedAge;
                var zero = new Simulation(policy, cutoff, ExecutionProfile.Laboratory);
                LaterCommit(zero, BatchCommand(zero, CommandKind.StartManufacturing, y: 2));
                LaterCommit(zero, BatchCommand(zero, CommandKind.PauseManufacturing));
                WorldAdvance(zero, 60);
                LaterCommit(zero, BatchCommand(zero, CommandKind.CancelManufacturing));
                var returned = zero.Capture();
                Require(returned.ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Returned
                    && returned.Work.AvailableAmount(lotId) == Q(1)
                    && returned.PortableEquipment.Single(x => x.Id == lotId).ParentId == cutoff.BloodSpecimen.VesselId
                    && BatchClaim(zero, "packaging").ReleasedAmount == Q(2)
                    && returned.RandomState == cutoff.RandomState && returned.AlchemyDoses.Length == 0
                    && BloodAge(zero).UnprotectedAge == originAge.AddSeconds(60),
                    "Zero-labor cancellation must release the same genuinely older specimen and packaging.");
                FormulaDenial(zero, host, BatchCommand(zero, CommandKind.StartManufacturing), "ConnectedRecipe4BatchAlreadyDeclared");
                SaveBatch(zero, policy, directory, "cancelled-with-return");

                var resumed = new Simulation(policy, cutoff, ExecutionProfile.Laboratory);
                LaterCommit(resumed, BatchCommand(resumed, CommandKind.StartManufacturing, y: 2));
                WorldAdvance(resumed, 300);
                LaterCommit(resumed, BatchCommand(resumed, CommandKind.PauseManufacturing));
                Require(BatchOrder(resumed).Work.Labor == T(300) && BatchOrder(resumed).Work.Retained == default,
                    "Pausing before stabilization erased labor or retained unfinished progress.");
                resumed = SaveBatch(resumed, policy, directory, "paused-before-stabilization");
                WorldAdvance(resumed, 6);
                LaterCommit(resumed, BatchCommand(resumed, CommandKind.ResumeManufacturing));
                WorldAdvance(resumed, 900);
                var work = BatchOrder(resumed);
                Require(work.Work.Labor == T(1200) && work.Work.Retained == T(900) && work.StabilizedAt == resumed.Capture().RuleClock,
                    "Resume did not earn the replacement first phase through real labor.");
                var stabilizedAge = BloodAge(resumed).UnprotectedAge;
                LaterCommit(resumed, BatchCommand(resumed, CommandKind.PauseManufacturing));
                WorldAdvance(resumed, 60);
                Require(BatchOrder(resumed).Work.Retained == T(900) && BloodAge(resumed).UnprotectedAge == stabilizedAge,
                    "A paused, intact apparatus lost completed stabilization.");
                LaterCommit(resumed, BatchCommand(resumed, CommandKind.CancelManufacturing));
                Require(resumed.Capture().ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Consumed
                    && BatchClaim(resumed, "component3").ConsumedAmount == Q(1)
                    && BatchClaim(resumed, "packaging").ReleasedAmount == Q(2)
                    && resumed.Capture().RandomState == cutoff.RandomState && resumed.Capture().AlchemyDoses.Length == 0,
                    "Abandonment after actual labor did not spend inputs once and release unused packaging.");
                SaveBatch(resumed, policy, directory, "abandoned-after-work");

                long spoilAt = cutoff.RuleClock.Numerator + 28800 - originAge.Numerator;
                Require(spoilAt < 57600, "The selected reachable spoilage tie must fit the existing Watch.");
                AdvanceBloodTo(sim, T(spoilAt - 912));
                LaterCommit(sim, BatchCommand(sim, CommandKind.StartManufacturing));
                WorldAdvance(sim, 6);
                LaterCommit(sim, BatchCommand(sim, CommandKind.PauseManufacturing));
                WorldAdvance(sim, 6);
                LaterCommit(sim, BatchCommand(sim, CommandKind.ResumeManufacturing));
                WorldAdvance(sim, 900);
                Require(sim.Capture().RuleClock == T(spoilAt) && BloodAge(sim).State == HarvestPreservationState.Spoiled
                    && BatchOrder(sim).Status == ManufacturingStatus.Paused && BatchOrder(sim).Work.Labor == T(906)
                    && BatchOrder(sim).Work.Retained == default && !BatchOrder(sim).StabilizedAt.HasValue
                    && sim.Capture().RandomState == cutoff.RandomState,
                    "Simultaneous spoilage must win over attempted stabilization without drawing quality.");
                FormulaDenial(sim, host, BatchCommand(sim, CommandKind.ResumeManufacturing), "ManufacturingIngredientSpoiled");
                SaveBatch(sim, policy, directory, "paused-at-spoilage-tie");
            });

            cases.Add("mgt04_connected_recipe4_due_condition_defers_one_check", () =>
            {
                var policy = BatchDeferredPolicy();
                var sim = BatchReady(policy);
                LaterCommit(sim, CCCommand(sim, "batch-stun", BatchWorker));
                FormulaDenial(sim, host, BatchCommand(sim, CommandKind.StartManufacturing), "ManufacturingWorkerIncapable");
                LaterCommit(sim, CCCommand(sim, "batch-ward", BatchWorker));
                LaterCommit(sim, BatchCommand(sim, CommandKind.StartManufacturing, y: 2));
                uint rng = sim.Capture().RandomState;
                WorldAdvance(sim, 14400);
                Require(BatchOrder(sim).Status == ManufacturingStatus.AwaitingCheck && BatchOrder(sim).Work.Complete
                    && sim.Capture().RuleClock == T(56648) && sim.Capture().RandomState == rng
                    && BloodAge(sim).UnprotectedAge == T(14279),
                    "The due ward expiry must defer the real check without losing stabilization or labor.");
                FormulaDenial(sim, host, BatchCommand(sim, CommandKind.ResumeManufacturing), "ManufacturingWorkerIncapable");
                var replay = SaveBatch(sim, policy, directory, "awaiting-check");
                foreach (var run in new[] { sim, replay }) {
                    WorldAdvance(run, 1);
                    LaterCommit(run, CCCommand(run, "batch-cure", BatchWorker));
                    var check = BatchCommand(run, CommandKind.ResumeManufacturing);
                    LaterCommit(run, check);
                    var draw = PlaytestDice.RollD20(rng);
                    Require(BatchOrder(run).Status == ManufacturingStatus.AwaitingChoice && BatchOrder(run).Natural == draw.Natural
                        && run.Capture().RandomState == draw.NextRandomState && BatchOrder(run).Work.Labor == T(14400)
                        && run.Execute(host, check).Outcome == Outcome.Duplicate,
                        "Explicit continuation must resolve the original check exactly once without adding labor.");
                    LaterCommit(run, BatchCommand(run, CommandKind.ResolveManufacturingQuality, (int)CraftQualityChoice.Durability));
                    Require(run.Capture().AlchemyDoses.Length == 5 && run.Capture().AlchemyDoses.All(x => x.Hp == 2 && x.MaximumHp == 2)
                        && BatchClaim(run, "packaging").ReleasedAmount == Q(2),
                        "Durability must use the source batch size and release unneeded supplemental vials.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Deferred native completion did not replay exactly.");
                SaveBatch(sim, policy, directory, "deferred-check-settled");
            });

            cases.Add("mgt04_connected_recipe4_masterwork_returns_exact_blood", () =>
            {
                var policy = BatchPolicy(seed: 818668);
                var sim = BatchReady(policy);
                string lotId = sim.Capture().BloodSpecimen.LotId;
                LaterCommit(sim, BatchCommand(sim, CommandKind.StartManufacturing));
                uint rng = sim.Capture().RandomState;
                WorldAdvance(sim, 14400);
                var check = BatchOrder(sim);
                Require(check.Quality == CraftQuality.Masterwork && check.Natural == PlaytestDice.RollD20(rng).Natural
                    && check.Status == ManufacturingStatus.AwaitingChoice && check.Natural == 19,
                    "The actual masterwork roll or required choice was bypassed.");
                FormulaDenial(sim, host, BatchCommand(sim, CommandKind.ResolveManufacturingQuality,
                    (int)CraftQualityChoice.FullYield, y: 4), "ManufacturingFullYieldUnavailable");
                var pending = SaveBatch(sim, policy, directory, "masterwork-choice");
                RuleTime retainedAge = BloodAge(sim).UnprotectedAge;
                foreach (var run in new[] { sim, pending }) {
                    LaterCommit(run, BatchCommand(run, CommandKind.ResolveManufacturingQuality,
                        (int)CraftQualityChoice.Durability, y: 4));
                    var returned = run.Capture();
                    var physical = returned.PortableEquipment.Single(x => x.Id == lotId);
                    Require(returned.ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Returned
                        && BatchClaim(run, "component3").ReleasedAmount == Q(1) && returned.Work.AvailableAmount(lotId) == Q(1)
                        && physical.ParentId == returned.BloodSpecimen.VesselId
                        && PortableEquipmentValidation.Mass(returned, physical) == ConnectedBloodSpecimen.Mass
                        && returned.AlchemyDoses.Length == 5 && returned.AlchemyDoses.All(x => x.Hp == 2)
                        && BloodAge(run).UnprotectedAge == retainedAge,
                        "Masterwork must return one actual unchanged catalyst and settle only the lawful durability batch.");
                    WorldAdvance(run, 12);
                    Require(BloodAge(run).UnprotectedAge == retainedAge.AddSeconds(12),
                        "The returned specimen did not resume its own age.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(pending)), "The native catalyst return did not replay exactly.");
                SaveBatch(sim, policy, directory, "masterwork-return");
            });

            cases.Add("mgt04_connected_recipe4_native_mishap_and_flawed_settlement", () =>
            {
                foreach (uint seed in new uint[] { 817576, 99690 }) {
                    var policy = BatchPolicy(seed: seed);
                    var sim = BatchReady(policy);
                    LaterCommit(sim, BatchCommand(sim, CommandKind.StartManufacturing, y: 2));
                    var check = PlaytestDice.RollD20(sim.Capture().RandomState);
                    WorldAdvance(sim, 14400);
                    var order = BatchOrder(sim);
                    var state = sim.Capture();
                    bool mishap = seed == 817576;
                    Require(order.Status == ManufacturingStatus.Complete && order.Natural == check.Natural
                        && order.Quality == (mishap ? CraftQuality.Mishap : CraftQuality.Flawed)
                        && state.ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Consumed
                        && BatchClaim(sim, "component3").ConsumedAmount == Q(1) && BatchClaim(sim, "packaging").ReleasedAmount == Q(2)
                        && order.XpAward == 0 && state.AlchemyDoses.Length == (mishap ? 0 : 2),
                        "Native low-quality settlement changed the actual specimen, packaging, XP or finite product.");
                    if (mishap) {
                        var consequence = DiceStream.Draw(check.NextRandomState, 6);
                        Require(check.Natural == 1 && order.Mishap == consequence.Value + 1
                            && state.CraftingIncidents.Single(x => x.Id == order.MishapIncidentId).Result == order.Mishap,
                            "Natural-1 manufacture did not apply its actual native d6 consequence.");
                    }
                    SaveBatch(sim, policy, directory, mishap ? "mishap" : "flawed");
                }
            });

            cases.Add("mgt04_connected_recipe4_actual_injury_and_failed_recovery", () =>
            {
                string occurrenceId = TestOnlySharedWorldPolicy.Recipe4InjuryWitnessId;
                var policy = BatchInjuryPolicy();
                var sim = BatchReady(policy);
                var before = sim.Capture();
                Require(before.RuleClock == TestOnlySharedWorldPolicy.Recipe4InjuryWitnessAt && before.Lives.Single(x => x.ActorId == BatchWorker).Hp == 1
                    && before.ManufacturingOrders.Length == 0 && before.AlchemyDoses.Length == 0,
                    "The separately selected witness installed a batch or altered the starting injury facts.");
                SaveBatch(sim, policy, directory, "injury-before-incident");
                CraftEvent(sim, occurrenceId);
                var accident = Incident(sim, occurrenceId);
                var injured = sim.Capture();
                Require(accident.Result == 4 && accident.Damage > 0 && accident.WoundD20 > 0
                    && accident.InjuryD6 == (int)Injury.FineMotorTrauma && accident.RandomBefore == before.RandomState
                    && accident.RandomAfter == injured.RandomState && injured.Lives.Single(x => x.ActorId == BatchWorker).Hp == 0
                    && injured.Receipts.Any(x => x.Revision == accident.Revision && CommandHistory.Read(x).Target == occurrenceId),
                    "The authored consequence did not resolve through actual damage, wound, injury and receipt authority.");
                var replay = SaveBatch(sim, policy, directory, "injury-before-recovery");
                foreach (var run in new[] { sim, replay }) {
                    WorldAdvance(run, 6);
                    var recovered = run.Capture();
                    var deathSave = recovered.LifeEvents.Single(x => x.ActorId == BatchWorker && x.Kind == LifeEventKind.DeathSave);
                    var facts = CharacterStateFacts.ForActor(recovered, BatchWorker);
                    int intelligence = facts.Rules.AbilityModifier(CharacterAbility.Intelligence);
                    int proficiency = facts.Rules.ProficiencyBonus;
                    int injury = facts.InjuryPenalty(CharacterAbility.Intelligence, toolCheck: true);
                    Require(facts.Life.Hp == 1 && deathSave.Natural == 20 && deathSave.RandomBefore == accident.RandomAfter
                        && deathSave.RandomAfter == recovered.RandomState && intelligence == 0 && proficiency == 2 && injury == -1,
                        "Legitimate recovery did not retain the actual Intelligence-tool injury penalty.");
                    LaterCommit(run, BatchCommand(run, CommandKind.StartManufacturing, y: 2));
                    var draw = PlaytestDice.RollD20(recovered.RandomState);
                    WorldAdvance(run, 14400);
                    var order = BatchOrder(run);
                    var settled = run.Capture();
                    int margin = order.Natural + intelligence + proficiency + injury - 8;
                    Require(order.Quality == CraftQuality.Failed && order.Natural == draw.Natural && order.Natural == 2
                        && margin == -5 && settled.RandomState == draw.NextRandomState && order.XpAward == 0
                        && settled.ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Consumed
                        && BatchClaim(run, "component3").ConsumedAmount == Q(1)
                        && BatchClaim(run, "component0").ReleasedAmount == default
                        && BatchClaim(run, "component1").ReleasedAmount == Q(1)
                        && BatchClaim(run, "component2").ReleasedAmount == new RuleQuantity(5, 4)
                        && BatchClaim(run, "packaging").ReleasedAmount == Q(2)
                        && settled.AlchemyDoses.Length == 0 && settled.PortableEquipment.All(x => x.Id != settled.BloodSpecimen.LotId),
                        "Failed settlement lost exact recovery, invented blood/XP/output or bypassed the actual roll.");
                }
                Require(Bytes(sim).SequenceEqual(Bytes(replay)), "Injury, recovery and Failed settlement changed across restore.");
                SaveBatch(sim, policy, directory, "injured-failed");
            });

            cases.Add("mgt04_connected_recipe4_wire95_preserves_wire94_and_rejects_malformed_composition", () =>
            {
                var codec = new SnapshotCodec();
                var old = BloodHandoffPolicy();
                var next = BatchPolicy();
                var original = codec.Encode(old.Initial());
                var current = next.Initial();
                var bytes = codec.Encode(current);
                Require(BitConverter.ToInt32(original, 4) == 94 && BitConverter.ToInt32(bytes, 4) == 95
                    && current.SchemaVersion == 90 && codec.Encode(codec.Decode(bytes)).SequenceEqual(bytes)
                    && codec.Encode(codec.Decode(original)).SequenceEqual(original)
                    && current.ConnectedBatch.Disposition == ConnectedSpecimenDisposition.Uncharged,
                    "The exact successor envelope changed a prior wire or duplicated the original payload.");
                Throws<ArgumentException>(() => new Simulation(old, codec.Decode(bytes), ExecutionProfile.Laboratory));
                Throws<ArgumentException>(() => new Simulation(next, codec.Decode(original), ExecutionProfile.Laboratory));
                Throws<InvalidOperationException>(() => new Simulation(next, codec.Decode(bytes), ExecutionProfile.Release));
                Throws<InvalidOperationException>(() => next.EnableConnectedRecipe4Batch());
                byte[] Retag(byte[] save, int wire)
                {
                    var body = save.Take(save.Length - 32).ToArray();
                    Array.Copy(BitConverter.GetBytes(wire), 0, body, 4, 4);
                    using (var sha = System.Security.Cryptography.SHA256.Create())
                        return body.Concat(sha.ComputeHash(body)).ToArray();
                }
                Throws<System.IO.InvalidDataException>(() => codec.Decode(Retag(bytes, 94)));
                Throws<System.IO.InvalidDataException>(() => codec.Decode(Retag(original, 95)));
                var missing = current.Copy();
                missing.ConnectedBatch = null;
                Throws<ArgumentException>(() => codec.Encode(missing));
                var moved = current.Copy();
                moved.PortableEquipment = moved.PortableEquipment.Select(x => x.Id == current.ConnectedBatch.ApparatusId
                    ? x.With(groundX: 4) : x).ToArray();
                Throws<ArgumentException>(() => codec.Encode(moved));
            });
        }
    }
}
#endif
