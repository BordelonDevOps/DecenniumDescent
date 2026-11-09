#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Numerics;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string PressureCohortId = "TEST_ONLY.pressure.cohort";
        private const string PressureCampId = "TEST_ONLY.pressure.camp";

        private static TestOnlySharedWorldPolicy PressurePolicy(int initialPressure = 5, uint seed = 1,
            TestOnlyExpeditionRouteFixture routes = null, long enemyHp = 1)
        {
            routes = routes ?? RouteTravelCheckpointFixture();
            return new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp: enemyHp, seed: seed),
                new SupplyCacheFixture()).EnableExpeditionRouteTravel(routes)
                .EnableExpeditionPressure(new TestOnlyExpeditionPressureFixture(PressureCohortId,
                    TestOnlyPolicy.ActorId, initialPressure, new[] { TestOnlyCropPolicy.PlotId }));
        }

        private static TestOnlySharedWorldPolicy PressureCampPolicy(TestOnlyExpeditionCampSiteFixture camp,
            int initialPressure = 5, uint seed = 1, TestOnlyExpeditionRouteFixture routes = null, long enemyHp = 1)
            => PressurePolicy(initialPressure, seed, routes, enemyHp).EnableExpeditionCampUse(camp);

        private static Simulation PressurePrepareCampAtCheckpoint(TestOnlySharedWorldPolicy policy,
            Action<Simulation> afterRouteCheckpoint = null)
        {
            var simulation = World(policy);
            WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId);
            WorldAdvance(simulation, 1);
            PortableCommit(simulation, Portable(simulation, CommandKind.RemovePortableItem, PortableKitFixture.Pack));
            PortableCommit(simulation, Portable(simulation, CommandKind.HandlePortableEquipment,
                PortableKitFixture.Pack, handling: HandlingKind.Drop));
            RouteTravelReachSource(simulation);
            WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                "pressure.camp.route.start"));
            WorldAdvance(simulation, 10800);
            PressurePauseActiveRouteIfMoving(simulation, "pressure.camp.route.pause");
            if (afterRouteCheckpoint != null) afterRouteCheckpoint(simulation);
            var state = simulation.Capture();
            Require(state.RouteTravels.Single().Progress == new RuleQuantity(1)
                && state.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                && state.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                && state.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                && state.ExpeditionCampSites.Single().Id == PressureCampId,
                "The camp fixture did not reach its exact paused physical route checkpoint: route="
                + state.RouteTravels.Single().Status + "/" + state.RouteTravels.Single().Progress
                + "; actor=" + state.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X + ","
                + state.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y + "; siteCount="
                + state.ExpeditionCampSites.Length + "; clock=" + state.RuleClock + ".");
            return simulation;
        }

        private static Command PressureCampCommand(Simulation simulation, CommandKind kind, string suffix)
            => new Command("pressure.camp." + suffix + "." + simulation.Capture().Revision.ToString(CultureInfo.InvariantCulture),
                TestOnlyPolicy.ActorId, simulation.Capture().Revision, kind, PressureCampId);

        private static void PressureCampCommit(Simulation simulation, CommandKind kind, string suffix)
            => WorldCommit(simulation, PressureCampCommand(simulation, kind, suffix));

        private static TestOnlyExpeditionRouteFixture PressureHavenRouteFixture(
            ExpeditionRouteQuality quality = ExpeditionRouteQuality.Secured)
            => new TestOnlyExpeditionRouteFixture(new TestOnlyExpeditionRoute(RouteTravelId,
                TestOnlyPolicy.ContainerId, TestOnlyCropPolicy.PlotId, 1, 2, 3, 3, new RuleQuantity(2),
                quality, 0, ExpeditionRouteMapping.Mapped, new RuleQuantity(10), new[] {
                    new TestOnlyRoutePositionBinding(default, 1, 2),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(1), 1, 3),
                    new TestOnlyRoutePositionBinding(new RuleQuantity(2), 2, 3)
                }));

        private static Simulation PressurePrepareHavenRoute(int initialPressure = 2, uint seed = 1,
            TestOnlyExpeditionRouteFixture routes = null, long enemyHp = 1,
            int schemaVersion = Snapshot.ExpeditionPressureLifecycleSchema)
        {
            routes = routes ?? PressureHavenRouteFixture();
            var policy = PressurePolicy(initialPressure, seed, routes, enemyHp);
            var initial = policy.Initial(); initial.SchemaVersion = schemaVersion;
            var simulation = new Simulation(policy, initial, ExecutionProfile.Laboratory);
            WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId);
            WorldAdvance(simulation, 1);
            PortableCommit(simulation, Portable(simulation, CommandKind.RemovePortableItem, PortableKitFixture.Pack));
            PortableCommit(simulation, Portable(simulation, CommandKind.HandlePortableEquipment,
                PortableKitFixture.Pack, handling: HandlingKind.Drop));
            RouteTravelReachSource(simulation);
            WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "pressure.haven.route.start"));
            return simulation;
        }

        private static void PressurePauseActiveRouteIfMoving(Simulation simulation, string commandId)
        {
            if (simulation.Capture().RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Moving)
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.PauseRouteTravel, commandId));
        }

        private static void PressureAdvanceTo(Simulation simulation, RuleTime target)
        {
            var now = simulation.Capture().RuleClock;
            if (target < now) throw new ArgumentOutOfRangeException(nameof(target));
            var delta = RuleTime.FromFraction((BigInteger)target.Numerator * now.Denominator
                - (BigInteger)now.Numerator * target.Denominator,
                (BigInteger)target.Denominator * now.Denominator);
            if (delta == default) return;
            WorldAdvance(simulation, checked((int)delta.Numerator), checked((int)delta.Denominator));
        }

        private static void PressureWaitForActor(Simulation simulation, string actor)
        {
            for (int i = 0; i < 6 && simulation.Capture().Encounter.CurrentActor != actor; i++) ConnectedEnd(simulation);
            Require(simulation.Capture().Encounter.CurrentActor == actor,
                "Tactical calendar did not offer the requested actor within three rounds: " + actor);
        }

        private static void PressureEnsureStance(Simulation simulation, string actor)
        {
            var state = simulation.Capture();
            if (state.Encounter.CurrentActor != actor) PressureWaitForActor(simulation, actor);
            state = simulation.Capture();
            if (!state.Stances.Any(x => x.ActorId == actor && x.TurnOrdinal == state.Encounter.TurnOrdinal
                && x.ExpiresAt > state.RuleClock))
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance, actor: actor,
                    stance: (int)CombatStance.Aggressive));
        }

        private static void PressureMoveHostileAdjacent(Simulation simulation)
        {
            PressureEnsureStance(simulation, AdditionalTacticalActor.Id);
            foreach (var cell in new[] { new[] { 3, 0 }, new[] { 2, 0 }, new[] { 1, 0 },
                new[] { 0, 0 }, new[] { 0, 1 }, new[] { 0, 2 } })
                WorldCommit(simulation, Tac(simulation, CommandKind.TacticalStep,
                    actor: AdditionalTacticalActor.Id, x: cell[0], y: cell[1]));
            Require(simulation.Capture().Actors.Single(x => x.Id == AdditionalTacticalActor.Id).X == 0
                && simulation.Capture().Actors.Single(x => x.Id == AdditionalTacticalActor.Id).Y == 2,
                "Hostile did not reach an admitted tactical square adjacent to the route-bound traveler.");
            PressureEnsureStance(simulation, AdditionalTacticalActor.Id);
            WorldCommit(simulation, Tac(simulation, CommandKind.AttackUnarmed, TestOnlyPolicy.ActorId,
                actor: AdditionalTacticalActor.Id));
            ConnectedEnd(simulation);
            PressureEnsureStance(simulation, AdditionalTacticalActor.Id);
            WorldCommit(simulation, Tac(simulation, CommandKind.AttackUnarmed, TestOnlyPolicy.ActorId,
                actor: AdditionalTacticalActor.Id));
        }

        private static Simulation PressureCombatAtRouteCheckpoint(int initialPressure = 5, uint seed = 1)
        {
            var policy = PressurePolicy(initialPressure, seed);
            var simulation = World(policy);
            RouteTravelReachSource(simulation);
            WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "pressure.route.start"));
            WorldAdvance(simulation, 16200);
            var beforeEncounter = simulation.Capture();
            var route = beforeEncounter.RouteTravels.Single();
            Require(route.Progress == new RuleQuantity(1) && route.Status == ExpeditionRouteTravelStatus.Moving
                && beforeEncounter.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                && beforeEncounter.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3,
                "Traveler did not reach the authored pressure encounter checkpoint.");
            BeginEncounter(simulation);
            var paused = simulation.Capture();
            Require(paused.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                && paused.RouteTravels.Single().Progress == route.Progress
                && paused.RouteTravels.Single().NominalEffort == route.NominalEffort
                && paused.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                && paused.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3,
                "Encounter entry changed the route-bound travel checkpoint.");
            PressureMoveHostileAdjacent(simulation);
            var attacked = simulation.Capture();
            var actualHostileAttacks = attacked.MeleeAttacks.Where(x => x.AttackerId == AdditionalTacticalActor.Id
                && x.TargetId == TestOnlyPolicy.ActorId).ToArray();
            var sources = attacked.ExpeditionPressureChanges.Where(x => x.Kind == ExpeditionPressureChangeKind.OpenCombat).ToArray();
            Require(actualHostileAttacks.Length >= 2 && sources.Length >= 2
                && actualHostileAttacks.All(a => sources.Any(x => x.SourceId == a.Id
                    && x.SourceRevision == a.Revision && x.At == a.At
                    && x.RouteId == route.RouteId && x.ExposureId == attacked.ExpeditionPressureExposures.Single().Id)),
                "Committed hostile attacks were not linked to the fixed cohort's active route exposure.");
            return simulation;
        }

        private static void PressureResolveEncounterAndResume(Simulation simulation)
        {
            DefeatConnectedEnemy(simulation);
            WorldCommit(simulation, Tac(simulation, CommandKind.EndFixedEncounter));
            Require(!simulation.Capture().InventoryCombat && simulation.Capture().Encounter != null,
                "Resolved combat history was not retained after tactical control ended.");
            var resume = RouteTravelCommand(simulation, CommandKind.ResumeRouteTravel, "pressure.route.resume");
            Require(simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(), resume).Admissible,
                "Resolved combat history stranded the schema67 paused base route.");
            WorldCommit(simulation, resume);
        }

        private static ExpeditionPressureCheckpointRecord PressureAdvanceToFirstCheckpoint(Simulation simulation, bool split)
        {
            if (split)
            {
                PressureAdvanceTo(simulation, new RuleTime(20000));
                PressureAdvanceTo(simulation, new RuleTime(26000));
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
            }
            else PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
            return simulation.Capture().ExpeditionPressureCheckpoints.Single();
        }

        private static void PressureExerciseStandardObstruction(Simulation simulation, bool split)
        {
            var checkpoint = simulation.Capture().ExpeditionPressureCheckpoints.Single();
            Require(checkpoint.Outcome == ExpeditionPressureOutcome.Standard
                && checkpoint.PressureBefore == 5 && checkpoint.StoredPressure == 5 && checkpoint.EffectivePressure == 4
                && checkpoint.CauseIds.Count >= 2 && checkpoint.ReductionIds.Count == 1
                && checkpoint.Natural >= 2 && checkpoint.Natural <= 4 && checkpoint.ModifiedTotal == checkpoint.Natural
                && checkpoint.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction
                && checkpoint.ConsequenceEndsAt == new RuleTime(32400)
                && checkpoint.RouteProgress == simulation.Capture().RouteTravels.Single().Progress,
                "Expected the source-linked attack category, secured-route reduction, TR-13 value and Standard consequence; got P="
                + checkpoint.StoredPressure + ", effective=" + checkpoint.EffectivePressure + ", d6=" + checkpoint.Natural
                + ", outcome=" + checkpoint.Outcome + ".");
            var routeBefore = simulation.Capture().RouteTravels.Single();
            Require(routeBefore.Status == ExpeditionRouteTravelStatus.Paused,
                "Standard pressure consequence did not pause route travel.");
            var resume = RouteTravelCommand(simulation, CommandKind.ResumeRouteTravel, "pressure.obstruction.early-resume");
            var query = simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(), resume);
            Require(query.Supported && !query.Admissible && query.Code == "RouteObstructedByPressure",
                "Timed obstruction did not reject route resumption before its deadline.");

            FarmWork(simulation, CommandKind.PlantCrop);
            if (split)
            {
                WorldAdvance(simulation, 1200);
                WorldAdvance(simulation, 1200);
                WorldAdvance(simulation, 1200);
            }
            else WorldAdvance(simulation, 3600);
            var after = simulation.Capture();
            Require(after.RuleClock == checkpoint.ConsequenceEndsAt.Value
                && after.RouteTravels.Single().Progress == routeBefore.Progress
                && after.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                && Crop(simulation).Stage == CropStage.Growing,
                "Independent companion farming did not advance through the obstruction while route progress stayed fixed.");
            resume = RouteTravelCommand(simulation, CommandKind.ResumeRouteTravel,
                "pressure.obstruction.resume." + (split ? "split" : "whole"));
            query = simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(), resume);
            Require(query.Supported && query.Admissible,
                "Route resumption was not admitted at the exact 60-minute deadline: " + query.Code);
            WorldCommit(simulation, resume);
            WorldAdvance(simulation, 3600);
            Require(simulation.Capture().RouteTravels.Single().Progress > routeBefore.Progress,
                "Route exploration did not continue after the obstruction expired.");
            Require(simulation.Capture().ExpeditionPressureCheckpoints.Single().RouteProgress == routeBefore.Progress,
                "Later route progress rewrote the immutable checkpoint position.");
        }

        private static void AddExpeditionPressureCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            cases.Add("expedition_pressure_settlement_and_fl09_classifier_are_exact", () => {
                Require(ExpeditionPressureRules.Settle(4, true, 9, 0) == 3
                    && ExpeditionPressureRules.Settle(1, false, 4, 2) == 2
                    && ExpeditionPressureRules.Settle(6, true, 0, 0) == 6
                    && ExpeditionPressureRules.EffectiveForRouteCheck(1, ExpeditionRouteQuality.Secured) == 0
                    && ExpeditionPressureRules.EffectiveForRouteCheck(5, ExpeditionRouteQuality.Contested) == 6,
                    "Pressure category aggregation, shared two-credit cap, Risk floor, clamp or TR-13 failed.");
                Require(ExpeditionPressureRules.Classify(0, 0, 0, false) == ExpeditionPressureOutcome.None
                    && ExpeditionPressureRules.Classify(6, 0, 0, false) == ExpeditionPressureOutcome.Severe
                    && ExpeditionPressureRules.Classify(4, 1, 1, false) == ExpeditionPressureOutcome.Severe
                    && ExpeditionPressureRules.Classify(4, 4, 4, false) == ExpeditionPressureOutcome.Standard
                    && ExpeditionPressureRules.Classify(4, 5, 5, false) == ExpeditionPressureOutcome.None
                    && ExpeditionPressureRules.Classify(4, 4, 4, true) == ExpeditionPressureOutcome.Minor,
                    "Unmodified FL-09 natural-one, equality, no-event, auto-Severe or gated Minor branch changed.");
                Throws<ArgumentOutOfRangeException>(() => ExpeditionPressureRules.Settle(1, false, -1, 0));
            });

            cases.Add("expedition_pressure_actual_combat_watch_save_replay_and_standard_obstruction", () => {
                var source = PressureCombatAtRouteCheckpoint();
                string path = Path.Combine(directory, "pressure-before-watch-settlement.ddsave");
                var store = new FileSaveStore();
                store.Save(path, source.Capture());
                byte[] saved = File.ReadAllBytes(path);
                var policy = PressurePolicy();
                var whole = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                var restored = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(whole)) && saved.SequenceEqual(Bytes(restored)),
                    "Pre-Watch actual attack/exposure evidence did not round-trip through persistence.");
                PressureResolveEncounterAndResume(whole);
                PressureResolveEncounterAndResume(restored);
                var checkpoint = PressureAdvanceToFirstCheckpoint(whole, false);
                var replayCheckpoint = PressureAdvanceToFirstCheckpoint(restored, false);
                Require(checkpoint.SameAs(replayCheckpoint) && Bytes(whole).SequenceEqual(Bytes(restored)),
                    "Restored deterministic replay diverged in RNG, pressure, receipts, or complication state.");
                Require(whole.Capture().Receipts.Any(x => x.Id == checkpoint.CommandId
                    && x.Revision == checkpoint.AppliedRevision),
                    "Pressure checkpoint lost its initiating command receipt.");

                var split = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
                PressureResolveEncounterAndResume(split);
                var splitCheckpoint = PressureAdvanceToFirstCheckpoint(split, true);
                Require(checkpoint.At == splitCheckpoint.At && checkpoint.WatchIndex == splitCheckpoint.WatchIndex
                    && checkpoint.RandomBefore == splitCheckpoint.RandomBefore && checkpoint.RandomAfter == splitCheckpoint.RandomAfter
                    && checkpoint.WordsConsumed == splitCheckpoint.WordsConsumed && checkpoint.Natural == splitCheckpoint.Natural
                    && checkpoint.Outcome == splitCheckpoint.Outcome && checkpoint.StoredPressure == splitCheckpoint.StoredPressure
                    && checkpoint.EffectivePressure == splitCheckpoint.EffectivePressure
                    && checkpoint.ConsequenceEndsAt == splitCheckpoint.ConsequenceEndsAt
                    && split.Capture().Receipts.Any(x => x.Id == splitCheckpoint.CommandId
                        && x.Revision == splitCheckpoint.AppliedRevision),
                    "Whole and split RuleClock advances diverged in Watch result, RNG or causal receipt attribution.");
                PressureExerciseStandardObstruction(whole, false);
                PressureExerciseStandardObstruction(restored, false);
                PressureExerciseStandardObstruction(split, true);
                Require(Bytes(whole).SequenceEqual(Bytes(restored)),
                    "The exact same post-save command continuation was not byte-identical after restore.");
            });

            cases.Add("expedition_pressure_automatic_severe_closes_route_and_allows_physical_retreat", () => {
                var simulation = PressureCombatAtRouteCheckpoint(initialPressure: 6);
                var policy = PressurePolicy(initialPressure: 6);
                byte[] precheck = Bytes(simulation);
                var restored = new Simulation(policy, new SnapshotCodec().Decode(precheck), ExecutionProfile.Laboratory);
                PressureResolveEncounterAndResume(simulation);
                PressureResolveEncounterAndResume(restored);
                PressureAdvanceToFirstCheckpoint(simulation, false);
                PressureAdvanceToFirstCheckpoint(restored, false);
                var checkpoint = simulation.Capture().ExpeditionPressureCheckpoints.Single();
                Require(checkpoint.Outcome == ExpeditionPressureOutcome.Severe
                    && checkpoint.StoredPressure == 6 && checkpoint.EffectivePressure == 6
                    && checkpoint.Natural == 0 && checkpoint.WordsConsumed == 0
                    && checkpoint.RandomBefore == checkpoint.RandomAfter
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.RouteClosure
                    && simulation.Capture().RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Terminated
                    && simulation.Capture().RouteTravelSpatial.Length == 0,
                    "Pressure six did not automatically close the route without consuming RNG.");
                var closed = RouteTravelCommand(simulation, CommandKind.StartRouteTravel, "pressure.closed-route");
                var closedQuery = simulation.QueryCommand(host, closed);
                Require(closedQuery.Supported && !closedQuery.Admissible && closedQuery.Code == "RouteClosedByPressure",
                    "Pressure closure left its authored passage traversable.");
                var current = simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                var closedProgress = simulation.Capture().RouteTravels.Single().Progress;
                Require(closedProgress > new RuleQuantity(1) && closedProgress < new RuleQuantity(2)
                    && current.X == 1 && current.Y == 3,
                    "Severe closure did not retain the checkpoint needed for a physical retreat.");
                WorldStep(simulation, 0, -1);
                WorldAdvance(simulation, 3, 2);
                WorldStep(restored, 0, -1);
                WorldAdvance(restored, 3, 2);
                var retreated = simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                Require(retreated.X == 1 && retreated.Y == 2
                    && Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Traveler did not physically retreat along the predeclared existing route path. position="
                    + retreated.X + "," + retreated.Y + "; restored="
                    + restored.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X + ","
                    + restored.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y + "; replayBytes="
                    + Bytes(simulation).SequenceEqual(Bytes(restored)) + "; traversals="
                    + simulation.Capture().WorldTraversals.Length + "; clock=" + simulation.Capture().RuleClock + ".");
            });

            cases.Add("expedition_pressure_zero_boundary_guard_and_no_roll_are_exact", () => {
                var policy = PressurePolicy(initialPressure: 0);
                var simulation = World(policy);
                RouteTravelReachSource(simulation);
                PortableCommit(simulation, Portable(simulation, CommandKind.RemovePortableItem, PortableKitFixture.Pack));
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "pressure.zero.route.start"));
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.PauseRouteTravel,
                    "pressure.zero.route.pause"));
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds * 2 - 1, 2));
                byte[] before = Bytes(simulation);
                var handling = Portable(simulation, CommandKind.HandlePortableEquipment, PortableKitFixture.Pack,
                    handling: HandlingKind.Drop);
                var rejected = simulation.Execute(host, handling);
                Require(rejected.Outcome == Outcome.Rejected && rejected.Code == "TimedHandlingBoundaryUnsupported"
                    && before.SequenceEqual(Bytes(simulation)),
                    "One-second portable boundary guard mismatch: outcome=" + rejected.Outcome + ", code=" + rejected.Code
                    + ", unchanged=" + before.SequenceEqual(Bytes(simulation)) + ", beforeClock="
                    + new SnapshotCodec().Decode(before).RuleClock + ", afterClock=" + simulation.Capture().RuleClock + ".");
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                var checkpoint = simulation.Capture().ExpeditionPressureCheckpoints.Single();
                Require(checkpoint.WatchIndex == 0 && checkpoint.Outcome == ExpeditionPressureOutcome.None
                    && checkpoint.PressureBefore == 0 && checkpoint.StoredPressure == 0 && checkpoint.EffectivePressure == 0
                    && checkpoint.Natural == 0 && checkpoint.WordsConsumed == 0
                    && checkpoint.RandomBefore == checkpoint.RandomAfter
                    && checkpoint.Reason == ExpeditionPressureSettlementReason.WatchEnd,
                    "Pressure zero did not settle the active Watch without a die draw.");
            });

            cases.Add("expedition_pressure_early_haven_settles_once_and_blocks_same_watch_reentry", () => {
                var simulation = PressurePrepareHavenRoute();
                WorldAdvance(simulation, 21600);
                var arrivedAtRouteEnd = simulation.Capture();
                Require(arrivedAtRouteEnd.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.SegmentComplete
                    && arrivedAtRouteEnd.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 2
                    && arrivedAtRouteEnd.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3,
                    "Mapped secured route did not finish at its existing route position before Haven arrival.");
                WorldStep(simulation, 1, 0);
                WorldAdvance(simulation, 1);
                var arrived = simulation.Capture();
                var checkpoint = arrived.ExpeditionPressureCheckpoints.Single();
                Require(arrived.RuleClock < new RuleTime(ExpeditionPressureRules.WatchSeconds)
                    && arrived.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 3
                    && arrived.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && checkpoint.WatchIndex == 0 && checkpoint.Reason == ExpeditionPressureSettlementReason.HavenArrival
                    && checkpoint.PressureBefore == 2 && checkpoint.StoredPressure == 1 && checkpoint.EffectivePressure == 0
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.None
                    && arrived.ExpeditionPressureExposures.Single().EndedAt == arrived.RuleClock,
                    "Early safe-Haven arrival did not settle the actual Watch once or preserve pressure.");
                WorldStep(simulation, -1, 0);
                WorldAdvance(simulation, 1);
                WorldStep(simulation, -1, 0);
                WorldAdvance(simulation, 1);
                WorldStep(simulation, 0, -1);
                WorldAdvance(simulation, 1);
                RejectUnchanged(simulation, host, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "pressure.haven.same-watch-reentry"), "ExpeditionPressureSameWatchRouteReentryUnsupported");
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                Require(simulation.Capture().ExpeditionPressureCheckpoints.Length == 1
                    && ExpeditionPressureRules.Current(simulation.Capture(), PressureCohortId) == 1,
                    "Safe-Haven completion created a duplicate Watch settlement or reset stored Pressure.");
            });

            cases.Add("expedition_pressure_haven_at_watch_end_settles_once_and_survives_restore", () => {
                var policy = PressurePolicy(initialPressure: 2, routes: PressureHavenRouteFixture());
                var simulation = PressurePrepareHavenRoute();
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds - 1));
                WorldStep(simulation, 1, 0);
                WorldAdvance(simulation, 1);
                var arrived = simulation.Capture();
                var checkpoint = arrived.ExpeditionPressureCheckpoints.Single();
                Require(arrived.RuleClock == new RuleTime(ExpeditionPressureRules.WatchSeconds)
                    && arrived.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 3
                    && arrived.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && checkpoint.WatchIndex == 0
                    && checkpoint.Reason == ExpeditionPressureSettlementReason.HavenArrivalAtWatchEnd
                    && checkpoint.PressureBefore == 2 && checkpoint.StoredPressure == 1 && checkpoint.EffectivePressure == 0
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.None
                    && arrived.ExpeditionPressureCheckpoints.Length == 1,
                    "Haven arrival coincident with the Watch end did not use the single exact-boundary settlement.");
                string path = Path.Combine(directory, "pressure-haven-watch-end.ddsave");
                var store = new FileSaveStore();
                store.Save(path, arrived);
                byte[] saved = File.ReadAllBytes(path);
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(restored)), "Exact Haven/Watch-end checkpoint failed its save roundtrip.");
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds * 2));
                PressureAdvanceTo(restored, new RuleTime(ExpeditionPressureRules.WatchSeconds * 2));
                Require(simulation.Capture().ExpeditionPressureCheckpoints.Length == 1
                    && restored.Capture().ExpeditionPressureCheckpoints.Length == 1
                    && ExpeditionPressureRules.Current(restored.Capture(), PressureCohortId) == 1
                    && Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Restored exact-boundary Haven arrival settled twice or changed stored pressure.");
            });

            cases.Add("expedition_pressure_haven_standard_resolves_before_admission_and_restores", () => {
                var routes = PressureHavenRouteFixture();
                var policy = PressurePolicy(initialPressure: 5, seed: 1, routes: routes);
                var simulation = PressurePrepareHavenRoute(initialPressure: 5, seed: 1, routes: routes);
                WorldAdvance(simulation, 21600);
                PressurePauseActiveRouteIfMoving(simulation, "pressure.haven.standard.pause");
                WorldStep(simulation, 1, 0);
                WorldAdvance(simulation, 1);
                var pending = simulation.Capture();
                var checkpoint = pending.ExpeditionPressureCheckpoints.Single();
                var actor = pending.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                Require(actor.X == 2 && actor.Y == 3
                    && checkpoint.Reason == ExpeditionPressureSettlementReason.HavenArrival
                    && checkpoint.Outcome == ExpeditionPressureOutcome.Standard
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction
                    && checkpoint.ConsequenceEndsAt == pending.RuleClock.AddSeconds(3600)
                    && !pending.ExpeditionPressureExposures.Single().EndedAt.HasValue,
                    "A Standard Haven checkpoint admitted the traveler before its 60-minute obstruction: actor="
                    + actor.X + "," + actor.Y + " outcome=" + checkpoint.Outcome + " consequence=" + checkpoint.Consequence
                    + " until=" + checkpoint.ConsequenceEndsAt + " clock=" + pending.RuleClock + " end="
                    + pending.ExpeditionPressureExposures.Single().EndedAt + ".");
                string path = Path.Combine(directory, "pressure-haven-standard-pending.ddsave");
                var store = new FileSaveStore(); store.Save(path, pending);
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                Require(Bytes(restored).SequenceEqual(Bytes(simulation)),
                    "Pending Haven admission did not survive save/restore byte-identically.");
                byte[] pendingBytes = Bytes(simulation);
                var repeatedEntry = IC(simulation, CommandKind.BeginWorldStep, "walk", x: 1, y: 0);
                var repeatedQuery = simulation.QueryCommand(host, repeatedEntry);
                var repeatedResult = simulation.Execute(host, repeatedEntry);
                Require(repeatedQuery.Supported && !repeatedQuery.Admissible
                    && repeatedQuery.Code == "PressureHavenAdmissionPending"
                    && repeatedResult.Outcome == Outcome.Rejected && repeatedResult.Code == repeatedQuery.Code
                    && pendingBytes.SequenceEqual(Bytes(simulation)),
                    "A pending Haven arrival could be duplicated or changed the snapshot on rejection.");
                FarmWork(simulation, CommandKind.PlantCrop);
                FarmWork(restored, CommandKind.PlantCrop);
                PressureAdvanceTo(simulation, checkpoint.ConsequenceEndsAt.Value);
                PressureAdvanceTo(restored, checkpoint.ConsequenceEndsAt.Value);
                var completed = simulation.Capture();
                Require(completed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 3
                    && completed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && completed.ExpeditionPressureExposures.Single().EndedAt == checkpoint.ConsequenceEndsAt
                    && Crop(simulation).Stage == CropStage.Growing
                    && Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Haven admission failed at the exact obstruction deadline or diverged after restore.");
            });

            cases.Add("expedition_pressure_haven_severe_keeps_gate_cell_for_physical_retreat", () => {
                var routes = PressureHavenRouteFixture();
                var simulation = PressurePrepareHavenRoute(initialPressure: 6, seed: 97, routes: routes);
                WorldAdvance(simulation, 21600);
                PressurePauseActiveRouteIfMoving(simulation, "pressure.haven.severe.pause");
                WorldStep(simulation, 1, 0);
                WorldAdvance(simulation, 1);
                var snapshot = simulation.Capture();
                var checkpoint = snapshot.ExpeditionPressureCheckpoints.Single();
                var actor = snapshot.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                Require(actor.X == 2 && actor.Y == 3
                    && checkpoint.Outcome == ExpeditionPressureOutcome.Severe
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.RouteClosure
                    && !snapshot.ExpeditionPressureExposures.Single().EndedAt.HasValue,
                    "A Severe Haven checkpoint finalized arrival or ended exposure before physical retreat.");
                var retreat = IC(simulation, CommandKind.BeginWorldStep, "walk", x: -1, y: 0);
                var retreatQuery = simulation.QueryCommand(host, retreat);
                Require(retreatQuery.Admissible, "Severe gate retreat was rejected: " + retreatQuery.Code
                    + "; actor=" + actor.X + "," + actor.Y + "; routes=" + string.Join(",", snapshot.RouteTravels.Select(x => x.Status))
                    + "; exposureEnd=" + snapshot.ExpeditionPressureExposures.Single().EndedAt + ".");
                WorldCommit(simulation, retreat); WorldAdvance(simulation, 1);
                Require(simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1,
                    "Severe gate closure did not permit retreat along the existing route.");
            });

            cases.Add("expedition_pressure_severe_closure_blocks_tactical_forward_movement", () => {
                var routes = PressureHavenRouteFixture(ExpeditionRouteQuality.Contested);
                var simulation = PressurePrepareHavenRoute(initialPressure: 6, seed: 1, routes: routes);
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                BeginEncounter(simulation);
                PressureEnsureStance(simulation, TestOnlyPolicy.ActorId);
                var forward = Tac(simulation, CommandKind.TacticalStep, actor: TestOnlyPolicy.ActorId, x: 3, y: 3);
                var query = simulation.QueryCommand(host, forward);
                Require(query.Supported && !query.Admissible && query.Code == "PressureRetreatMustFollowClosedRoute",
                    "Tactical movement bypassed the Severe closure: " + query.Code + ".");
                byte[] before = Bytes(simulation);
                var rejected = simulation.Execute(host, forward);
                Require(rejected.Outcome == Outcome.Rejected && rejected.Code == query.Code
                    && before.SequenceEqual(Bytes(simulation)),
                    "Tactical execution did not share the closure query or changed state after rejection.");
            });

            cases.Add("expedition_pressure_retreat_exposure_crosses_watch_and_releases_after_departure", () => {
                var routes = PressureHavenRouteFixture(ExpeditionRouteQuality.Contested);
                var simulation = PressurePrepareHavenRoute(initialPressure: 6, seed: 1, routes: routes);
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                Require(!simulation.Capture().ExpeditionPressureExposures.Single().EndedAt.HasValue,
                    "Severe closure ended route exposure before physical withdrawal.");
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds * 4 - 1, 2));
                var route = routes.Routes.Single();
                var actorBeforeRetreat = simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                var routePosition = route.Positions.SingleOrDefault(x => x.X == actorBeforeRetreat.X && x.Y == actorBeforeRetreat.Y);
                var previousPosition = routePosition == null ? null
                    : route.Positions.Where(x => x.Progress < routePosition.Progress).OrderBy(x => x.Progress).LastOrDefault();
                Require(previousPosition != null, "The Watch crossing fixture must begin at a retreatable route position.");
                WorldStep(simulation, previousPosition.X - actorBeforeRetreat.X, previousPosition.Y - actorBeforeRetreat.Y);
                WorldAdvance(simulation, 1);
                var crossed = simulation.Capture();
                Require(crossed.ExpeditionPressureCheckpoints.Select(x => x.WatchIndex).OrderBy(x => x)
                    .SequenceEqual(new long[] { 0, 1 })
                    && !crossed.ExpeditionPressureExposures.Single().EndedAt.HasValue,
                    "Pressure exposure/checkpoint was not retained across the retreating Watch boundary.");
                var retreatingActor = crossed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                while (retreatingActor.X != route.FromX || retreatingActor.Y != route.FromY)
                {
                    routePosition = route.Positions.SingleOrDefault(x => x.X == retreatingActor.X && x.Y == retreatingActor.Y);
                    previousPosition = routePosition == null ? null
                        : route.Positions.Where(x => x.Progress < routePosition.Progress).OrderBy(x => x.Progress).LastOrDefault();
                    Require(previousPosition != null, "Retreat did not reach the existing route origin.");
                    WorldStep(simulation, previousPosition.X - retreatingActor.X, previousPosition.Y - retreatingActor.Y);
                    WorldAdvance(simulation, 1);
                    retreatingActor = simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                }
                WorldStep(simulation, -1, 0); WorldAdvance(simulation, 1);
                var retreated = simulation.Capture();
                Require(retreated.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 0
                    && retreated.ExpeditionPressureExposures.Single().EndedAt.HasValue
                    && (int)retreated.ExpeditionPressureExposures.Single().EndKind == 4,
                    "Exposure did not end when the traveler physically departed the closed route.");
                var next = IC(simulation, CommandKind.BeginWorldStep, "walk", x: 0, y: -1);
                var query = simulation.QueryCommand(host, next);
                Require(query.Supported && query.Admissible,
                    "A completed retreat left ordinary movement stranded: " + query.Code + ".");
                WorldCommit(simulation, next); WorldAdvance(simulation, 1);
            });

            cases.Add("expedition_pressure_late_watch_attack_reconciles_at_haven_admission_and_next_checkpoint", () => {
                var route = PressureHavenRouteFixture().Routes.Single();
                var continuationRoute = new TestOnlyExpeditionRoute("TEST_ONLY.pressure.follow-up-route",
                    route.FromLocationId, route.ToLocationId, route.FromX, route.FromY, route.ToSiteX, route.ToSiteY,
                    route.LengthProgress, route.Quality, route.Risk, route.Mapping, route.CapacityLoad, route.Positions);
                var routes = new TestOnlyExpeditionRouteFixture(route, continuationRoute);
                var policy = PressurePolicy(initialPressure: 5, seed: 1, routes: routes);
                var simulation = PressurePrepareHavenRoute(initialPressure: 5, seed: 1, routes: routes);
                WorldAdvance(simulation, 21600);
                PressurePauseActiveRouteIfMoving(simulation, "pressure.late-haven.pause");
                WorldStep(simulation, 1, 0); WorldAdvance(simulation, 1);
                var earlyCheckpoint = simulation.Capture().ExpeditionPressureCheckpoints.Single();
                Require(earlyCheckpoint.Outcome == ExpeditionPressureOutcome.Standard
                    && earlyCheckpoint.StoredPressure == 4 && earlyCheckpoint.ReductionIds.Count == 1
                    && !simulation.Capture().ExpeditionPressureExposures.Single().EndedAt.HasValue,
                    "The late-cause scenario did not begin with one immutable Standard Haven checkpoint.");

                BeginEncounter(simulation);
                PressureEnsureStance(simulation, AdditionalTacticalActor.Id);
                foreach (var cell in new[] { new[] { 4, 1 }, new[] { 4, 2 }, new[] { 4, 3 }, new[] { 3, 4 } })
                    WorldCommit(simulation, Tac(simulation, CommandKind.TacticalStep,
                        actor: AdditionalTacticalActor.Id, x: cell[0], y: cell[1]));
                WorldCommit(simulation, Tac(simulation, CommandKind.AttackUnarmed, TestOnlyPolicy.ActorId,
                    actor: AdditionalTacticalActor.Id));
                ConnectedEnd(simulation);
                PressureEnsureStance(simulation, AdditionalTacticalActor.Id);
                WorldCommit(simulation, Tac(simulation, CommandKind.AttackUnarmed, TestOnlyPolicy.ActorId,
                    actor: AdditionalTacticalActor.Id));
                var attacked = simulation.Capture();
                var attackSources = attacked.ExpeditionPressureChanges.Where(x => x.WatchIndex == earlyCheckpoint.WatchIndex
                    && x.Kind == ExpeditionPressureChangeKind.OpenCombat).ToArray();
                Require(attackSources.Length == 2 && earlyCheckpoint.SameAs(attacked.ExpeditionPressureCheckpoints.Single()),
                    "Later duplicate attacks did not remain evidence beside the unchanged early checkpoint.");

                string path = Path.Combine(directory, "pressure-late-haven-attacks.ddsave");
                var store = new FileSaveStore(); store.Save(path, attacked);
                byte[] saved = File.ReadAllBytes(path);
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(restored)), "Late same-Watch attack evidence did not survive save/restore.");
                var nextCheckpoints = new List<ExpeditionPressureCheckpointRecord>();
                int replayIndex = 0;
                foreach (var replay in new[] { simulation, restored })
                {
                    DefeatConnectedEnemy(replay);
                    WorldCommit(replay, Tac(replay, CommandKind.EndFixedEncounter));
                    var admissionDeadline = earlyCheckpoint.ConsequenceEndsAt.Value;
                    if (replayIndex++ == 0) PressureAdvanceTo(replay, admissionDeadline);
                    else
                    {
                        var beforeAdmission = RuleTime.FromFraction(
                            (BigInteger)admissionDeadline.Numerator - (BigInteger)1800 * admissionDeadline.Denominator,
                            admissionDeadline.Denominator);
                        PressureAdvanceTo(replay, beforeAdmission);
                        Require(ExpeditionPressureRules.Current(replay.Capture(), PressureCohortId)
                            == earlyCheckpoint.StoredPressure,
                            "Late pressure reconciled before split advancement reached its due Haven admission.");
                        PressureAdvanceTo(replay, admissionDeadline);
                    }
                    var admitted = replay.Capture();
                    Require(admitted.ExpeditionPressureCheckpoints.Single().SameAs(earlyCheckpoint)
                        && admitted.ExpeditionPressureExposures.Single().EndKind == ExpeditionPressureExposureEndKind.SafeHavenArrival
                        && admitted.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 3
                        && ExpeditionPressureRules.Current(admitted, PressureCohortId) == 5,
                        "Safe-Haven admission did not derive one late category from the original checkpoint arithmetic.");

                    foreach (var step in new[] { new[] { -1, 0 }, new[] { -1, 0 }, new[] { 0, -1 } })
                    {
                        WorldStep(replay, step[0], step[1]); WorldAdvance(replay, 1);
                    }
                    PressureAdvanceTo(replay, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                    var nextRouteStart = new Command("pressure.late-next-watch.route.start", TestOnlyPolicy.ActorId,
                        replay.Capture().Revision, CommandKind.StartRouteTravel, continuationRoute.Id);
                    WorldCommit(replay, nextRouteStart);
                    if (replay.Capture().RouteTravels.Single(x => x.RouteId == continuationRoute.Id).Status
                        == ExpeditionRouteTravelStatus.Moving)
                        WorldCommit(replay, new Command("pressure.late-next-watch.route.pause", TestOnlyPolicy.ActorId,
                            replay.Capture().Revision, CommandKind.PauseRouteTravel, continuationRoute.Id));
                    PressureAdvanceTo(replay, new RuleTime(ExpeditionPressureRules.WatchSeconds * 2));
                    var next = replay.Capture().ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 1);
                    nextCheckpoints.Add(next);
                    Require(next.PressureBefore == 5 && next.StoredPressure == 4 && next.CauseIds.Count == 0
                        && next.ReductionIds.Count == 1,
                        "The reconciled value did not carry into the next checkpoint exactly once.");
                }
                var whole = nextCheckpoints[0]; var split = nextCheckpoints[1];
                Require(whole.At == split.At && whole.PressureBefore == split.PressureBefore
                    && whole.StoredPressure == split.StoredPressure && whole.EffectivePressure == split.EffectivePressure
                    && whole.RandomBefore == split.RandomBefore && whole.RandomAfter == split.RandomAfter
                    && whole.WordsConsumed == split.WordsConsumed && whole.Natural == split.Natural
                    && whole.Outcome == split.Outcome && whole.Consequence == split.Consequence
                    && simulation.Capture().RuleClock == restored.Capture().RuleClock
                    && simulation.Capture().RandomState == restored.Capture().RandomState
                    && ExpeditionPressureRules.Current(simulation.Capture(), PressureCohortId)
                        == ExpeditionPressureRules.Current(restored.Capture(), PressureCohortId),
                    "Whole, split and restored advancement diverged in late-cause carry or the next Watch settlement.");
            });

            cases.Add("expedition_pressure_same_time_attack_and_opportunity_survive_tactical_retreat", () => {
                var routes = PressureHavenRouteFixture(ExpeditionRouteQuality.Contested);
                var policy = PressurePolicy(initialPressure: 6, seed: 1, routes: routes, enemyHp: 26);
                var simulation = PressurePrepareHavenRoute(initialPressure: 6, seed: 1, routes: routes, enemyHp: 26);
                PressurePauseActiveRouteIfMoving(simulation, "pressure.same-time.pause");
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                var closure = simulation.Capture().ExpeditionPressureCheckpoints.Single();
                Require(closure.Outcome == ExpeditionPressureOutcome.Severe
                    && closure.Consequence == ExpeditionPressureConsequenceKind.RouteClosure,
                    "The same-time retreat scenario did not establish a Severe route closure.");
                Require(simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2,
                    "The traveler did not remain at the closed route origin for its tactical retreat.");

                BeginEncounter(simulation);
                PressureEnsureStance(simulation, AdditionalTacticalActor.Id);
                foreach (var cell in new[] { new[] { 3, 0 }, new[] { 2, 0 }, new[] { 1, 0 },
                    new[] { 0, 0 }, new[] { 0, 1 }, new[] { 0, 2 } })
                    WorldCommit(simulation, Tac(simulation, CommandKind.TacticalStep,
                        actor: AdditionalTacticalActor.Id, x: cell[0], y: cell[1]));
                PressureEnsureStance(simulation, TestOnlyPolicy.ActorId);
                WorldCommit(simulation, Tac(simulation, CommandKind.AttackUnarmed, AdditionalTacticalActor.Id,
                    actor: TestOnlyPolicy.ActorId));
                var first = simulation.Capture().MeleeAttacks.Last();
                Require(first.At == simulation.Capture().RuleClock && first.AttackerId == TestOnlyPolicy.ActorId,
                    "The same-time pre-retreat attack was not recorded at the shared RuleClock.");
                WorldCommit(simulation, Tac(simulation, CommandKind.TacticalStep, actor: TestOnlyPolicy.ActorId, x: 2, y: 2));
                var pending = TestOnlyClubAttackPolicy.PendingMove(simulation.Capture());
                Require(pending != null && pending.Reactors.Contains(AdditionalTacticalActor.Id),
                    "The off-route departure did not produce its opportunity attack.");
                WorldCommit(simulation, Tac(simulation, CommandKind.RespondOpportunityAttack, pending.Id,
                    AdditionalTacticalActor.Id, weapon: CombatProfileIds.OrdinaryUnarmed, choice: true));

                var retreated = simulation.Capture();
                var exposure = retreated.ExpeditionPressureExposures.Single();
                var opportunity = retreated.MeleeAttacks.Single(x => x.Opportunity);
                var sources = retreated.ExpeditionPressureChanges.Where(x => x.Kind == ExpeditionPressureChangeKind.OpenCombat
                    && new[] { first.Id, opportunity.Id }.Contains(x.SourceId, StringComparer.Ordinal)).ToArray();
                Require(retreated.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 2
                    && retreated.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 2
                    && exposure.EndKind == ExpeditionPressureExposureEndKind.RetreatCompleted
                    && opportunity.At == exposure.EndedAt && opportunity.Revision == exposure.EndRevision
                    && first.At == exposure.EndedAt && first.Revision < exposure.EndRevision
                    && sources.Length == 2,
                    "Same-time attack history or the departure opportunity was lost at exposure completion.");
                string path = Path.Combine(directory, "pressure-same-time-retreat.ddsave");
                var store = new FileSaveStore(); store.Save(path, retreated);
                byte[] saved = File.ReadAllBytes(path);
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(restored)),
                    "Same-time tactical retreat attack history failed canonical save/restore replay.");
            });

            cases.Add("expedition_pressure_multi_watch_single_command_partition_and_restore", () => {
                foreach (var schema in new[] { Snapshot.ExpeditionPressureSchema,
                    Snapshot.ExpeditionPressureLifecycleSchema })
                {
                    var routes = PressureHavenRouteFixture();
                    var policy = PressurePolicy(initialPressure: 5, seed: 1, routes: routes);
                    var whole = PressurePrepareHavenRoute(initialPressure: 5, seed: 1, routes: routes,
                        schemaVersion: schema);
                    var split = PressurePrepareHavenRoute(initialPressure: 5, seed: 1, routes: routes,
                        schemaVersion: schema);
                    PressurePauseActiveRouteIfMoving(whole, "pressure.inflight.whole.pause");
                    PressurePauseActiveRouteIfMoving(split, "pressure.inflight.split.pause");
                    foreach (var branch in new[] { whole, split })
                    {
                        var before = branch.Capture();
                        Require(before.ExpeditionPressureChanges.Count(x => x.WatchIndex == 0
                            && x.Kind == ExpeditionPressureChangeKind.SecuredRouteEntry) == 1
                            && !before.ExpeditionPressureExposures.Single().EndedAt.HasValue,
                            "The partition-invariance fixture needs one secured-entry reduction and an open exposure.");
                    }

                    var twoWatches = new RuleTime(ExpeditionPressureRules.WatchSeconds * 2);
                    PressureAdvanceTo(whole, twoWatches);
                    PressureAdvanceTo(split, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                    var firstBoundary = split.Capture();
                    var firstCheckpoint = firstBoundary.ExpeditionPressureCheckpoints.Single();
                    Require(firstCheckpoint.StoredPressure == 4,
                        "The first Watch did not preserve the one secured-entry reduction.");

                    string path = Path.Combine(directory, "pressure-inflight-schema-" + schema.ToString(CultureInfo.InvariantCulture) + ".ddsave");
                    var store = new FileSaveStore(); store.Save(path, firstBoundary);
                    var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                    Require(File.ReadAllBytes(path).SequenceEqual(Bytes(restored)),
                        "Split first-Watch checkpoint did not restore canonically.");
                    PressureAdvanceTo(split, twoWatches);
                    PressureAdvanceTo(restored, twoWatches);

                    var wholeState = whole.Capture();
                    var wholeCheckpoints = wholeState.ExpeditionPressureCheckpoints.OrderBy(x => x.WatchIndex).ToArray();
                    var splitCheckpoints = split.Capture().ExpeditionPressureCheckpoints.OrderBy(x => x.WatchIndex).ToArray();
                    var restoredCheckpoints = restored.Capture().ExpeditionPressureCheckpoints.OrderBy(x => x.WatchIndex).ToArray();
                    Require(wholeCheckpoints.Length == 2 && splitCheckpoints.Length == 2 && restoredCheckpoints.Length == 2,
                        "A single or split advancement did not settle both Watch boundaries.");
                    for (int i = 0; i < 2; i++)
                    {
                        var a = wholeCheckpoints[i]; var b = splitCheckpoints[i]; var c = restoredCheckpoints[i];
                        Require(a.WatchIndex == i && b.WatchIndex == i && c.WatchIndex == i
                            && a.At == b.At && a.At == c.At && a.PressureBefore == b.PressureBefore
                            && a.PressureBefore == c.PressureBefore && a.StoredPressure == b.StoredPressure
                            && a.StoredPressure == c.StoredPressure && a.EffectivePressure == b.EffectivePressure
                            && a.EffectivePressure == c.EffectivePressure && a.RandomBefore == b.RandomBefore
                            && a.RandomBefore == c.RandomBefore && a.RandomAfter == b.RandomAfter
                            && a.RandomAfter == c.RandomAfter && a.WordsConsumed == b.WordsConsumed
                            && a.WordsConsumed == c.WordsConsumed && a.Natural == b.Natural && a.Natural == c.Natural
                            && a.Outcome == b.Outcome && a.Outcome == c.Outcome && a.Consequence == b.Consequence
                            && a.Consequence == c.Consequence
                            && a.CauseIds.SequenceEqual(b.CauseIds, StringComparer.Ordinal)
                            && a.CauseIds.SequenceEqual(c.CauseIds, StringComparer.Ordinal)
                            && a.ReductionIds.SequenceEqual(b.ReductionIds, StringComparer.Ordinal)
                            && a.ReductionIds.SequenceEqual(c.ReductionIds, StringComparer.Ordinal),
                            "Whole, split and restored Watch checkpoint history diverged for schema " + schema + ".");
                    }
                    Require(wholeCheckpoints[1].PressureBefore == wholeCheckpoints[0].StoredPressure
                        && splitCheckpoints[1].PressureBefore == splitCheckpoints[0].StoredPressure
                        && restoredCheckpoints[1].PressureBefore == restoredCheckpoints[0].StoredPressure
                        && wholeState.RuleClock == twoWatches && split.Capture().RuleClock == twoWatches
                        && restored.Capture().RuleClock == twoWatches
                        && wholeState.RandomState == split.Capture().RandomState
                        && wholeState.RandomState == restored.Capture().RandomState,
                        "The prior in-flight checkpoint was not carried once with matching RNG and clock state.");

                    string wholePath = Path.Combine(directory, "pressure-inflight-whole-schema-"
                        + schema.ToString(CultureInfo.InvariantCulture) + ".ddsave");
                    store.Save(wholePath, wholeState);
                    var wholeRestored = new Simulation(policy, store.Load(wholePath), ExecutionProfile.Laboratory);
                    Require(File.ReadAllBytes(wholePath).SequenceEqual(Bytes(wholeRestored))
                        && Bytes(split).SequenceEqual(Bytes(restored)),
                        "Whole-command replay or split/restored replay did not remain canonical for schema " + schema + ".");
                }
            });

            cases.Add("expedition_camp_unrelated_companion_traversal_preserves_active_use_and_low_restore", () => {
                var site = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                    new RuleQuantity(1), concealed: true);
                var policy = PressureCampPolicy(site, initialPressure: 2);
                var simulation = PressurePrepareCampAtCheckpoint(policy);
                PressureCampCommit(simulation, CommandKind.BeginCampUse, "companion-traversal.use");
                PressureCampCommit(simulation, CommandKind.BeginLyingLow, "companion-traversal.low");
                string path = Path.Combine(directory, "camp-companion-traversal-before.ddsave");
                var store = new FileSaveStore();
                store.Save(path, simulation.Capture());
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                var step = IC(simulation, CommandKind.BeginWorldStep, "walk", actor: TestOnlyPolicy.CompanionId, x: 1);
                var query = simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(), step);
                var result = simulation.Execute(TestOnlySharedWorldPolicy.Host(), step);
                bool companionTraversalStarted = simulation.Capture().WorldTraversals.Any(x =>
                    x.ActorId == TestOnlyPolicy.CompanionId);
                Require(query.Supported && query.Admissible && result.Outcome == Outcome.Committed,
                    "A non-cohort companion traversal was rejected while the expedition remained at camp: query="
                    + query.Code + "; result=" + result.Outcome + "/" + result.Code + ".");
                Require(companionTraversalStarted,
                    "The accepted companion step did not persist an active traversal while camp use remained active.");
                WorldAdvance(simulation, 1);
                var replay = restored.Execute(TestOnlySharedWorldPolicy.Host(), step);
                Require(replay.Outcome == Outcome.Committed, "Restored companion traversal did not replay: " + replay.Code);
                WorldAdvance(restored, 1);
                byte[] afterTraversal = Bytes(simulation);
                var duplicate = simulation.Execute(TestOnlySharedWorldPolicy.Host(), step);
                Require(duplicate.Outcome == Outcome.Duplicate && afterTraversal.SequenceEqual(Bytes(simulation))
                    && Bytes(simulation).SequenceEqual(Bytes(restored))
                    && simulation.Capture().ExpeditionCampActivities.Where(x => x.Kind == ExpeditionCampActivityKind.Use
                        || x.Kind == ExpeditionCampActivityKind.LyingLow).All(x => x.Active),
                    "Companion movement changed cohort camp use/lying-low or diverged after save/restore and command replay: duplicate="
                    + duplicate.Outcome + "; mainPos=" + simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.CompanionId).X
                    + "," + simulation.Capture().Actors.Single(x => x.Id == TestOnlyPolicy.CompanionId).Y
                    + "; activity=" + string.Join(",", simulation.Capture().ExpeditionCampActivities.Where(x =>
                        x.Kind == ExpeditionCampActivityKind.Use || x.Kind == ExpeditionCampActivityKind.LyingLow)
                        .Select(x => x.Kind + "/" + x.Active + "/" + x.EndReason))
                    + "; duplicateStable=" + afterTraversal.SequenceEqual(Bytes(simulation))
                    + "; restoredEqual=" + Bytes(simulation).SequenceEqual(Bytes(restored)) + ".");
            });

            cases.Add("expedition_camp_severe_closure_accepts_tactical_turn_clock_receipt", () => {
                var site = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                    new RuleQuantity(1), exposed: true);
                var policy = PressureCampPolicy(site, initialPressure: 6, seed: 1);
                var simulation = PressurePrepareCampAtCheckpoint(policy);
                var boundary = new RuleTime(ExpeditionPressureRules.WatchSeconds);
                PressureAdvanceTo(simulation, new RuleTime(boundary.Numerator - 2));
                PressureCampCommit(simulation, CommandKind.BeginCampUse, "turn-closure.use");
                BeginEncounter(simulation);
                PressureEnsureStance(simulation, simulation.Capture().Encounter.CurrentActor);
                string path = Path.Combine(directory, "camp-tactical-closure-before.ddsave");
                var store = new FileSaveStore();
                store.Save(path, simulation.Capture());
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                var turn = Tac(simulation, CommandKind.EndRegularTurn);
                var query = simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(), turn);
                var first = simulation.Execute(TestOnlySharedWorldPolicy.Host(), turn);
                var second = restored.Execute(TestOnlySharedWorldPolicy.Host(), turn);
                var state = simulation.Capture();
                Require(state.ExpeditionPressureCheckpoints.Length == 1,
                    "Tactical turn did not reach the expected Severe Watch checkpoint: query=" + query.Code
                    + "; result=" + first.Outcome + "/" + first.Code + "; clock=" + state.RuleClock
                    + "; slot=" + state.WorldSchedule.ProcessedSlot + "; checkpointCount="
                    + state.ExpeditionPressureCheckpoints.Length + ".");
                var checkpoint = state.ExpeditionPressureCheckpoints.Single();
                var use = state.ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.Use);
                Require(query.Supported && query.Admissible && first.Outcome == Outcome.Committed
                    && second.Outcome == Outcome.Committed && state.RuleClock == boundary
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.RouteClosure
                    && use.EndReason == ExpeditionCampActivityEndReason.PressureClosure
                    && use.EndCommandId == turn.Id && use.EndedAt == boundary
                    && Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "A tactical turn ending at the Severe Watch boundary did not close camp use against its exact clock receipt: query="
                    + query.Code + "; result=" + first.Outcome + "/" + first.Code + "; consequence="
                    + checkpoint.Consequence + "; end=" + use.EndReason + "/" + use.EndCommandId + ".");
                var duplicate = restored.Execute(TestOnlySharedWorldPolicy.Host(), turn);
                Require(duplicate.Outcome == Outcome.Duplicate && Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Tactical turn receipt replay changed the persisted camp closure.");
            });

            cases.Add("expedition_camp_movement_encounter_entry_interrupts_low_and_replays", () => {
                var site = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                    new RuleQuantity(1), concealed: true);
                var policy = PressureCampPolicy(site, initialPressure: 2);
                var simulation = PressurePrepareCampAtCheckpoint(policy, world => {
                    foreach (var step in new[] { new[] { -1, 0 }, new[] { -1, 0 }, new[] { -1, 0 }, new[] { 0, 1 } })
                    {
                        WorldStep(world, step[0], step[1], actor: AdditionalTacticalActor.Id);
                        Require(!world.Capture().InventoryCombat,
                            "Test fixture entered tactical control while positioning the hostile at "
                            + world.Capture().Actors.Single(x => x.Id == AdditionalTacticalActor.Id).X + ","
                            + world.Capture().Actors.Single(x => x.Id == AdditionalTacticalActor.Id).Y + ".");
                        WorldAdvance(world, 1);
                    }
                    var hostile = world.Capture().Actors.Single(x => x.Id == AdditionalTacticalActor.Id);
                    Require(hostile.X == 1 && hostile.Y == 1,
                        "Hostile was not staged two cells from the party before the encounter trigger: "
                        + hostile.X + "," + hostile.Y + ".");
                });
                PressureCampCommit(simulation, CommandKind.BeginCampUse, "world-entry.use");
                PressureCampCommit(simulation, CommandKind.BeginLyingLow, "world-entry.low");
                string path = Path.Combine(directory, "camp-world-entry-before.ddsave");
                var store = new FileSaveStore();
                store.Save(path, simulation.Capture());
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                var step = IC(simulation, CommandKind.BeginWorldStep, "walk", actor: AdditionalTacticalActor.Id, y: 1);
                var query = simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(), step);
                var result = simulation.Execute(TestOnlySharedWorldPolicy.Host(), step);
                var state = simulation.Capture();
                var use = state.ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.Use);
                var low = state.ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.LyingLow);
                Require(query.Supported && query.Admissible && query.Code == "EncounterTransition"
                    && result.Outcome == Outcome.Committed && state.InventoryCombat
                    && use.Active && low.EndReason == ExpeditionCampActivityEndReason.Combat
                    && low.EndCommandId == step.Id && low.EndedAt == state.RuleClock,
                    "Movement-triggered combat did not interrupt lying-low while preserving camp occupancy: query="
                    + query.Code + "; result=" + result.Outcome + "/" + result.Code + "; low=" + low.EndReason + ".");
                var replay = restored.Execute(TestOnlySharedWorldPolicy.Host(), step);
                Require(replay.Outcome == Outcome.Committed && Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Movement-triggered camp interruption did not restore/replay deterministically: " + replay.Code + ".");
            });

            cases.Add("expedition_camp_known_use_and_actual_combat_are_distinct_pressure_categories", () => {
                var blockedSite = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                    new RuleQuantity(1), legalAccess: false, knownToEnemies: true);
                var blockedPolicy = PressureCampPolicy(blockedSite, initialPressure: 6);
                var blocked = PressurePrepareCampAtCheckpoint(blockedPolicy);
                var blockedCommand = PressureCampCommand(blocked, CommandKind.BeginCampUse, "blocked");
                byte[] beforeBlocked = Bytes(blocked);
                var blockedQuery = blocked.QueryCommand(TestOnlySharedWorldPolicy.Host(), blockedCommand);
                var blockedResult = blocked.Execute(TestOnlySharedWorldPolicy.Host(), blockedCommand);
                Require(blockedQuery.Supported && !blockedQuery.Admissible
                    && blockedQuery.Code == "CampSiteAccessBlockedOrUnsuitable"
                    && blockedResult.Outcome == Outcome.Rejected && blockedResult.Code == blockedQuery.Code
                    && beforeBlocked.SequenceEqual(Bytes(blocked)),
                    "An explicitly inaccessible camp profile passed preflight or changed state: query="
                    + blockedQuery.Supported + "/" + blockedQuery.Admissible + "/" + blockedQuery.Code
                    + "; result=" + blockedResult.Outcome + "/" + blockedResult.Code
                    + "; bytesEqual=" + beforeBlocked.SequenceEqual(Bytes(blocked)) + ".");

                var campSite = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                    new RuleQuantity(1), knownToEnemies: true);
                var policy = PressureCampPolicy(campSite, initialPressure: 6, enemyHp: 1);
                var simulation = PressurePrepareCampAtCheckpoint(policy);
                var firstBegin = PressureCampCommand(simulation, CommandKind.BeginCampUse, "known.begin.first");
                var beginQuery = simulation.QueryCommand(TestOnlySharedWorldPolicy.Host(), firstBegin);
                Require(beginQuery.Supported && beginQuery.Admissible,
                    "An accessible exact-checkpoint camp did not pass command preflight: " + beginQuery.Code);
                WorldCommit(simulation, firstBegin);
                byte[] afterFirstBegin = Bytes(simulation);
                var duplicate = simulation.Execute(TestOnlySharedWorldPolicy.Host(), firstBegin);
                Require(duplicate.Outcome == Outcome.Duplicate && afterFirstBegin.SequenceEqual(Bytes(simulation)),
                    "Repeated camp-use command replay changed the committed activity or its receipt.");
                WorldAdvance(simulation, 1);
                PressureCampCommit(simulation, CommandKind.EndCampUse, "known.end.first");
                PressureCampCommit(simulation, CommandKind.BeginCampUse, "known.begin.second");
                WorldAdvance(simulation, 1);
                BeginEncounter(simulation);
                PressureMoveHostileAdjacent(simulation);
                DefeatConnectedEnemy(simulation);
                WorldCommit(simulation, Tac(simulation, CommandKind.EndFixedEncounter));
                Require(simulation.Capture().ExpeditionCampActivities.Any(x => x.Kind == ExpeditionCampActivityKind.Use
                    && x.Active) && simulation.Capture().RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused,
                    "Combat incorrectly ended physical camp occupancy or moved the paused expedition route.");

                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                var state = simulation.Capture();
                var checkpoint = state.ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 0);
                var campEvidence = state.ExpeditionPressureChanges.Where(x => x.WatchIndex == 0
                    && x.Kind == ExpeditionPressureChangeKind.ExposedCampUse).ToArray();
                var combatEvidence = state.ExpeditionPressureChanges.Where(x => x.WatchIndex == 0
                    && x.Kind == ExpeditionPressureChangeKind.OpenCombat).ToArray();
                var pressureKinds = state.ExpeditionPressureChanges.Where(x => x.WatchIndex == 0
                    && (x.Kind == ExpeditionPressureChangeKind.ExposedCampUse
                        || x.Kind == ExpeditionPressureChangeKind.OpenCombat)).Select(x => x.Kind).Distinct().ToArray();
                Require(campEvidence.Length == 2 && combatEvidence.Length >= 2 && pressureKinds.Length == 2
                    && campEvidence.All(x => checkpoint.CauseIds.Contains(x.Id))
                    && combatEvidence.All(x => checkpoint.CauseIds.Contains(x.Id))
                    && checkpoint.PressureBefore == 6 && checkpoint.StoredPressure == 6
                    && checkpoint.Context == ExpeditionPressureCheckpointContext.Camp
                    && checkpoint.EffectivePressure == 6 && checkpoint.Outcome == ExpeditionPressureOutcome.Severe
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.RouteClosure
                    && state.ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.Use
                        && x.Active == false && x.EndReason == ExpeditionCampActivityEndReason.PressureClosure).EndedAt
                        == checkpoint.At,
                    "Repeated known-site use and separate actual combat did not settle as two source categories, clamp to Severe, and close occupancy at the exact checkpoint.");
                WorldStep(simulation, 0, -1);
                WorldAdvance(simulation, 3, 2);
                WorldStep(simulation, 0, -1);
                WorldAdvance(simulation, 1);
                var retreated = simulation.Capture();
                Require(retreated.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && retreated.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 1
                    && retreated.ExpeditionPressureExposures.Single().EndKind == ExpeditionPressureExposureEndKind.RetreatCompleted
                    && retreated.ExpeditionPressureCheckpoints.Length == 1
                    && retreated.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.ExposedCampUse
                        && x.WatchIndex == 0) == 2,
                    "Severe camp Pressure did not preserve physical retreat on the existing path without duplicating its checkpoint or camp category: actor="
                    + retreated.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X + ","
                    + retreated.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y + "; exposure="
                    + retreated.ExpeditionPressureExposures.Single().EndKind + "; checkpoints="
                    + retreated.ExpeditionPressureCheckpoints.Length + "; campRows="
                    + retreated.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.ExposedCampUse
                        && x.WatchIndex == 0) + "; traversal="
                    + string.Join(",", retreated.WorldTraversals.Select(x => x.Status + ":" + x.DistanceFeet)) + ".");
            });

            cases.Add("expedition_camp_exposed_pressure_context_and_companion_farming_connect", () => {
                var campSite = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                    new RuleQuantity(1), exposed: true);
                var policy = PressureCampPolicy(campSite, initialPressure: 5, seed: 1);
                var simulation = PressurePrepareCampAtCheckpoint(policy);
                PressureCampCommit(simulation, CommandKind.BeginCampUse, "exposed.begin");
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                var checkpoint = simulation.Capture().ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 0);
                Require(checkpoint.PressureBefore == 5 && checkpoint.StoredPressure == 5
                    && checkpoint.Context == ExpeditionPressureCheckpointContext.Camp
                    && checkpoint.EffectivePressure == 5
                    && checkpoint.EffectivePressure != ExpeditionPressureRules.EffectiveForRouteCheck(
                        checkpoint.StoredPressure, checkpoint.RouteQuality)
                    && checkpoint.Outcome == ExpeditionPressureOutcome.Standard
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction
                    && checkpoint.CauseIds.Count == 1 && checkpoint.ReductionIds.Count == 1
                    && simulation.Capture().ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.Use).Active,
                    "Exposed camp use did not raise one category or use the camp Pressure context at Watch-end.");
                FarmWork(simulation, CommandKind.PlantCrop);
                PressureAdvanceTo(simulation, checkpoint.ConsequenceEndsAt.Value);
                var completed = simulation.Capture();
                Require(Crop(simulation).Stage == CropStage.Growing
                    && completed.Work.WorkerIntervals.Any(x => x.WorkerId == TestOnlyPolicy.CompanionId
                        && x.Start == checkpoint.At && x.End <= checkpoint.ConsequenceEndsAt.Value)
                    && completed.RouteTravels.Single().Status == ExpeditionRouteTravelStatus.Paused
                    && completed.ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.Use).Active,
                    "The companion did not finish farming during the timed route obstruction while camp occupancy and the exploration position persisted.");
            });

            cases.Add("expedition_camp_early_haven_uses_route_context_and_does_not_settle_twice", () => {
                var routes = PressureHavenRouteFixture();
                var campSite = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                    new RuleQuantity(1), exposed: true);
                var policy = PressureCampPolicy(campSite, initialPressure: 5, seed: 1, routes: routes);
                var simulation = PressurePrepareCampAtCheckpoint(policy);
                PressureCampCommit(simulation, CommandKind.BeginCampUse, "haven.use.begin");
                WorldAdvance(simulation, 1);
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.ResumeRouteTravel,
                    "camp.haven.route.resume"));
                var afterLeaving = simulation.Capture().ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.Use);
                Require(afterLeaving.EndedAt == simulation.Capture().RuleClock
                    && afterLeaving.EndReason == ExpeditionCampActivityEndReason.Travel,
                    "Leaving the authored camp did not end actual use on the route-resume receipt.");
                WorldAdvance(simulation, 10800);
                Require(simulation.Capture().RouteTravels.Single().Progress == new RuleQuantity(2),
                    "The Haven scenario did not reach the authored route endpoint.");
                WorldStep(simulation, 1, 0);
                WorldAdvance(simulation, 1);
                var early = simulation.Capture();
                var checkpoint = early.ExpeditionPressureCheckpoints.Single();
                Require(early.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 2
                    && early.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && checkpoint.WatchIndex == 0 && checkpoint.Reason == ExpeditionPressureSettlementReason.HavenArrival
                    && checkpoint.Context == ExpeditionPressureCheckpointContext.Route
                    && checkpoint.PressureBefore == 5 && checkpoint.StoredPressure == 5
                    && checkpoint.EffectivePressure == 4 && checkpoint.CauseIds.Count == 1
                    && checkpoint.ReductionIds.Count == 1
                    && checkpoint.Consequence == ExpeditionPressureConsequenceKind.TimedRouteObstruction
                    && early.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.ExposedCampUse
                        && x.WatchIndex == 0) == 1
                    && !early.ExpeditionPressureExposures.Single().EndedAt.HasValue,
                    "Early Haven settlement did not preserve route context, one real camp-use source, and its single pending Standard consequence: actor="
                    + early.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X + ","
                    + early.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y + "; watch/context="
                    + checkpoint.WatchIndex + "/" + checkpoint.Context + "; pressure=" + checkpoint.PressureBefore
                    + "/" + checkpoint.StoredPressure + "/" + checkpoint.EffectivePressure + "; causes/reductions="
                    + checkpoint.CauseIds.Count + "/" + checkpoint.ReductionIds.Count + "; outcome/consequence="
                    + checkpoint.Outcome + "/" + checkpoint.Consequence + "; campRows="
                    + early.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.ExposedCampUse
                        && x.WatchIndex == 0) + "; exposureEnd=" + early.ExpeditionPressureExposures.Single().EndedAt
                    + "; clock=" + early.RuleClock + "; routeStatus=" + early.RouteTravels.Single().Status
                    + "; traversal=" + string.Join(",", early.WorldTraversals.Select(x => x.Status + ":" + x.DistanceFeet)) + ".");
                PressureAdvanceTo(simulation, checkpoint.ConsequenceEndsAt.Value);
                var admitted = simulation.Capture();
                Require(checkpoint.SameAs(admitted.ExpeditionPressureCheckpoints.Single())
                    && admitted.ExpeditionPressureCheckpoints.Length == 1
                    && admitted.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.ExposedCampUse
                        && x.WatchIndex == 0) == 1
                    && admitted.ExpeditionPressureExposures.Single().EndKind == ExpeditionPressureExposureEndKind.SafeHavenArrival
                    && admitted.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 3
                    && admitted.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && ExpeditionPressureRules.Current(admitted, PressureCohortId) == checkpoint.StoredPressure,
                    "The actual Haven admission duplicated its earlier checkpoint/source or changed its Pressure settlement.");
            });

            cases.Add("expedition_camp_concealed_full_watch_lie_low_saves_replays_and_requires_unbroken_coverage", () => {
                var campSite = new TestOnlyExpeditionCampSiteFixture(PressureCampId, RouteTravelId,
                    new RuleQuantity(1), concealed: true);
                var policy = PressureCampPolicy(campSite, initialPressure: 2, seed: 1);
                Simulation StartConcealedCamp()
                {
                    var simulation = PressurePrepareCampAtCheckpoint(policy);
                    PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds));
                    PressureCampCommit(simulation, CommandKind.BeginCampUse, "concealed.use.begin");
                    PressureCampCommit(simulation, CommandKind.BeginLyingLow, "concealed.low.begin");
                    FarmWork(simulation, CommandKind.PlantCrop);
                    return simulation;
                }

                var whole = StartConcealedCamp();
                var split = StartConcealedCamp();
                var startOfSecondWatch = new RuleTime(ExpeditionPressureRules.WatchSeconds);
                var endOfSecondWatch = new RuleTime(ExpeditionPressureRules.WatchSeconds * 2);
                PressureAdvanceTo(split, new RuleTime(ExpeditionPressureRules.WatchSeconds * 3 / 2));
                string path = Path.Combine(directory, "pressure-concealed-camp-mid-watch.ddsave");
                var store = new FileSaveStore();
                store.Save(path, split.Capture());
                byte[] midSave = File.ReadAllBytes(path);
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                Require(midSave.SequenceEqual(Bytes(restored))
                    && restored.Capture().ExpeditionCampActivities.Count(x => x.Active) == 2,
                    "Active camp use and lying-low did not round-trip as authoritative intervals.");

                PressureAdvanceTo(whole, endOfSecondWatch);
                PressureAdvanceTo(split, endOfSecondWatch);
                PressureAdvanceTo(restored, endOfSecondWatch);
                var wholeState = whole.Capture();
                var a = wholeState.ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 1);
                var b = split.Capture().ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 1);
                var c = restored.Capture().ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 1);
                bool SameSettlement(ExpeditionPressureCheckpointRecord x, ExpeditionPressureCheckpointRecord y)
                    => x.At == y.At && x.WatchIndex == y.WatchIndex && x.PressureBefore == y.PressureBefore
                        && x.StoredPressure == y.StoredPressure && x.EffectivePressure == y.EffectivePressure
                        && x.Context == y.Context && x.RandomBefore == y.RandomBefore && x.RandomAfter == y.RandomAfter
                        && x.WordsConsumed == y.WordsConsumed && x.Natural == y.Natural
                        && x.Outcome == y.Outcome && x.Consequence == y.Consequence
                        && x.CauseIds.SequenceEqual(y.CauseIds, StringComparer.Ordinal)
                        && x.ReductionIds.SequenceEqual(y.ReductionIds, StringComparer.Ordinal);
                Require(SameSettlement(a, b) && SameSettlement(a, c)
                    && a.PressureBefore == 1 && a.StoredPressure == 0
                    && a.Context == ExpeditionPressureCheckpointContext.Camp
                    && a.ReductionIds.Count == 1
                    && wholeState.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow
                        && x.WatchIndex == 1) == 1
                    && wholeState.ExpeditionCampActivities.Where(x => x.Kind == ExpeditionCampActivityKind.LyingLow)
                        .Single().Active
                    && wholeState.RestIntervals.Length == 0
                    && Crop(whole).Stage == CropStage.Growing
                    && wholeState.RandomState == split.Capture().RandomState
                    && wholeState.RandomState == restored.Capture().RandomState
                    && Bytes(split).SequenceEqual(Bytes(restored)),
                    "A full concealed Watch did not grant exactly one credit or deterministic whole/split/restored replay.");

                var crossingPolicy = PressureCampPolicy(campSite, initialPressure: 0, seed: 1);
                var crossing = PressurePrepareCampAtCheckpoint(crossingPolicy);
                PressureCampCommit(crossing, CommandKind.BeginCampUse, "crossing.use.begin");
                PressureCampCommit(crossing, CommandKind.BeginLyingLow, "crossing.low.begin");
                PressureAdvanceTo(crossing, endOfSecondWatch);
                var crossed = crossing.Capture();
                var crossedFirst = crossed.ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 0);
                var crossedSecond = crossed.ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 1);
                Require(crossed.ExpeditionPressureCheckpoints.Length == 2
                    && crossedFirst.Context == ExpeditionPressureCheckpointContext.Camp
                    && crossedSecond.Context == ExpeditionPressureCheckpointContext.Camp
                    && crossedFirst.ReductionIds.Count == 1
                    && crossedSecond.ReductionIds.Count == 1
                    && !crossed.ExpeditionPressureChanges.Any(x => x.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow
                        && x.WatchIndex == 0)
                    && crossed.ExpeditionPressureChanges.Count(x => x.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow
                        && x.WatchIndex == 1) == 1
                    && crossed.RuleClock == endOfSecondWatch,
                    "One command spanning two Watches did not settle each boundary once, count only the fully covered lying-low Watch, and accept the exact closing endpoint.");

                var interrupted = PressurePrepareCampAtCheckpoint(policy);
                PressureAdvanceTo(interrupted, startOfSecondWatch);
                PressureCampCommit(interrupted, CommandKind.BeginCampUse, "interrupted.use.begin");
                PressureCampCommit(interrupted, CommandKind.BeginLyingLow, "interrupted.low.begin");
                BeginEncounter(interrupted);
                var afterCombatEntry = interrupted.Capture();
                Require(afterCombatEntry.ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.LyingLow)
                        .EndReason == ExpeditionCampActivityEndReason.Combat
                    && afterCombatEntry.ExpeditionCampActivities.Single(x => x.Kind == ExpeditionCampActivityKind.Use).Active,
                    "Combat did not interrupt lying-low independently of physical camp occupancy.");
                PressureMoveHostileAdjacent(interrupted);
                DefeatConnectedEnemy(interrupted);
                WorldCommit(interrupted, Tac(interrupted, CommandKind.EndFixedEncounter));
                PressureCampCommit(interrupted, CommandKind.BeginLyingLow, "interrupted.low.restart");
                PressureAdvanceTo(interrupted, new RuleTime(ExpeditionPressureRules.WatchSeconds * 2 - 1));
                PressureCampCommit(interrupted, CommandKind.EndLyingLow, "interrupted.low.end");
                PressureAdvanceTo(interrupted, endOfSecondWatch);
                var interruptedState = interrupted.Capture();
                var interruptedCheckpoint = interruptedState.ExpeditionPressureCheckpoints.Single(x => x.WatchIndex == 1);
                Require(interruptedCheckpoint.Context == ExpeditionPressureCheckpointContext.Camp
                    && !interruptedState.ExpeditionPressureChanges.Any(x => x.Kind == ExpeditionPressureChangeKind.FullWatchLyingLow
                        && x.WatchIndex == 1)
                    && interruptedState.ExpeditionCampActivities.Where(x => x.Kind == ExpeditionCampActivityKind.LyingLow)
                        .All(x => x.EndedAt.HasValue && x.EndReason != ExpeditionCampActivityEndReason.PressureClosure),
                    "Combat-interrupted and restarted partial lying-low intervals incorrectly combined into a full-Watch credit.");
            });

            cases.Add("expedition_pressure_schema67_save_continues_with_legacy_arrival_semantics", () => {
                var routes = PressureHavenRouteFixture();
                var policy = PressurePolicy(initialPressure: 5, seed: 1, routes: routes);
                var legacyInitial = policy.Initial();
                legacyInitial.SchemaVersion = Snapshot.ExpeditionPressureSchema;
                var simulation = new Simulation(policy, legacyInitial, ExecutionProfile.Laboratory);
                WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId);
                WorldAdvance(simulation, 1);
                PortableCommit(simulation, Portable(simulation, CommandKind.RemovePortableItem, PortableKitFixture.Pack));
                PortableCommit(simulation, Portable(simulation, CommandKind.HandlePortableEquipment,
                    PortableKitFixture.Pack, handling: HandlingKind.Drop));
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "pressure.schema67.route.start"));
                WorldAdvance(simulation, 21600);
                PressurePauseActiveRouteIfMoving(simulation, "pressure.schema67.route.pause");
                string path = Path.Combine(directory, "pressure-schema67-before-haven.ddsave");
                var store = new FileSaveStore(); store.Save(path, simulation.Capture());
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                Require(restored.Capture().SchemaVersion == Snapshot.ExpeditionPressureSchema
                    && Bytes(restored).SequenceEqual(Bytes(simulation)),
                    "Schema67 pressure save did not retain its supported wire form after restore.");
                WorldStep(simulation, 1, 0); WorldAdvance(simulation, 1);
                WorldStep(restored, 1, 0); WorldAdvance(restored, 1);
                var completed = simulation.Capture();
                Require(completed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 3
                    && completed.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 3
                    && completed.ExpeditionPressureExposures.Single().EndKind == ExpeditionPressureExposureEndKind.SafeHavenArrival
                    && Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Historical schema67 continuation changed arrival ordering or deterministic state.");
            });

            cases.Add("expedition_pressure_schema67_exact_watch_haven_retains_legacy_reason_on_restore", () => {
                var routes = PressureHavenRouteFixture();
                var policy = PressurePolicy(initialPressure: 5, seed: 1, routes: routes);
                var legacyInitial = policy.Initial();
                legacyInitial.SchemaVersion = Snapshot.ExpeditionPressureSchema;
                var simulation = new Simulation(policy, legacyInitial, ExecutionProfile.Laboratory);
                WorldStep(simulation, 0, -1, actor: TestOnlyPolicy.CompanionId);
                WorldAdvance(simulation, 1);
                PortableCommit(simulation, Portable(simulation, CommandKind.RemovePortableItem, PortableKitFixture.Pack));
                PortableCommit(simulation, Portable(simulation, CommandKind.HandlePortableEquipment,
                    PortableKitFixture.Pack, handling: HandlingKind.Drop));
                RouteTravelReachSource(simulation);
                WorldCommit(simulation, RouteTravelCommand(simulation, CommandKind.StartRouteTravel,
                    "pressure.schema67.exact.route.start"));
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds - 1));
                PressurePauseActiveRouteIfMoving(simulation, "pressure.schema67.exact.route.pause");
                WorldStep(simulation, 1, 0); WorldAdvance(simulation, 1);
                var checkpoint = simulation.Capture().ExpeditionPressureCheckpoints.Single();
                Require(simulation.Capture().SchemaVersion == Snapshot.ExpeditionPressureSchema
                    && simulation.Capture().RuleClock == new RuleTime(ExpeditionPressureRules.WatchSeconds)
                    && checkpoint.Reason == ExpeditionPressureSettlementReason.HavenArrivalAtWatchEnd,
                    "Schema67 exact-Watch safe arrival changed its established checkpoint reason.");
                string path = Path.Combine(directory, "pressure-schema67-exact-haven-watch.ddsave");
                var store = new FileSaveStore(); store.Save(path, simulation.Capture());
                byte[] saved = File.ReadAllBytes(path);
                var restored = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                PressureAdvanceTo(simulation, new RuleTime(ExpeditionPressureRules.WatchSeconds * 2));
                PressureAdvanceTo(restored, new RuleTime(ExpeditionPressureRules.WatchSeconds * 2));
                Require(saved.SequenceEqual(Bytes(new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory)))
                    && checkpoint.SameAs(simulation.Capture().ExpeditionPressureCheckpoints.Single())
                    && Bytes(simulation).SequenceEqual(Bytes(restored)),
                    "Schema67 exact-Watch arrival failed continuation/restore replay or settled twice.");
            });
        }
    }
}
#endif
