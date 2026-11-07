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
        private const string RouteTravelId = "TEST_ONLY.route.cache-to-plot";

        private static TestOnlyExpeditionRouteFixture RouteTravelFixture(
            ExpeditionRouteQuality quality = ExpeditionRouteQuality.Secured, int risk = 0,
            ExpeditionRouteMapping mapping = ExpeditionRouteMapping.Mapped, RuleQuantity? capacity = null)
            => new TestOnlyExpeditionRouteFixture(new TestOnlyExpeditionRoute(RouteTravelId,
                TestOnlyPolicy.ContainerId, TestOnlyCropPolicy.PlotId, 1, 2, 3, 3, new RuleQuantity(2),
                quality, risk, mapping, capacity ?? new RuleQuantity(10), new[] {
                    new TestOnlyRoutePositionBinding(default, 1, 2),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(1), 1, 3),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(2), 2, 3)
                }));

        private static TestOnlyExpeditionRouteFixture RouteTravelCheckpointFixture()
            => new TestOnlyExpeditionRouteFixture(new TestOnlyExpeditionRoute(RouteTravelId,
                TestOnlyPolicy.ContainerId, TestOnlyCropPolicy.PlotId, 1, 2, 3, 3, new RuleQuantity(4),
                ExpeditionRouteQuality.Secured, 0, ExpeditionRouteMapping.Mapped, new RuleQuantity(10), new[] {
                    new TestOnlyRoutePositionBinding(default, 1, 2),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(1), 1, 3),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(2), 2, 3),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(3), 2, 4),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(4), 3, 4)
                }));

        private static TestOnlySharedWorldPolicy RouteTravelPolicy(TestOnlyExpeditionRouteFixture fixture,
            ConditionCombatFixture conditions = null)
            => new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(), new SupplyCacheFixture(),
                conditions: conditions)
                .EnableExpeditionRouteTravel(fixture);

        private static TestOnlyExpeditionRouteMotionFixture RouteTravelMotionFixture(TestOnlyExpeditionRouteFixture routes)
            => new TestOnlyExpeditionRouteMotionFixture(routes,
                new TestOnlyRouteMotionLeg(RouteTravelId, default, new RuleQuantity(1), 1, 2, 1, 3),
                new TestOnlyRouteMotionLeg(RouteTravelId, new RuleQuantity(1), new RuleQuantity(2), 1, 3, 2, 3));

        private static TestOnlyExpeditionRouteMotionFixture RouteTravelCheckpointMotionFixture(TestOnlyExpeditionRouteFixture routes)
            => new TestOnlyExpeditionRouteMotionFixture(routes,
                new TestOnlyRouteMotionLeg(RouteTravelId, default, new RuleQuantity(1), 1, 2, 1, 3),
                new TestOnlyRouteMotionLeg(RouteTravelId, new RuleQuantity(1), new RuleQuantity(2), 1, 3, 2, 3),
                new TestOnlyRouteMotionLeg(RouteTravelId, new RuleQuantity(2), new RuleQuantity(3), 2, 3, 2, 4),
                new TestOnlyRouteMotionLeg(RouteTravelId, new RuleQuantity(3), new RuleQuantity(4), 2, 4, 3, 4));

        private static TestOnlySharedWorldPolicy RouteObservationPolicy(TestOnlyExpeditionRouteFixture routes, long enemyHp = 26,
            TestOnlyExpeditionRouteMotionFixture motion = null)
            => new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp), new SupplyCacheFixture())
                .EnableRouteObservationIntegration(routes, motion ?? RouteTravelMotionFixture(routes), RouteTravelObservationFixture());

        private static Command RouteTravelCommand(Simulation s, CommandKind kind, string id = "route.command",
            string actor = TestOnlyPolicy.ActorId)
            => new Command(id, actor, s.Capture().Revision, kind, RouteTravelId);

        private static Command RouteMappingCommand(Simulation s, string resultId, string id,
            string actor = TestOnlyPolicy.ActorId)
            => new Command(id, actor, s.Capture().Revision, CommandKind.ConsumeTestOnlyRouteMappingResult, resultId);

        private static void RouteTravelReachSource(Simulation s)
        {
            WorldStep(s, 0, 1); WorldAdvance(s, 3, 2);
            WorldStep(s, 1, 0); WorldAdvance(s, 3, 2);
            WorldStep(s, 0, 1); WorldAdvance(s, 3, 2);
        }

        private static ObservationFixture RouteTravelObservationFixture()
            => new ObservationFixture(5, 5, Array.Empty<ObservationGridCell>(), new[] {
                new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
            });

        private static void AddExpeditionRouteTravelCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("expedition_route_rate_and_mapping_arithmetic_are_exact", () => {
                var qualities = new[] {
                    ExpeditionRouteQuality.Secured, ExpeditionRouteQuality.Known,
                    ExpeditionRouteQuality.Contested, ExpeditionRouteQuality.Collapsed
                };
                var expectedAt30 = new long[] { 21600, 28800, 36000, 43200 };
                for (int i = 0; i < qualities.Length; i++) {
                    var actual = ExpeditionRouteTravelRules.ActualMovingTime(
                        new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds), 30, qualities[i]);
                    Require(actual == new RuleTime(expectedAt30[i])
                        && ExpeditionRouteTravelRules.EarnedNominalEffort(actual, 30, qualities[i])
                            == new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds),
                        "Route quality and 3 mph must preserve exact 480-minute nominal effort.");
                }
                Require(ExpeditionRouteTravelRules.ActualMovingTime(
                        new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds), 20, ExpeditionRouteQuality.Secured)
                        == new RuleTime(32400)
                    && ExpeditionRouteTravelRules.EarnedNominalEffort(new RuleTime(16200), 20,
                        ExpeditionRouteQuality.Secured) == new RuleTime(14400)
                    && ExpeditionRouteTravelRules.ProgressAtEffort(default, new RuleQuantity(2), new RuleTime(14400))
                        == new RuleQuantity(1)
                    && ExpeditionRouteTravelRules.EffortAtProgress(default, new RuleQuantity(2), new RuleQuantity(1))
                        == new RuleTime(14400),
                    "Burden-adjusted pace and exact partial Progress were rounded or mis-scaled.");
                Require(ExpeditionRouteTravelRules.BaseProgress(ExpeditionRouteMapping.Unknown) == default
                    && ExpeditionRouteTravelRules.BaseProgress(ExpeditionRouteMapping.Sketched) == new RuleQuantity(1)
                    && ExpeditionRouteTravelRules.BaseProgress(ExpeditionRouteMapping.Mapped) == new RuleQuantity(2)
                    && ExpeditionRouteTravelRules.BaseProgress(ExpeditionRouteMapping.Secured) == new RuleQuantity(2),
                    "FL-10 base Progress changed by starting Mapping.");
            });

            cases.Add("route_mapping_results_persist_without_claiming_a_check_or_passage", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 2,
                    mapping: ExpeditionRouteMapping.Unknown);
                var results = new TestOnlyExpeditionRouteMappingResultFixture(routes,
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId, "route.mapping.risk2.first",
                        TestOnlyPolicy.ActorId, "evidence.synthetic.first", default,
                        ExpeditionRouteMappingResultDegree.Success),
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId, "route.mapping.risk2.second",
                        TestOnlyPolicy.ActorId, "evidence.synthetic.second", default,
                        ExpeditionRouteMappingResultDegree.Success),
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId, "route.mapping.future",
                        TestOnlyPolicy.ActorId, "evidence.synthetic.future", new RuleTime(1000),
                        ExpeditionRouteMappingResultDegree.CriticalSuccess),
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId, "route.mapping.other-actor",
                        TestOnlyPolicy.CompanionId, "evidence.synthetic.other-actor", default,
                        ExpeditionRouteMappingResultDegree.Success));
                var policy = RouteTravelPolicy(routes).EnableTestOnlyRouteMappingResults(results);
                var simulation = World(policy);
                var initial = simulation.Capture();
                Require(initial.SchemaVersion == Snapshot.RouteMappingSchema && initial.RouteMappingResults.Length == 0,
                    "Synthetic mapping results did not select empty schema54 history.");
                var first = RouteMappingCommand(simulation, "route.mapping.risk2.first", "route.mapping.apply.first");
                var firstQuery = simulation.QueryCommand(host, first);
                Require(firstQuery.Supported && firstQuery.Admissible && firstQuery.Costs.Count == 0,
                    "Synthetic result query claimed costs or was not admissible: " + firstQuery.Code);
                Require(Bytes(simulation).SequenceEqual(Bytes(new Simulation(policy,
                        new SnapshotCodec().Decode(Bytes(simulation)), ExecutionProfile.Laboratory))),
                    "Initial schema54 route mapping state did not replay canonically.");
                WorldCommit(simulation, first);
                var afterFirst = simulation.Capture();
                Require(afterFirst.RouteMappingResults.Length == 1
                    && afterFirst.RouteMappingResults[0].MappingBefore == ExpeditionRouteMapping.Unknown
                    && afterFirst.RouteMappingResults[0].MappingAfter == ExpeditionRouteMapping.Unknown
                    && afterFirst.RouteMappingResults[0].MarksAfter == 1
                    && ExpeditionRouteMappingRules.Current(afterFirst, RouteTravelId, ExpeditionRouteMapping.Unknown).UnspentMarks == 1
                    && afterFirst.RuleClock == initial.RuleClock && afterFirst.RandomState == initial.RandomState
                    && afterFirst.Actors.Select(x => x.Id + "|" + x.X + "|" + x.Y)
                        .SequenceEqual(initial.Actors.Select(x => x.Id + "|" + x.X + "|" + x.Y))
                    && afterFirst.InventoryLots.Length == initial.InventoryLots.Length,
                    "First Risk-2 success failed to retain one mark or changed unrelated simulation state.");
                var checkpoint = Bytes(simulation);
                var restored = new Simulation(policy, new SnapshotCodec().Decode(checkpoint), ExecutionProfile.Laboratory);
                Require(checkpoint.SequenceEqual(Bytes(restored)), "Schema54 mapping result changed after save/restore.");
                RejectUnchanged(restored, host, RouteMappingCommand(restored, "route.mapping.risk2.first",
                    "route.mapping.apply.duplicate"), "RouteMappingResultAlreadyConsumed");
                RejectUnchanged(restored, host, RouteMappingCommand(restored, "missing.synthetic.result",
                    "route.mapping.apply.unknown"), "UnknownTestOnlyRouteMappingResult");
                RejectUnchanged(restored, host, RouteMappingCommand(restored, "route.mapping.future",
                    "route.mapping.apply.future"), "RouteMappingResultNotComplete");
                RejectUnchanged(restored, host, RouteMappingCommand(restored, "route.mapping.other-actor",
                    "route.mapping.apply.actor"), "RouteMappingResultActorMismatch");
                WorldCommit(restored, RouteMappingCommand(restored, "route.mapping.risk2.second",
                    "route.mapping.apply.second"));
                var afterSecond = restored.Capture();
                var knowledge = ExpeditionRouteMappingRules.Current(afterSecond, RouteTravelId, ExpeditionRouteMapping.Unknown);
                Require(knowledge.Mapping == ExpeditionRouteMapping.Sketched && knowledge.UnspentMarks == 0
                    && afterSecond.RouteMappingResults.Length == 2
                    && afterSecond.RouteMappingResults.All(x => x.Synthetic
                        && x.OperationId == ExpeditionRouteMappingRules.MapRouteOperationId),
                    "Second distinct success did not cross Risk-2 threshold exactly once with auditable provenance.");
                var replay = new Simulation(policy, new SnapshotCodec().Decode(Bytes(restored)), ExecutionProfile.Laboratory);
                Require(Bytes(restored).SequenceEqual(Bytes(replay)), "Route mapping records failed deterministic replay.");
            });

            cases.Add("route_mapping_surplus_waits_for_a_distinct_success_and_does_not_survey", () => {
                var routes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 1,
                    mapping: ExpeditionRouteMapping.Unknown);
                var results = new TestOnlyExpeditionRouteMappingResultFixture(routes,
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId, "route.mapping.crit",
                        TestOnlyPolicy.ActorId, "evidence.synthetic.crit", default,
                        ExpeditionRouteMappingResultDegree.CriticalSuccess),
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId, "route.mapping.failure",
                        TestOnlyPolicy.ActorId, "evidence.synthetic.failure", default,
                        ExpeditionRouteMappingResultDegree.Failure),
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId, "route.mapping.success",
                        TestOnlyPolicy.ActorId, "evidence.synthetic.success", default,
                        ExpeditionRouteMappingResultDegree.Success));
                var policy = RouteTravelPolicy(routes).EnableTestOnlyRouteMappingResults(results);
                var simulation = World(policy);
                WorldCommit(simulation, RouteMappingCommand(simulation, "route.mapping.crit", "route.mapping.crit.apply"));
                var afterCritical = ExpeditionRouteMappingRules.Current(simulation.Capture(), RouteTravelId,
                    ExpeditionRouteMapping.Unknown);
                Require(afterCritical.Mapping == ExpeditionRouteMapping.Sketched && afterCritical.UnspentMarks == 1,
                    "Critical success did not retain one surplus mark after one-level promotion.");
                WorldCommit(simulation, RouteMappingCommand(simulation, "route.mapping.failure", "route.mapping.fail.apply"));
                var afterFailure = ExpeditionRouteMappingRules.Current(simulation.Capture(), RouteTravelId,
                    ExpeditionRouteMapping.Unknown);
                Require(afterFailure.Mapping == ExpeditionRouteMapping.Sketched && afterFailure.UnspentMarks == 1,
                    "Failure consumed or activated held surplus marks.");
                WorldCommit(simulation, RouteMappingCommand(simulation, "route.mapping.success", "route.mapping.success.apply"));
                var afterSuccess = ExpeditionRouteMappingRules.Current(simulation.Capture(), RouteTravelId,
                    ExpeditionRouteMapping.Unknown);
                Require(afterSuccess.Mapping == ExpeditionRouteMapping.Mapped && afterSuccess.UnspentMarks == 1,
                    "A later distinct success failed to consume exactly one threshold and preserve excess.");

                var unknownRoutes = RouteTravelFixture(ExpeditionRouteQuality.Secured, risk: 0,
                    mapping: ExpeditionRouteMapping.Unknown);
                var unknownResults = new TestOnlyExpeditionRouteMappingResultFixture(unknownRoutes,
                    new TestOnlyExpeditionRouteMappingResult(RouteTravelId, "route.mapping.synthetic.survey",
                        TestOnlyPolicy.ActorId, "evidence.synthetic.not-survey", default,
                        ExpeditionRouteMappingResultDegree.Success));
                var unknownPolicy = RouteTravelPolicy(unknownRoutes).EnableTestOnlyRouteMappingResults(unknownResults);
                var unknownSimulation = World(unknownPolicy);
                RouteTravelReachSource(unknownSimulation);
                WorldCommit(unknownSimulation, RouteMappingCommand(unknownSimulation,
                    "route.mapping.synthetic.survey", "route.mapping.synthetic.survey.apply"));
                Require(ExpeditionRouteMappingRules.Current(unknownSimulation.Capture(), RouteTravelId,
                        ExpeditionRouteMapping.Unknown).Mapping == ExpeditionRouteMapping.Sketched
                    && unknownRoutes.Routes.Single().Mapping == ExpeditionRouteMapping.Unknown,
                    "Synthetic result rewrote immutable authored Mapping or failed to record separate knowledge.");
                var travel = RouteTravelCommand(unknownSimulation, CommandKind.StartRouteTravel,
                    "route.mapping.synthetic.travel");
                var travelQuery = unknownSimulation.QueryCommand(host, travel);
                Require(travelQuery.Supported && !travelQuery.Admissible && travelQuery.Code == "RouteRequiresReconnaissance",
                    "Synthetic Map Route result incorrectly established Unknown-route passage feasibility: " + travelQuery.Code);
            });

            cases.Add("expedition_route_shared_clock_save_pause_pace_change_and_management", () => {
                var conditionStart = new ConditionStamp(new RuleTime(9, 2));
                var conditionExpiry = new ConditionStamp(new RuleTime(7209, 2));
                var routeCondition = new ConditionFixtureEvent(TestOnlyPolicy.ActorId,
                    ConditionOperation.Apply("event.route-poison", conditionStart,
                        new ConditionApplicationData("event.route-poison", TestOnlyPolicy.ActorId, "TEST_ONLY.route-clock",
                            "Poisoned", conditionExpiry, "expires", true)));
                var policy = RouteTravelPolicy(RouteTravelFixture(), new ConditionCombatFixture(routeCondition));
                var simulation = World(policy);
                Require(simulation.Capture().SchemaVersion == Snapshot.ExpeditionRouteSchema,
                    "Opted-in route state did not select the append-only route schema.");

                // The authored source site is the existing TEST_ONLY container at (1,2).
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, IC(simulation, CommandKind.DispatchConditionEvent, "event.route-poison"));

                var start = RouteTravelCommand(simulation, CommandKind.StartRouteTravel);
                var preview = simulation.QueryCommand(host, start);
                Require(preview.Supported && preview.Admissible && preview.Costs.Any(x =>
                    x.Kind == "nominal-route-seconds" && x.Amount == ExpeditionRouteTravelRules.NominalSegmentSeconds),
                    "Route query did not expose the admissible nominal segment cost: supported=" + preview.Supported
                    + ", admissible=" + preview.Admissible + ", code=" + preview.Code + ", costs="
                    + string.Join(";", preview.Costs.Select(x => x.Kind + "=" + x.Amount)) + ", actor="
                    + simulation.Capture().Actors.Single(x => x.Id == start.Actor).X + ","
                    + simulation.Capture().Actors.Single(x => x.Id == start.Actor).Y + ".");
                WorldCommit(simulation, start);
                byte[] afterStart = Bytes(simulation);
                Require(simulation.Execute(host, start).Outcome == Outcome.Duplicate
                    && afterStart.SequenceEqual(Bytes(simulation)),
                    "Duplicate route start changed shared state, time, RNG, or receipts.");
                RejectUnchanged(simulation, host, IC(simulation, CommandKind.BeginWorldStep, "walk", x: -1),
                    "RouteTravelMustPauseFirst");
                RejectUnchanged(simulation, host, IC(simulation, CommandKind.BeginWorldStep, "walk",
                    actor: TestOnlyPolicy.CompanionId, x: -1), "RouteTravelPathReserved");
                WorldStep(simulation, 1, 0, actor: TestOnlyPolicy.CompanionId);
                WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, -1, 0, actor: TestOnlyPolicy.CompanionId);
                WorldAdvance(simulation, 3, 2);
                Require(simulation.Capture().RouteTravels.Single().NominalEffort > default(RuleTime)
                    && simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.CompanionId).X == 3,
                    "A moving route immobilized another actor or failed to accrue concurrent shared-clock effort.");
                FarmWork(simulation, CommandKind.PlantCrop);

                // At 20 ft Speed on Secured quality, 4.5 actual hours earn half the Mapped segment.
                WorldAdvance(simulation, 16197); // plus the other actor's 3 seconds: 4.5 hours total.
                var midpoint = simulation.Capture();
                var active = midpoint.RouteTravels.Single();
                Require(midpoint.RuleClock == new RuleTime(32409, 2)
                    && active.Status == ExpeditionRouteTravelStatus.Moving
                    && active.Progress == new RuleQuantity(1) && active.NominalEffort == new RuleTime(14400)
                    && midpoint.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && midpoint.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && Crop(simulation).Stage == CropStage.Growing,
                    "Exact route progress, bound location, or companion planting did not advance on the shared clock.");
                var conditionJournal = midpoint.Conditions.Single(x => x.Target == TestOnlyPolicy.ActorId);
                Require(conditionJournal.Now.Time == conditionExpiry.Time && conditionJournal.Operations.Count <= 3
                    && !TestOnlyClubAttackPolicy.ConditionsFor(midpoint, TestOnlyPolicy.ActorId).View().Has(ConditionKind.Poisoned),
                    "Long travel either wrote every idle six-second condition tick or skipped the exact expiry projection.");

                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.PauseRouteTravel, "route.pause"));
                WorldAdvance(simulation, 3600);
                var paused = simulation.Capture().RouteTravels.Single();
                Require(paused.Status == ExpeditionRouteTravelStatus.Paused && paused.Progress == new RuleQuantity(1)
                    && paused.NominalEffort == new RuleTime(14400),
                    "Paused route accrued effort while the shared world clock advanced.");

                // A paused traveler may leave by ordinary world movement. Rejoin is explicit and
                // must reject while away from the exact route-position anchor.
                WorldStep(simulation, 0, -1);
                WorldAdvance(simulation, 3, 2);
                byte[] checkpoint = Bytes(simulation);
                var restored = new Simulation(policy, new SnapshotCodec().Decode(checkpoint), ExecutionProfile.Laboratory);
                Require(checkpoint.SequenceEqual(Bytes(restored))
                    && restored.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2,
                    "Paused off-route state did not round-trip byte-for-byte.");
                RejectUnchanged(restored, host, RouteTravelCommand(restored, CommandKind.ResumeRouteTravel,
                    "route.resume.off-anchor"), "TravelerNotAtBoundRoutePosition");
                WorldStep(restored, 0, 1);
                WorldAdvance(restored, 3, 2);
                PortableCommit(restored, Portable(restored, CommandKind.RemovePortableItem, PortableKitFixture.Pack));
                PortableCommit(restored, Portable(restored, CommandKind.HandlePortableEquipment,
                    PortableKitFixture.Pack, handling: HandlingKind.Drop));
                Require(TestOnlyClubAttackPolicy.WalkingSpeed(restored.Capture(), TestOnlyPolicy.ActorId) == 30
                    && restored.Capture().RouteTravels.Single().NominalEffort == new RuleTime(14400),
                    "Removing the carried pack did not change only future route pace while paused.");

                var resume = RouteTravelCommand(restored, CommandKind.ResumeRouteTravel, "route.resume");
                Require(restored.QueryCommand(host, resume).Admissible, "Route did not resume from its real saved position.");
                WorldCommit(restored, resume);
                WorldAdvance(restored, 10800);
                var complete = restored.Capture();
                var finished = complete.RouteTravels.Single();
                Require(finished.Status == ExpeditionRouteTravelStatus.SegmentComplete
                    && finished.Progress == new RuleQuantity(2)
                    && finished.NominalEffort == new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds)
                    && complete.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 2
                    && complete.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && Crop(restored).Stage == CropStage.Growing,
                    "Route completion, pace change, or management continuity diverged after restore.");
                Require(Bytes(restored).SequenceEqual(Bytes(new Simulation(policy,
                    new SnapshotCodec().Decode(Bytes(restored)), ExecutionProfile.Laboratory))),
                    "Completed route replay through the current policy changed canonical save bytes.");
            });

            cases.Add("expedition_route_rejects_unresolved_risk_quality_mapping_and_capacity", () => {
                void CheckRejected(ExpeditionRouteQuality quality, int risk, ExpeditionRouteMapping mapping,
                    RuleQuantity capacity, string expected)
                {
                    var policy = RouteTravelPolicy(RouteTravelFixture(quality, risk, mapping, capacity));
                    var simulation = World(policy);
                    RouteTravelReachSource(simulation);
                    RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                        "route.reject." + expected), expected);
                }
                CheckRejected(ExpeditionRouteQuality.Secured, 1, ExpeditionRouteMapping.Mapped,
                    new RuleQuantity(10), "RouteRiskResolutionUnsupported");
                CheckRejected(ExpeditionRouteQuality.Known, 0, ExpeditionRouteMapping.Mapped,
                    new RuleQuantity(10), "RouteQualityConsequenceUnsupported");
                CheckRejected(ExpeditionRouteQuality.Secured, 0, ExpeditionRouteMapping.Unknown,
                    new RuleQuantity(10), "RouteRequiresReconnaissance");
                CheckRejected(ExpeditionRouteQuality.Secured, 0, ExpeditionRouteMapping.Mapped,
                    new RuleQuantity(1), "RouteCapacitySettlementUnsupported");
            });

            cases.Add("expedition_route_rejects_partial_terminal_progress_before_play", () => {
                var shortTerminal = new TestOnlyExpeditionRouteFixture(new TestOnlyExpeditionRoute(RouteTravelId,
                    TestOnlyPolicy.ContainerId, TestOnlyCropPolicy.PlotId, 1, 2, 3, 3, new RuleQuantity(1),
                    ExpeditionRouteQuality.Secured, 0, ExpeditionRouteMapping.Mapped, new RuleQuantity(10), new[] {
                        new TestOnlyRoutePositionBinding(default, 1, 2),
                        new TestOnlyRoutePositionBinding(new RuleQuantity(1, 2), 1, 3),
                        new TestOnlyRoutePositionBinding(new RuleQuantity(1), 2, 3)
                    }));
                Throws<InvalidOperationException>(() => World(RouteTravelPolicy(shortTerminal)));
            });

            cases.Add("expedition_route_tactical_entry_pauses_and_preserves_off_anchor_rejoin", () => {
                var policy = RouteTravelPolicy(RouteTravelFixture());
                var simulation = World(policy);
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "route.tactical.start"));
                WorldAdvance(simulation, 27); // leave the actor's saved slot active for tactical displacement.
                var inProgress = simulation.Capture().RouteTravels.Single();
                Require(inProgress.Status == ExpeditionRouteTravelStatus.Moving && inProgress.NominalEffort > default(RuleTime),
                    "Pre-combat route segment did not preserve partial progress.");

                WorldCommit(simulation, IC(simulation, CommandKind.BeginFixedEncounter));
                Require(simulation.Capture().InventoryCombat
                    && simulation.Capture().RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused,
                    "Tactical control did not freeze the active route record.");
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                    stance: (int)CombatStance.Aggressive));
                var displacement = Tac(simulation, CommandKind.TacticalStep, x: 1, y: 3);
                var displacementPreview = simulation.QueryCommand(host, displacement);
                Require(displacementPreview.Supported && displacementPreview.Admissible,
                    "Tactical displacement query failed: " + displacementPreview.Code + ", actor="
                    + displacement.Actor + ", target=" + displacement.Target + ", current="
                    + simulation.Capture().Encounter.CurrentActor + ", position="
                    + simulation.Capture().Actors.Single(x => x.Id == displacement.Actor).X + ","
                    + simulation.Capture().Actors.Single(x => x.Id == displacement.Actor).Y + ", step="
                    + displacement.X + "," + displacement.Y + ".");
                WorldCommit(simulation, displacement);
                Require(simulation.Capture().RouteTravels.Single().Progress == inProgress.Progress
                    && simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3,
                    "Tactical displacement changed route progress or failed to leave its position anchor.");
                TacStep(simulation, 1, 2);
                WorldCommit(simulation, Tac(simulation, CommandKind.DropProne));
                var proneJournal = simulation.Capture().Conditions.Single(x => x.Target == TestOnlyPolicy.ActorId);
                Require(proneJournal.Now.Time == simulation.Capture().RuleClock
                    && proneJournal.Operations.Last().At.Time == simulation.Capture().RuleClock,
                    "A condition applied after route travel used the stale pre-travel journal clock.");
                byte[] saved = Bytes(simulation);
                var restored = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(restored)) && restored.Capture().InventoryCombat
                    && restored.Capture().RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                    && restored.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2,
                    "Combat save/restore lost paused route effort or exact route-anchor rejoin.");
            });

            cases.Add("expedition_route_schema52_retained_encounter_remains_blocking", () => {
                var routes = RouteTravelFixture();
                var policy = new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(1), new SupplyCacheFixture())
                    .EnableExpeditionRouteTravel(routes);
                var simulation = World(policy);
                Require(simulation.Capture().SchemaVersion == Snapshot.ExpeditionRouteSchema,
                    "Route-only compatibility case did not select schema52.");
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "route.schema52.start"));
                WorldCommit(simulation, IC(simulation, CommandKind.BeginFixedEncounter));
                while (simulation.Capture().Encounter.CurrentActor != TestOnlyPolicy.ActorId) ConnectedEnd(simulation);
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                    stance: (int)CombatStance.Aggressive));
                foreach (var position in new[] { new[] { 2, 2 }, new[] { 3, 2 }, new[] { 4, 2 }, new[] { 4, 1 } })
                    TacStep(simulation, position[0], position[1]);
                DefeatConnectedEnemy(simulation);
                WorldCommit(simulation, Tac(simulation, CommandKind.EndFixedEncounter));
                Require(!simulation.Capture().InventoryCombat && simulation.Capture().Encounter != null
                    && simulation.Capture().Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Dead,
                    "Schema52 combat did not retain its resolved encounter record.");
                RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.ResumeRouteTravel,
                    "route.schema52.reject-resume"), "RouteTravelDuringTacticalControl");
            });

            cases.Add("route_observation_fractional_detach_detour_exact_rejoin_and_replay", () => {
                var routes = RouteTravelFixture();
                var policy = RouteObservationPolicy(routes);
                var simulation = World(policy);
                Require(simulation.Capture().SchemaVersion == Snapshot.RouteObservationSchema,
                    "Composed route-motion and observation content did not select schema53.");
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "route.observed.start"));
                WorldAdvance(simulation, 4050); // At 20 ft/speed, secured quality earns 3600 nominal seconds (Progress 1/4).
                var moving = simulation.Capture();
                var movingTravel = moving.RouteTravels.Single();
                var movingPosition = moving.RouteTravelSpatial.Single();
                var visible = moving.ObserverKnowledge.Single(x => x.ObserverId == TestOnlyPolicy.CompanionId
                    && x.TargetId == TestOnlyPolicy.ActorId);
                Require(movingTravel.Progress == new RuleQuantity(1, 4)
                    && moving.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2
                    && movingPosition.X == new RuleQuantity(1) && movingPosition.Y == new RuleQuantity(9, 4)
                    && ObservationRules.KnownLocations(moving, TestOnlyPolicy.CompanionId).Single(x => x.ActorId == TestOnlyPolicy.ActorId).Y
                        == new RuleQuantity(9, 4)
                    && visible.CurrentLocationKnown && visible.LastKnownY == new RuleQuantity(9, 4)
                    && visible.Evidence == ObservationEvidenceKind.DirectSight,
                    "Continuous route pose or route-segment observation did not use exact Progress and shared time.");
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.PauseRouteTravel, "route.observed.pause"));
                RejectUnchanged(simulation, host, IC(simulation, CommandKind.BeginFixedEncounter),
                    "OffGridCombatEntryUnsupported");
                RuleTime detachAt = simulation.Capture().RuleClock;
                RuleTime effortAtDetach = simulation.Capture().RouteTravels.Single().NominalEffort;
                RuleQuantity movementBefore = simulation.Capture().WorldIntervals.Single(x => x.ActorId == TestOnlyPolicy.ActorId).MovementSpent;
                RejectUnchanged(simulation, host, IC(simulation, CommandKind.BeginWorldStep, "walk", x: -1),
                    "RouteDepartureDirectionUnsupported");
                WorldStep(simulation, 0, 1);
                var detached = simulation.Capture();
                Require(detached.RuleClock == detachAt && detached.RouteTravels.Single().NominalEffort == effortAtDetach
                    && detached.WorldIntervals.Single(x => x.ActorId == TestOnlyPolicy.ActorId).MovementSpent == movementBefore
                    && detached.WorldTraversals.Single().DistanceFeet == new RuleQuantity(5, 4)
                    && detached.RouteTravelSpatial.Single().Detached
                    && ObservationRules.KnownLocations(detached, TestOnlyPolicy.CompanionId).Single(x => x.ActorId == TestOnlyPolicy.ActorId).Y
                        == new RuleQuantity(9, 4),
                    "Detaching charged time or displacement, changed route effort, or changed exact physical position.");
                byte[] afterDetach = Bytes(simulation);
                var replay = new Simulation(policy, new SnapshotCodec().Decode(afterDetach), ExecutionProfile.Laboratory);
                Require(afterDetach.SequenceEqual(Bytes(replay)),
                    "Save/restore immediately after route-derived nonzero traversal origin changed canonical bytes.");
                var forgedOffset = new SnapshotCodec().Decode(afterDetach);
                forgedOffset.WorldTraversals = forgedOffset.WorldTraversals.Select(x => x.With(new RuleQuantity(3, 2), x.Status)).ToArray();
                Throws<ArgumentException>(() => new Simulation(policy, forgedOffset, ExecutionProfile.Laboratory));

                void ContinueDetour(Simulation value)
                {
                    WorldAdvance(value, 9, 8); // The seeded 5/4 ft is pre-existing position; only 15/4 ft is paid.
                    WorldStep(value, -1, 0); WorldAdvance(value, 3, 2);
                    WorldStep(value, 1, 0); WorldAdvance(value, 3, 2);
                    WorldStep(value, 0, -1); WorldAdvance(value, 3, 2); // Return to the old integer anchor only.
                    RejectUnchanged(value, host, RouteTravelCommand(value, CommandKind.ResumeRouteTravel,
                        "route.observed.reject-old-anchor"), "TravelerNotAtBoundRoutePosition");
                    WorldStep(value, 0, 1); WorldAdvance(value, 3, 2);
                    WorldStep(value, 0, -1); WorldAdvance(value, 9, 8);
                    WorldCommit(value, IC(value, CommandKind.SuspendWorldStep));
                    var atRejoin = value.Capture();
                    Require(atRejoin.WorldTraversals.Single().Status == WorldTraversalStatus.Suspended
                        && atRejoin.WorldTraversals.Single().DistanceFeet == new RuleQuantity(15, 4)
                        && ObservationRules.KnownLocations(atRejoin, TestOnlyPolicy.CompanionId).Single(x => x.ActorId == TestOnlyPolicy.ActorId).Y
                            == new RuleQuantity(9, 4),
                        "Paid return did not stop at the exact fractional rejoin point.");
                    WorldCommit(value, RouteTravelCommand(value, CommandKind.ResumeRouteTravel, "route.observed.resume"));
                    var rejoined = value.Capture();
                    Require(rejoined.WorldTraversals.Length == 0 && !rejoined.RouteTravelSpatial.Single().Detached
                        && rejoined.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2
                        && ObservationRules.KnownLocations(rejoined, TestOnlyPolicy.CompanionId).Single(x => x.ActorId == TestOnlyPolicy.ActorId).Y
                            == new RuleQuantity(9, 4)
                        && rejoined.RouteTravels.Single().Progress == new RuleQuantity(1, 4),
                        "Reattachment snapped, charged movement, or advanced route effort.");
                }
                ContinueDetour(simulation);
                ContinueDetour(replay);
                Require(Bytes(simulation).SequenceEqual(Bytes(replay)),
                    "Detached traversal save/restore diverged during paid detour, exact rejoin, or replay.");
            });

            cases.Add("route_observation_checkpoint_tactical_entry_detaches_route_pose", () => {
                var routes = RouteTravelFixture(); var policy = RouteObservationPolicy(routes); var simulation = World(policy);
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "route.checkpoint.start"));
                WorldCommit(simulation, IC(simulation, CommandKind.BeginFixedEncounter));
                var checkpoint = simulation.Capture();
                Require(checkpoint.InventoryCombat && checkpoint.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                    && checkpoint.RouteTravelSpatial.Single().Detached
                    && checkpoint.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && checkpoint.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2,
                    "Checkpoint tactical entry did not transfer position authority to ordinary tactical grid state.");
            });

            cases.Add("route_observation_checkpoint_combat_paid_return_resume_and_intake", () => {
                var routes = RouteTravelCheckpointFixture();
                var motion = RouteTravelCheckpointMotionFixture(routes);
                Simulation StartAtRoute(TestOnlySharedWorldPolicy selectedPolicy)
                {
                    var value = World(selectedPolicy);
                    FarmWork(value, CommandKind.PlantCrop); // Companion manages the authored destination plot concurrently.
                    RouteTravelReachSource(value);
                    WorldCommit(value, Portable(value, CommandKind.HandlePortableEquipment, PortableKitFixture.Rations,
                        handling: HandlingKind.Retrieve)); // Carry the meal so destination intake does not borrow cache reach.
                    WorldCommit(value, RouteTravelCommand(value, CommandKind.StartRouteTravel, "route.loop.start"));
                    return value;
                }

                var whole = StartAtRoute(RouteObservationPolicy(routes, enemyHp: 1, motion));
                WorldAdvance(whole, 16200); // One complete 5-foot authored leg at the fixture's burden-adjusted pace.

                var policy = RouteObservationPolicy(routes, enemyHp: 1, motion);
                var simulation = StartAtRoute(policy);
                WorldAdvance(simulation, 5400);
                byte[] midLegSave = Bytes(simulation);
                simulation = new Simulation(policy, new SnapshotCodec().Decode(midLegSave), ExecutionProfile.Laboratory);
                Require(midLegSave.SequenceEqual(Bytes(simulation)), "Mid-leg route save/restore changed the canonical state.");
                WorldAdvance(simulation, 10800);

                var wholeState = whole.Capture();
                var splitState = simulation.Capture();
                var wholeSight = wholeState.ObserverKnowledge.Single(x => x.ObserverId == TestOnlyPolicy.CompanionId
                    && x.TargetId == TestOnlyPolicy.ActorId);
                var splitSight = splitState.ObserverKnowledge.Single(x => x.ObserverId == TestOnlyPolicy.CompanionId
                    && x.TargetId == TestOnlyPolicy.ActorId);
                Require(wholeState.RuleClock == splitState.RuleClock
                    && wholeState.RouteTravels.Single().Progress == new RuleQuantity(1)
                    && wholeState.RouteTravels.Single().Progress == splitState.RouteTravels.Single().Progress
                    && wholeState.RouteTravels.Single().NominalEffort == splitState.RouteTravels.Single().NominalEffort
                    && wholeState.RouteTravelSpatial.Single().X == splitState.RouteTravelSpatial.Single().X
                    && wholeState.RouteTravelSpatial.Single().Y == splitState.RouteTravelSpatial.Single().Y
                    && wholeSight.CurrentLocationKnown == splitSight.CurrentLocationKnown
                    && wholeSight.LastKnownX == splitSight.LastKnownX && wholeSight.LastKnownY == splitSight.LastKnownY
                    && wholeSight.Evidence == splitSight.Evidence && wholeSight.EvidenceAt == splitSight.EvidenceAt
                    && wholeSight.CurrentLocationKnown && wholeSight.LastKnownX == new RuleQuantity(1)
                    && wholeSight.LastKnownY == new RuleQuantity(3) && wholeSight.Evidence == ObservationEvidenceKind.DirectSight,
                    "Whole versus split/save/restore route time changed checkpoint progress, physical pose, or sight evidence.");

                byte[] checkpointSave = Bytes(simulation);
                simulation = new Simulation(policy, new SnapshotCodec().Decode(checkpointSave), ExecutionProfile.Laboratory);
                Require(checkpointSave.SequenceEqual(Bytes(simulation)), "Integer route checkpoint did not restore byte-for-byte.");
                WorldCommit(simulation, IC(simulation, CommandKind.BeginFixedEncounter));
                var encounter = simulation.Capture();
                Require(encounter.InventoryCombat && encounter.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                    && encounter.RouteTravelSpatial.Single().Detached
                    && encounter.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && encounter.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3,
                    "Tactical entry did not transfer the exact checkpoint into shared combat position state.");
                RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.ResumeRouteTravel,
                    "route.loop.resume-during-combat"), "RouteTravelDuringTacticalControl");
                for (int skipped = 0; simulation.Capture().Encounter.CurrentActor != TestOnlyPolicy.ActorId; skipped++)
                {
                    Require(skipped < encounter.Encounter.Order.Count, "Combat initiative did not reach the expedition actor.");
                    ConnectedEnd(simulation);
                }
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                    stance: (int)CombatStance.Aggressive));
                foreach (var position in new[] { new[] { 2, 3 }, new[] { 2, 2 }, new[] { 3, 2 }, new[] { 4, 2 } })
                    TacStep(simulation, position[0], position[1]);
                ConnectedEnd(simulation); // The burden-adjusted tactical movement allowance is 20 feet.
                while (simulation.Capture().Encounter.CurrentActor != TestOnlyPolicy.ActorId) ConnectedEnd(simulation);
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                    stance: (int)CombatStance.Aggressive));
                TacStep(simulation, 4, 1); // Final 5-foot step ends adjacent to the authored enemy at (4,0).
                byte[] displacedCombatSave = Bytes(simulation);
                simulation = new Simulation(policy, new SnapshotCodec().Decode(displacedCombatSave), ExecutionProfile.Laboratory);
                Require(displacedCombatSave.SequenceEqual(Bytes(simulation))
                    && simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 4
                    && simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 1,
                    "Tactical displacement did not survive save/restore at its exact world position: bytes="
                    + displacedCombatSave.SequenceEqual(Bytes(simulation)) + ", actor="
                    + simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X + ","
                    + simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y + ", expected=4,1, encounter="
                    + simulation.Capture().Encounter.CurrentActor + ", route=" + simulation.Capture().RouteTravels.Single().Status
                    + ", detached=" + simulation.Capture().RouteTravelSpatial.Single().Detached + ".");
                DefeatConnectedEnemy(simulation);
                RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.ResumeRouteTravel,
                    "route.loop.resume-before-combat-exit"), "RouteTravelDuringTacticalControl");
                WorldCommit(simulation, Tac(simulation, CommandKind.EndFixedEncounter));
                var exited = simulation.Capture();
                Require(!exited.InventoryCombat && exited.Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Dead
                    && exited.RouteTravels.Single().Progress == new RuleQuantity(1)
                    && exited.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                    && exited.RouteTravelSpatial.Single().Detached
                    && exited.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 4
                    && exited.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 1,
                    "Combat exit reset route progress, failed to retain tactical displacement, or left the conflict unresolved.");
                byte[] exitSave = Bytes(simulation);
                simulation = new Simulation(policy, new SnapshotCodec().Decode(exitSave), ExecutionProfile.Laboratory);
                Require(exitSave.SequenceEqual(Bytes(simulation)), "Resolved combat exit lost the detached route reference on restore.");
                RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.ResumeRouteTravel,
                    "route.loop.resume-from-displaced-position"), "TravelerNotAtBoundRoutePosition");

                foreach (var step in new[] { new[] { -1, 0 }, new[] { 0, 1 }, new[] { -1, 0 }, new[] { -1, 0 }, new[] { 0, 1 } })
                {
                    WorldStep(simulation, step[0], step[1]);
                    WorldAdvance(simulation, 3, 2);
                }
                var returned = simulation.Capture();
                Require(returned.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && returned.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && returned.WorldTraversals.Length == 0 && returned.RouteTravelSpatial.Single().Detached
                    && returned.RouteTravels.Single().Progress == new RuleQuantity(1),
                    "Ordinary paid movement did not return to the exact saved route checkpoint.");
                byte[] returnSave = Bytes(simulation);
                var resumedWhole = new Simulation(policy, new SnapshotCodec().Decode(returnSave), ExecutionProfile.Laboratory);
                var resumedSplit = new Simulation(policy, new SnapshotCodec().Decode(returnSave), ExecutionProfile.Laboratory);
                WorldCommit(resumedWhole, RouteTravelCommand(resumedWhole, CommandKind.ResumeRouteTravel, "route.loop.resume"));
                WorldCommit(resumedSplit, RouteTravelCommand(resumedSplit, CommandKind.ResumeRouteTravel, "route.loop.resume"));
                WorldAdvance(resumedWhole, 16200);
                WorldAdvance(resumedSplit, 5400);
                byte[] resumedMidLegSave = Bytes(resumedSplit);
                resumedSplit = new Simulation(policy, new SnapshotCodec().Decode(resumedMidLegSave), ExecutionProfile.Laboratory);
                Require(resumedMidLegSave.SequenceEqual(Bytes(resumedSplit)),
                    "Post-combat resumed route save/restore changed the canonical state.");
                WorldAdvance(resumedSplit, 10800);
                var wholeResumed = resumedWhole.Capture();
                var splitResumed = resumedSplit.Capture();
                var wholeResumedSight = wholeResumed.ObserverKnowledge.Single(x => x.ObserverId == TestOnlyPolicy.CompanionId
                    && x.TargetId == TestOnlyPolicy.ActorId);
                var splitResumedSight = splitResumed.ObserverKnowledge.Single(x => x.ObserverId == TestOnlyPolicy.CompanionId
                    && x.TargetId == TestOnlyPolicy.ActorId);
                Require(wholeResumed.RuleClock == splitResumed.RuleClock
                    && wholeResumed.RouteTravels.Single().Progress == splitResumed.RouteTravels.Single().Progress
                    && wholeResumed.RouteTravels.Single().NominalEffort == splitResumed.RouteTravels.Single().NominalEffort
                    && wholeResumed.RouteTravelSpatial.Length == splitResumed.RouteTravelSpatial.Length
                    && wholeResumed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X
                        == splitResumed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X
                    && wholeResumed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y
                        == splitResumed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y
                    && wholeResumedSight.CurrentLocationKnown == splitResumedSight.CurrentLocationKnown
                    && wholeResumedSight.LastKnownX == splitResumedSight.LastKnownX
                    && wholeResumedSight.LastKnownY == splitResumedSight.LastKnownY
                    && wholeResumedSight.Evidence == splitResumedSight.Evidence
                    && wholeResumedSight.EvidenceAt == splitResumedSight.EvidenceAt,
                    "Post-combat route continuation changed under split time or save/restore.");
                simulation = resumedSplit;
                var arrived = simulation.Capture();
                Require(arrived.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.SegmentComplete
                    && arrived.RouteTravels.Single().Progress == new RuleQuantity(2)
                    && arrived.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 2
                    && arrived.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && Crop(simulation).Stage == CropStage.Growing,
                    "Route resume failed to complete at its destination while remote crop management continued.");

                var intake = IC(simulation, CommandKind.StartIntake, PortableKitFixture.Rations,
                    new InventoryRequest(new RuleQuantity(2, 3)));
                WorldCommit(simulation, intake);
                WorldAdvance(simulation, 600);
                Require(simulation.Capture().Intakes.Single().Status == IntakeStatus.Complete
                    && Eaten(simulation) == new RuleQuantity(2, 3)
                    && simulation.Capture().RouteTravels.Single().Status == ExpeditionRouteTravelStatus.SegmentComplete,
                    "Destination resource management did not continue on the same clock and persisted route outcome.");

                var nextSegment = RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "route.loop.next-segment");
                var nextSegmentQuery = simulation.QueryCommand(host, nextSegment);
                Require(nextSegmentQuery.Supported && nextSegmentQuery.Admissible,
                    "Resolved encounter history blocked a lawful next route segment: " + nextSegmentQuery.Code);
                WorldCommit(simulation, nextSegment);
                WorldAdvance(simulation, 16200);
                var continuation = simulation.Capture();
                var latestRoute = continuation.RouteTravels.OrderBy(x => x.StartedRevision).Last();
                Require(!continuation.InventoryCombat && continuation.Encounter != null
                    && continuation.Lives.Single(x => x.ActorId == AdditionalTacticalActor.Id).Dead
                    && continuation.RouteTravels.Length == 2
                    && latestRoute.Status == ExpeditionRouteTravelStatus.Moving
                    && latestRoute.Progress == new RuleQuantity(3)
                    && continuation.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 2
                    && continuation.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 4,
                    "Retained resolved combat history paused or rewrote the next route segment.");
                var replay = new Simulation(policy, new SnapshotCodec().Decode(Bytes(simulation)), ExecutionProfile.Laboratory);
                Require(Bytes(simulation).SequenceEqual(Bytes(replay)),
                    "Completed travel, combat, return, resumed route, crop and intake state failed canonical replay.");
            });

            cases.Add("expedition_route_and_observation_profile_composition_fails_closed", () => {
                var observationFirst = new TestOnlySharedWorldPolicy(new SharedCombatFixture())
                    .EnableObservation(RouteTravelObservationFixture());
                Throws<InvalidOperationException>(() => observationFirst.EnableExpeditionRouteTravel(RouteTravelFixture()));
                var routeFirst = RouteTravelPolicy(RouteTravelFixture());
                Throws<InvalidOperationException>(() => routeFirst.EnableObservation(RouteTravelObservationFixture()));

                var restorePolicy = RouteTravelPolicy(RouteTravelFixture());
                var forgedCombined = restorePolicy.Initial();
                forgedCombined.ObservationMapWidth = 5;
                forgedCombined.ObservationMapHeight = 5;
                forgedCombined.ObservationProfiles = forgedCombined.Actors.Select(x =>
                    new ObservationProfileRecord(x.Id, 30, 30)).ToArray();
                Throws<ArgumentException>(() => new Simulation(restorePolicy, forgedCombined, ExecutionProfile.Laboratory));
            });
        }
    }
}
#endif
