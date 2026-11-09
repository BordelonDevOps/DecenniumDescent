#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Numerics;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private const string PressureCohortId = "TEST_ONLY.pressure.cohort";

        private static TestOnlySharedWorldPolicy PressurePolicy(int initialPressure = 5, uint seed = 1,
            TestOnlyExpeditionRouteFixture routes = null)
        {
            routes = routes ?? RouteTravelCheckpointFixture();
            return new TestOnlySharedWorldPolicy(new PortableKitFixture(), new SharedCombatFixture(enemyHp: 1, seed: seed),
                new SupplyCacheFixture()).EnableExpeditionRouteTravel(routes)
                .EnableExpeditionPressure(new TestOnlyExpeditionPressureFixture(PressureCohortId,
                    TestOnlyPolicy.ActorId, initialPressure, new[] { TestOnlyCropPolicy.PlotId }));
        }

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
            TestOnlyExpeditionRouteFixture routes = null)
        {
            routes = routes ?? PressureHavenRouteFixture();
            var simulation = World(PressurePolicy(initialPressure, seed, routes));
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
        }
    }
}
#endif
