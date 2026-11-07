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

        private static TestOnlySharedWorldPolicy RouteTravelPolicy(TestOnlyExpeditionRouteFixture fixture,
            ConditionCombatFixture conditions = null)
            => new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(), new SupplyCacheFixture(),
                conditions: conditions)
                .EnableExpeditionRouteTravel(fixture);

        private static Command RouteTravelCommand(Simulation s, CommandKind kind, string id = "route.command",
            string actor = TestOnlyPolicy.ActorId)
            => new Command(id, actor, s.Capture().Revision, kind, RouteTravelId);

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
