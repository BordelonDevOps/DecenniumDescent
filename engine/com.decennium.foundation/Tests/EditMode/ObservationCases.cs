#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Linq;
using Decennium.Foundation.Laboratory;

namespace Decennium.Foundation.Tests
{
    public static partial class FoundationCases
    {
        private static ObservationFixture ObservationCoverFixture()
            => new ObservationFixture(8, 8,
                new[]
                {
                    new ObservationGridCell(2, 0, blocksSight: true, blocksEffect: false, blocksMovement: true),
                    new ObservationGridCell(2, 2, blocksSight: true, blocksEffect: false, blocksMovement: true)
                },
                new[]
                {
                    new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                    new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                    new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                });

        private static ObservationFixture ObservationTraversalGapFixture()
            => new ObservationFixture(8, 8,
                new[]
                {
                    new ObservationGridCell(1, 1, blocksSight: true, blocksEffect: false, blocksMovement: true),
                    new ObservationGridCell(3, 1, blocksSight: true, blocksEffect: false, blocksMovement: true)
                },
                new[]
                {
                    new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                    new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                    new ObservationSightProfile(AdditionalTacticalActor.Id, 0, 0)
                });

        private static ObservationFixture ObservationObserverIsolatedGapFixture()
            => new ObservationFixture(8, 8,
                new[]
                {
                    new ObservationGridCell(1, 1, blocksSight: true, blocksEffect: false, blocksMovement: true),
                    new ObservationGridCell(3, 1, blocksSight: true, blocksEffect: false, blocksMovement: true),
                    new ObservationGridCell(3, 0, blocksSight: true, blocksEffect: false, blocksMovement: true)
                },
                new[]
                {
                    new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                    new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                    new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                });

        private static uint ObservationTwoObserverHideSeed(Snapshot initial)
        {
            var hider = initial.Characters.Single(x => x.ActorId == TestOnlyPolicy.ActorId);
            var hiderSkill = initial.SkillTraining.SingleOrDefault(x => x.ActorId == hider.ActorId && x.SkillId == "stealth");
            int hideModifier = AbilityCheckRules.Derive(hider, hiderSkill, 1)
                .TotalWithInjury(ActorLifeRules.Read(initial.Lives.Single(x => x.ActorId == hider.ActorId)));
            int[] observerDcs = new[] { TestOnlyPolicy.CompanionId, AdditionalTacticalActor.Id }.Select(observerId =>
            {
                var character = initial.Characters.Single(x => x.ActorId == observerId);
                var skill = initial.SkillTraining.SingleOrDefault(x => x.ActorId == observerId && x.SkillId == "perception");
                return checked(10 + AbilityCheckRules.Derive(character, skill, 4).Total);
            }).ToArray();
            for (uint seed = 1; seed < 1000000; seed++)
            {
                var roll = PlaytestDice.RollD20(seed);
                if (observerDcs.All(dc => PlaytestRolls.TaskCheck(roll.Natural, hideModifier, dc).Success)) return seed;
            }
            throw new Exception("No deterministic Hide seed was found for both observers.");
        }

        private static byte[] RunObservationTraversalTrace(TestOnlySharedWorldPolicy policy, Simulation simulation)
        {
            string observer = TestOnlyPolicy.CompanionId, target = TestOnlyPolicy.ActorId;
            Require(!ObservationRules.CanSee(simulation.Capture(), observer, target),
                "The companion unexpectedly sees the hero before the authored traversal.");

            WorldStep(simulation, 1, 0);
            WorldAdvance(simulation, 1);
            WorldStep(simulation, 1, 0);
            WorldAdvance(simulation, 1, 4);
            var partial = simulation.Capture();
            var edge = partial.WorldTraversals.Single(x => x.ActorId == target);
            Require(edge.DistanceFeet == new RuleQuantity(5, 4),
                "The saved mid-traversal position did not retain its exact quarter-second progress.");
            byte[] partialBytes = Bytes(simulation);
            simulation = new Simulation(policy, new SnapshotCodec().Decode(partialBytes), ExecutionProfile.Laboratory);
            Require(partialBytes.SequenceEqual(Bytes(simulation)),
                "Restoring during exposed traversal changed the observer or exact movement state.");

            WorldAdvance(simulation, 3, 4);
            var final = simulation.Capture();
            var mover = final.Actors.Single(x => x.Id == target);
            var knowledge = final.ObserverKnowledge.SingleOrDefault(x => x.ObserverId == observer && x.TargetId == target);
            Require(final.WorldTraversals.Length == 0 && mover.X == 2 && mover.Y == 0
                && !ObservationGeometry.CanSee(final, observer, target)
                && knowledge != null && knowledge.HasLastKnownLocation && !knowledge.CurrentLocationKnown
                && knowledge.Evidence == ObservationEvidenceKind.DirectSightLimit
                && knowledge.EvidenceAt == T(2)
                && knowledge.LastKnownX == new RuleQuantity(2)
                && knowledge.LastKnownY == default,
                "A brief sighting during partial travel did not preserve the exact excluded sight-loss boundary after concealment at arrival.");
            return Bytes(simulation);
        }

        private static byte[] RunObservationPartialExposureClearTrace(byte[] hiddenBytes)
        {
            string observer = TestOnlyPolicy.CompanionId, unexposedObserver = AdditionalTacticalActor.Id;
            string target = TestOnlyPolicy.ActorId;
            var codec = new SnapshotCodec();
            var before = codec.Decode(hiddenBytes);
            Require(before.Actors.Single(x => x.Id == target).X == 1
                && ObservationRules.HiddenTo(before, observer, target)
                && ObservationRules.HiddenTo(before, unexposedObserver, target),
                "The saved pre-traversal state did not contain the two successful observer-specific Hide results.");

            var edge = new WorldTraversalRecord(target, before.Revision, 1, 0, 2, 0);
            var partialEdge = edge.With(new RuleQuantity(5, 4), WorldTraversalStatus.Moving);
            before.WorldTraversals = before.WorldTraversals.Concat(new[] { partialEdge }).ToArray();
            ObservationRules.ProcessWorldTraversalSegments(before,
                new[] { new ObservationMovementSegment(edge, default, new RuleQuantity(5, 4)) },
                before.RuleClock, before.RuleClock, before.Revision);
            var partial = before;
            var partialKnowledge = partial.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target);
            Require(partial.WorldTraversals.Single(x => x.ActorId == target).DistanceFeet == new RuleQuantity(5, 4)
                && partialKnowledge.HiddenAttemptId == ""
                && partialKnowledge.Evidence == ObservationEvidenceKind.DirectSight
                && partialKnowledge.CurrentLocationKnown
                && partialKnowledge.LastKnownX == new RuleQuantity(5, 4)
                && ObservationRules.HiddenTo(partial, unexposedObserver, target)
                && !ObservationRules.HiddenTo(partial, observer, target),
                "A partial direct-sight segment did not clear Hidden only for its seeing observer.");

            byte[] result = codec.Encode(partial);
            var restored = codec.Decode(result);
            Require(result.SequenceEqual(codec.Encode(restored))
                && ObservationRules.HiddenTo(restored, unexposedObserver, target)
                && !ObservationRules.HiddenTo(restored, observer, target),
                "Observer-specific Hidden state changed across snapshot save and restore.");
            Require(restored.RuleClock == partial.RuleClock && restored.RandomState == partial.RandomState
                && restored.Revision == partial.Revision && restored.Receipts.Select(x => x.Fingerprint)
                    .SequenceEqual(partial.Receipts.Select(x => x.Fingerprint)),
                "Partial observation changed authoritative clock, RNG, revision, or command history.");
            return result;
        }

        private static bool SameSightBoundary(ObserverKnowledgeRecord left, ObserverKnowledgeRecord right)
            => left.HasLastKnownLocation && right.HasLastKnownLocation
                && !left.CurrentLocationKnown && !right.CurrentLocationKnown
                && left.LastKnownX == right.LastKnownX && left.LastKnownY == right.LastKnownY
                && left.Evidence == ObservationEvidenceKind.DirectSightLimit
                && right.Evidence == ObservationEvidenceKind.DirectSightLimit
                && left.EvidenceAt == right.EvidenceAt && left.HiddenAttemptId == "" && right.HiddenAttemptId == "";

        private static bool SameKnowledgeContent(ObserverKnowledgeRecord left, ObserverKnowledgeRecord right)
            => left != null && right != null && left.ObserverId == right.ObserverId && left.TargetId == right.TargetId
                && left.HasLastKnownLocation == right.HasLastKnownLocation
                && left.CurrentLocationKnown == right.CurrentLocationKnown
                && left.LastKnownX == right.LastKnownX && left.LastKnownY == right.LastKnownY
                && left.Evidence == right.Evidence && left.EvidenceAt == right.EvidenceAt
                && left.HiddenAttemptId == right.HiddenAttemptId
                && left.RevealedInvisibleEpisodeId == right.RevealedInvisibleEpisodeId;

        private static bool SameKnowledgeContent(Snapshot left, Snapshot right)
        {
            var a = left.ObserverKnowledge.OrderBy(x => x.ObserverId, StringComparer.Ordinal)
                .ThenBy(x => x.TargetId, StringComparer.Ordinal).ToArray();
            var b = right.ObserverKnowledge.OrderBy(x => x.ObserverId, StringComparer.Ordinal)
                .ThenBy(x => x.TargetId, StringComparer.Ordinal).ToArray();
            return a.Length == b.Length && a.Zip(b, SameKnowledgeContent).All(x => x);
        }

        private static ObservationFixture ObservationMovingObserverLimitFixture()
            => new ObservationFixture(8, 8,
                new[] { new ObservationGridCell(3, 1, blocksSight: true, blocksEffect: false, blocksMovement: false) },
                new[]
                {
                    new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                    new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                    new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                });

        private static ObservationFixture ObservationInclusiveRangeFixture()
            => new ObservationFixture(8, 8, Array.Empty<ObservationGridCell>(),
                new[]
                {
                    new ObservationSightProfile(TestOnlyPolicy.ActorId, 5, 30),
                    new ObservationSightProfile(TestOnlyPolicy.CompanionId, 5, 30),
                    new ObservationSightProfile(AdditionalTacticalActor.Id, 5, 30)
                });

        private static ObservationFixture ObservationMultipleExposureFixture()
            => new ObservationFixture(8, 8,
                new[]
                {
                    new ObservationGridCell(1, 4, blocksSight: true, blocksEffect: false, blocksMovement: false),
                    new ObservationGridCell(4, 4, blocksSight: true, blocksEffect: false, blocksMovement: false)
                },
                new[]
                {
                    new ObservationSightProfile(TestOnlyPolicy.ActorId, 50, 30),
                    new ObservationSightProfile(TestOnlyPolicy.CompanionId, 50, 30),
                    new ObservationSightProfile(AdditionalTacticalActor.Id, 50, 30)
                });

        private static Snapshot ObservationStateAt(TestOnlySharedWorldPolicy policy, string actorId, int x, int y,
            ObservationFixture fixture)
        {
            var state = policy.Initial();
            var actor = state.Actors.Single(a => a.Id == actorId);
            actor.X = x;
            actor.Y = y;
            ObservationRules.Initialize(state, fixture);
            return state;
        }

        private static void ProcessObservationLeg(Snapshot state, string moverId, int fromX, int fromY,
            int toX, int toY, RuleQuantity fromDistance, RuleQuantity toDistance, RuleTime start, RuleTime end)
        {
            long revision = checked(state.Revision + 1);
            state.Revision = revision;
            var edge = new WorldTraversalRecord(moverId, revision, fromX, fromY, toX, toY);
            bool completes = toDistance == new RuleQuantity(5);
            if (completes)
            {
                var mover = state.Actors.Single(a => a.Id == moverId);
                mover.X = toX;
                mover.Y = toY;
                state.WorldTraversals = Array.Empty<WorldTraversalRecord>();
            }
            else state.WorldTraversals = new[] { edge.With(toDistance, WorldTraversalStatus.Moving) };
            ObservationRules.ProcessWorldTraversalSegments(state,
                new[] { new ObservationMovementSegment(edge, fromDistance, toDistance) }, start, end, revision);
            RuleTime priorClock = state.RuleClock;
            state.RuleClock = end;
            if (end > priorClock)
            {
                var stamp = new ConditionStamp(end);
                state.Conditions = state.Conditions.Select((journal, index) => ConditionHistory.Restore(journal)
                    .Append(ConditionOperation.Advance("host.clock.observation." + revision + "." + index, stamp))
                    .State.Journal).ToArray();
            }
            if (completes) ObservationRules.Refresh(state, end, revision);
        }

        private static Simulation RunObservationHideThroughExit(TestOnlySharedWorldPolicy policy, byte[] encounterBytes, int observers)
        {
            string hero = TestOnlyPolicy.ActorId;
            string companion = TestOnlyPolicy.CompanionId;
            string enemy = AdditionalTacticalActor.Id;
            var codec = new SnapshotCodec();
            var simulation = new Simulation(policy, codec.Decode(encounterBytes), ExecutionProfile.Laboratory);
            var initial = simulation.Capture();
            Require(initial.InventoryCombat && initial.Encounter.CurrentActor == hero
                && initial.Actors.Single(x => x.Id == hero).X == 1 && initial.Actors.Single(x => x.Id == hero).Y == 0
                && !ObservationRules.CanSee(initial, companion, hero)
                && !ObservationRules.CanSee(initial, enemy, hero),
                "The legal encounter entry did not retain the concealed shared-world anchor.");

            WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                stance: (int)CombatStance.Aggressive));
            WorldCommit(simulation, ObservationCommand(simulation, CommandKind.Hide, hero));
            var hidden = simulation.Capture();
            Require(hidden.ObservationHideResults.Length == observers
                && hidden.ObservationHideResults.All(x => x.HiddenEstablished)
                && ObservationRules.HiddenTo(hidden, companion, hero)
                && ObservationRules.HiddenTo(hidden, enemy, hero),
                "The legal tactical Hide did not establish the expected observer-specific Hidden results.");
            byte[] afterHide = Bytes(simulation);
            simulation = new Simulation(policy, codec.Decode(afterHide), ExecutionProfile.Laboratory);
            Require(afterHide.SequenceEqual(Bytes(simulation))
                && ObservationRules.HiddenTo(simulation.Capture(), companion, hero)
                && ObservationRules.HiddenTo(simulation.Capture(), enemy, hero),
                "Tactical Hide state changed across a saved encounter boundary.");

            WorldCommit(simulation, Tac(simulation, CommandKind.EndRegularTurn));
            int[,] enemyRoute = {
                { 4, 1 }, { 4, 2 }, { 3, 2 }, { 2, 2 }, { 2, 3 }, { 1, 3 },
                { 0, 3 }, { 0, 2 }, { 0, 1 }, { 0, 0 }
            };
            for (int i = 0; i < enemyRoute.GetLength(0); i++)
            {
                if (simulation.Capture().Encounter.CurrentActor != enemy)
                    ConnectedEnd(simulation);
                var turn = simulation.Capture();
                Require(turn.Encounter.CurrentActor == enemy, "The blinded fixture opponent did not receive its movement turn.");
                if (!turn.Stances.Any(x => x.ActorId == enemy && x.TurnOrdinal == turn.Encounter.TurnOrdinal))
                    WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                        stance: (int)CombatStance.Aggressive));
                TacStep(simulation, enemyRoute[i, 0], enemyRoute[i, 1]);
                if (i == 5 || i == enemyRoute.GetLength(0) - 1)
                    ConnectedEnd(simulation);
            }
            var adjacent = simulation.Capture();
            Require(adjacent.Encounter.CurrentActor == hero
                && adjacent.Actors.Single(x => x.Id == enemy).X == 0 && adjacent.Actors.Single(x => x.Id == enemy).Y == 0
                && WorldSpatialQueries.WithinRange(adjacent.Actors.Single(x => x.Id == hero).X,
                    adjacent.Actors.Single(x => x.Id == hero).Y, 0, 0, 1),
                "The fixture opponent did not approach the concealed hider through legal tactical steps.");
            DefeatConnectedEnemy(simulation);
            Require(simulation.Capture().Lives.Single(x => x.ActorId == enemy).Dead,
                "The tactical encounter did not resolve before exploration resumed.");
            WorldCommit(simulation, Tac(simulation, CommandKind.EndFixedEncounter));
            var exited = simulation.Capture();
            Require(!exited.InventoryCombat && exited.Actors.Single(x => x.Id == hero).X == 1
                && exited.Actors.Single(x => x.Id == hero).Y == 0
                && ObservationRules.HiddenTo(exited, companion, hero)
                && exited.ObservationActions.Any(x => x.Kind == ObservationActionKind.Hide
                    && x.Outcome == ObservationActionOutcome.HideAttempted)
                && exited.ObservationHideResults.Length == observers,
                "A legal tactical Hide did not survive resolved encounter exit for the occluded companion.");
            return simulation;
        }

        private static byte[] RunObservationTacticalHideExitTrace(TestOnlySharedWorldPolicy policy,
            ObservationFixture fixture, byte[] encounterBytes)
        {
            string hero = TestOnlyPolicy.ActorId, companion = TestOnlyPolicy.CompanionId, enemy = AdditionalTacticalActor.Id;
            var codec = new SnapshotCodec();
            var simulation = RunObservationHideThroughExit(policy, encounterBytes, 2);
            var exited = simulation.Capture();
            var otherObserverBefore = exited.ObserverKnowledge.Single(x => x.ObserverId == enemy && x.TargetId == hero);
            byte[] exitedBytes = Bytes(simulation);
            var uninterrupted = new Simulation(policy, codec.Decode(exitedBytes), ExecutionProfile.Laboratory);
            WorldStep(uninterrupted, 1, 0);
            WorldAdvance(uninterrupted, 1);
            var uninterruptedFinal = uninterrupted.Capture();
            var uninterruptedCompanion = uninterruptedFinal.ObserverKnowledge.Single(x => x.ObserverId == companion && x.TargetId == hero);
            var uninterruptedOther = uninterruptedFinal.ObserverKnowledge.Single(x => x.ObserverId == enemy && x.TargetId == hero);
            Require(uninterruptedFinal.WorldTraversals.Length == 0
                && uninterruptedFinal.Actors.Single(x => x.Id == hero).X == 2
                && uninterruptedFinal.Actors.Single(x => x.Id == hero).Y == 0
                && !uninterruptedCompanion.CurrentLocationKnown && uninterruptedCompanion.HasLastKnownLocation
                && uninterruptedCompanion.HiddenAttemptId == ""
                && uninterruptedCompanion.Evidence == ObservationEvidenceKind.DirectSightLimit
                && uninterruptedCompanion.LastKnownX == new RuleQuantity(2)
                && uninterruptedCompanion.LastKnownY == default
                && uninterruptedCompanion.EvidenceAt == uninterruptedFinal.RuleClock
                && !ObservationGeometry.CanSee(uninterruptedFinal, fixture, companion, hero)
                && uninterruptedOther.SameAs(otherObserverBefore)
                && !ObservationRules.LocationKnown(uninterruptedFinal, enemy, hero),
                "A single uninterrupted traversal did not retain the excluded sight-loss boundary as stale observer-specific evidence.");

            byte[] exactLossBoundaryBytes = Bytes(uninterrupted);
            var exactLossBoundaryRestored = new Simulation(policy, codec.Decode(exactLossBoundaryBytes), ExecutionProfile.Laboratory);
            Require(exactLossBoundaryBytes.SequenceEqual(Bytes(exactLossBoundaryRestored)),
                "Saving and restoring exactly at target sight loss changed its evidence or command replay.");
            var exactLossBoundarySplit = new Simulation(policy, codec.Decode(exitedBytes), ExecutionProfile.Laboratory);
            WorldStep(exactLossBoundarySplit, 1, 0);
            WorldAdvance(exactLossBoundarySplit, 3, 4);
            byte[] preLimitBytes = Bytes(exactLossBoundarySplit);
            exactLossBoundarySplit = new Simulation(policy, codec.Decode(preLimitBytes), ExecutionProfile.Laboratory);
            WorldAdvance(exactLossBoundarySplit, 1, 4);
            var exactLossBoundary = exactLossBoundarySplit.Capture();
            var exactLossKnowledge = exactLossBoundary.ObserverKnowledge.Single(x => x.ObserverId == companion && x.TargetId == hero);
            var exactLossOther = exactLossBoundary.ObserverKnowledge.Single(x => x.ObserverId == enemy && x.TargetId == hero);
            Require(SameSightBoundary(exactLossKnowledge, uninterruptedCompanion)
                && exactLossOther.SameAs(otherObserverBefore)
                && exactLossBoundary.RuleClock == uninterruptedFinal.RuleClock
                && SameKnowledgeContent(uninterruptedFinal, exactLossBoundary),
                "Splitting and restoring immediately before sight loss changed the complete observer-knowledge set.");
            var splitLossBytes = Bytes(exactLossBoundarySplit);
            exactLossBoundarySplit = new Simulation(policy, codec.Decode(splitLossBytes), ExecutionProfile.Laboratory);
            Require(splitLossBytes.SequenceEqual(Bytes(exactLossBoundarySplit)),
                "Restoring at the split sight-loss boundary changed the completed target traversal.");

            var boundarySplit = new Simulation(policy, codec.Decode(exitedBytes), ExecutionProfile.Laboratory);
            WorldStep(boundarySplit, 1, 0);
            WorldAdvance(boundarySplit, 1, 5);
            var atEntryBoundary = boundarySplit.Capture();
            Require(atEntryBoundary.WorldTraversals.Single(x => x.ActorId == hero).DistanceFeet == new RuleQuantity(1)
                && !ObservationGeometry.CanSee(atEntryBoundary, fixture, companion, hero)
                && ObservationRules.HiddenTo(atEntryBoundary, companion, hero),
                "The exact visibility-entry boundary was treated as visible instead of blocked.");
            byte[] entryBoundaryBytes = Bytes(boundarySplit);
            boundarySplit = new Simulation(policy, codec.Decode(entryBoundaryBytes), ExecutionProfile.Laboratory);
            WorldAdvance(boundarySplit, 4, 5);
            var boundarySplitFinal = boundarySplit.Capture();
            var boundarySplitKnowledge = boundarySplitFinal.ObserverKnowledge.Single(x => x.ObserverId == companion && x.TargetId == hero);
            var boundarySplitOther = boundarySplitFinal.ObserverKnowledge.Single(x => x.ObserverId == enemy && x.TargetId == hero);
            Require(boundarySplitFinal.WorldTraversals.Length == 0
                && SameSightBoundary(boundarySplitKnowledge, uninterruptedCompanion)
                && boundarySplitOther.SameAs(otherObserverBefore)
                && !ObservationRules.LocationKnown(boundarySplitFinal, companion, hero),
                "Splitting and restoring at the exact visibility-entry boundary changed the final sight-limit evidence.");

            WorldStep(simulation, 1, 0);
            WorldAdvance(simulation, 1, 4);
            var partial = simulation.Capture();
            var edge = partial.WorldTraversals.Single(x => x.ActorId == hero);
            var companionKnowledge = partial.ObserverKnowledge.Single(x => x.ObserverId == companion && x.TargetId == hero);
            var otherObserverPartial = partial.ObserverKnowledge.Single(x => x.ObserverId == enemy && x.TargetId == hero);
            var expectedX = new RuleQuantity(edge.FromX) + new RuleQuantity(edge.ToX - edge.FromX)
                .Scale(edge.DistanceFeet.Numerator, checked(5 * edge.DistanceFeet.Denominator));
            var expectedY = new RuleQuantity(edge.FromY) + new RuleQuantity(edge.ToY - edge.FromY)
                .Scale(edge.DistanceFeet.Numerator, checked(5 * edge.DistanceFeet.Denominator));
            Require(edge.DistanceFeet == new RuleQuantity(5, 4)
                && companionKnowledge.HiddenAttemptId == ""
                && companionKnowledge.Evidence == ObservationEvidenceKind.DirectSight
                && companionKnowledge.CurrentLocationKnown
                && companionKnowledge.LastKnownX == expectedX && companionKnowledge.LastKnownY == expectedY
                && !ObservationRules.HiddenTo(partial, companion, hero)
                && otherObserverPartial.SameAs(otherObserverBefore)
                && ObservationRules.HiddenTo(partial, enemy, hero)
                && !ObservationRules.LocationKnown(partial, enemy, hero),
                "Legal shared exploration movement did not clear only the companion's Hidden state at its fractional sighting.");
            byte[] partialBytes = Bytes(simulation);
            simulation = new Simulation(policy, codec.Decode(partialBytes), ExecutionProfile.Laboratory);
            Require(partialBytes.SequenceEqual(Bytes(simulation)),
                "The legal post-combat partial traversal changed across save and restore.");

            var visibleInterior = codec.Decode(partialBytes);
            var probeEdge = visibleInterior.WorldTraversals.Single(x => x.ActorId == hero);
            visibleInterior.WorldTraversals = new[] { probeEdge.With(new RuleQuantity(35, 8), probeEdge.Status) };
            Require(ObservationGeometry.CanSee(visibleInterior, fixture, companion, hero),
                "An exact interior point before the sight-limit boundary was incorrectly blocked.");

            WorldAdvance(simulation, 3, 4);
            var final = simulation.Capture();
            companionKnowledge = final.ObserverKnowledge.Single(x => x.ObserverId == companion && x.TargetId == hero);
            var otherObserverFinal = final.ObserverKnowledge.Single(x => x.ObserverId == enemy && x.TargetId == hero);
            Require(final.WorldTraversals.Length == 0
                && final.Actors.Single(x => x.Id == hero).X == 2 && final.Actors.Single(x => x.Id == hero).Y == 0
                && !ObservationGeometry.CanSee(final, companion, hero)
                && companionKnowledge.HasLastKnownLocation && !companionKnowledge.CurrentLocationKnown
                && companionKnowledge.Evidence == ObservationEvidenceKind.DirectSightLimit
                && companionKnowledge.LastKnownX == new RuleQuantity(2) && companionKnowledge.LastKnownY == default
                && companionKnowledge.EvidenceAt == final.RuleClock
                && SameSightBoundary(companionKnowledge, uninterruptedCompanion)
                && otherObserverFinal.SameAs(otherObserverBefore)
                && ObservationRules.HiddenTo(final, enemy, hero)
                && !ObservationRules.LocationKnown(final, enemy, hero),
                "The companion's excluded sight-loss boundary was not retained consistently after concealment.");
            return Bytes(simulation);
        }

        private static uint ObservationHideSearchSeed(Snapshot initial)
        {
            var hider = initial.Characters.Single(x => x.ActorId == TestOnlyPolicy.ActorId);
            var hiderSkill = initial.SkillTraining.SingleOrDefault(x => x.ActorId == hider.ActorId && x.SkillId == "stealth");
            int hideModifier = AbilityCheckRules.Derive(hider, hiderSkill, 1)
                .TotalWithInjury(ActorLifeRules.Read(initial.Lives.Single(x => x.ActorId == hider.ActorId)));
            var observer = initial.Characters.Single(x => x.ActorId == AdditionalTacticalActor.Id);
            var observerSkill = initial.SkillTraining.SingleOrDefault(x => x.ActorId == observer.ActorId && x.SkillId == "perception");
            int hideDc = checked(10 + AbilityCheckRules.Derive(observer, observerSkill, 4).Total);
            var searcher = initial.Characters.Single(x => x.ActorId == AdditionalTacticalActor.Id);
            var searchSkill = initial.SkillTraining.SingleOrDefault(x => x.ActorId == searcher.ActorId && x.SkillId == "perception");
            int searchModifier = AbilityCheckRules.Derive(searcher, searchSkill, 4)
                .TotalWithInjury(ActorLifeRules.Read(initial.Lives.Single(x => x.ActorId == searcher.ActorId)), perception: true);
            for (uint seed = 1; seed < 1000000; seed++)
            {
                var hide = PlaytestDice.RollD20(seed);
                var hideCheck = PlaytestRolls.TaskCheck(hide.Natural, hideModifier, hideDc);
                if (!hideCheck.Success) continue;
                var search = PlaytestDice.RollD20(hide.NextRandomState);
                if (PlaytestRolls.TaskCheck(search.Natural, searchModifier, checked((int)hideCheck.Total)).Success) return seed;
            }
            throw new Exception("No deterministic Hide/Search seed was found.");
        }

        private static Command ObservationCommand(Simulation simulation, CommandKind kind, string actor = null, int x = 0, int y = 0)
        {
            var s = simulation.Capture();
            actor = actor ?? s.Encounter.CurrentActor;
            return new Command("observation.command." + (s.Revision + 1), actor, s.Revision, kind,
                s.Encounter.CurrentTurnId, x, y);
        }

        private static byte[] RunObservationTrace(TestOnlySharedWorldPolicy policy, Simulation simulation)
        {
            var hero = TestOnlyPolicy.ActorId;
            var enemy = AdditionalTacticalActor.Id;
            var host = TestOnlySharedWorldPolicy.Host();
            var initial = simulation.Capture();
            Require(initial.SchemaVersion == Snapshot.ObservationSchema
                && !ObservationRules.LocationKnown(initial, hero, enemy)
                && !ObservationRules.LocationKnown(initial, enemy, hero)
                && !ObservationRules.CanSee(initial, hero, enemy)
                && ObservationGeometry.LineOfEffectClear(initial, hero, enemy),
                "A sight-only blocker did not preserve location secrecy independently of line of effect.");

            WorldCommit(simulation, new Command("observation.begin", hero, initial.Revision, CommandKind.BeginFixedEncounter));
            WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
            byte[] beforeSearchQuery = Bytes(simulation);
            var availableSearch = simulation.QueryCommand(host, ObservationCommand(simulation, CommandKind.Search, hero, 0, 0));
            var outOfBoundsSearch = simulation.QueryCommand(host, ObservationCommand(simulation, CommandKind.Search,
                hero, initial.ObservationMapWidth, 0));
            var outOfRangeSearch = simulation.QueryCommand(host, ObservationCommand(simulation, CommandKind.Search, hero, 7, 7));
            Require(availableSearch.Supported && availableSearch.Admissible && availableSearch.Code == "Available"
                && availableSearch.Costs.Count == 1 && availableSearch.Costs[0].Kind == "action"
                && availableSearch.Costs[0].ResourceId == "" && availableSearch.Costs[0].Amount == 1
                && outOfBoundsSearch.Supported && !outOfBoundsSearch.Admissible
                && outOfBoundsSearch.Code == "InvalidSearchRequest" && outOfBoundsSearch.Costs.Count == 0
                && outOfRangeSearch.Supported && !outOfRangeSearch.Admissible
                && outOfRangeSearch.Code == "SearchCellOutOfRange" && outOfRangeSearch.Costs.Count == 0
                && beforeSearchQuery.SequenceEqual(Bytes(simulation)),
                "The public Search query did not report Action cost and bounds/range failures without mutating state.");
            RejectUnchanged(simulation, host,
                Tac(simulation, CommandKind.AttackClub, enemy, weapon: TestOnlyClubAttackPolicy.ActorClub), "TargetLocationUnknown");
            RejectUnchanged(simulation, host, ObservationCommand(simulation, CommandKind.Search, hero, 7, 7), "SearchCellOutOfRange");

            var hide = ObservationCommand(simulation, CommandKind.Hide, hero);
            WorldCommit(simulation, hide);
            var hidden = simulation.Capture();
            var hideAction = hidden.ObservationActions.Single(x => x.Kind == ObservationActionKind.Hide);
            var enemyHide = hidden.ObservationHideResults.Single(x => x.ObserverId == enemy);
            var companionHide = hidden.ObservationHideResults.Single(x => x.ObserverId == TestOnlyPolicy.CompanionId);
            Require(hideAction.Outcome == ObservationActionOutcome.HideAttempted
                && hidden.ObservationHideResults.Length == 2 && enemyHide.HiddenEstablished && companionHide.HiddenEstablished
                && ObservationRules.HiddenTo(hidden, enemy, hero) && ObservationRules.HiddenTo(hidden, TestOnlyPolicy.CompanionId, hero)
                && !ObservationRules.LocationKnown(hidden, enemy, hero)
                && !ObservationRules.LocationKnown(hidden, TestOnlyPolicy.CompanionId, hero)
                && !ObservationRules.LocationKnown(hidden, hero, enemy),
                "Hide did not create observer-specific hidden state and preserve information boundaries.");
            byte[] afterHide = Bytes(simulation);
            Require(simulation.Execute(host, hide).Outcome == Outcome.Duplicate && afterHide.SequenceEqual(Bytes(simulation)),
                "Duplicate Hide replay consumed another Action or random draw.");
            simulation = new Simulation(policy, new SnapshotCodec().Decode(afterHide), ExecutionProfile.Laboratory);
            Require(ObservationRules.HiddenTo(simulation.Capture(), enemy, hero)
                && ObservationRules.HiddenTo(simulation.Capture(), TestOnlyPolicy.CompanionId, hero),
                "Restoring the save changed observer-specific Hide outcomes.");
            WorldCommit(simulation, Tac(simulation, CommandKind.EndRegularTurn));

            byte[] beforeDiscovery = Bytes(simulation);
            var searchOptions = simulation.DiscoverCommands(host, enemy)
                .Where(x => x.Command.Kind == CommandKind.Search).ToArray();
            var hiddenCellOption = searchOptions.SingleOrDefault(x => x.Command.X == 0 && x.Command.Y == 0);
            var emptyCellOption = searchOptions.SingleOrDefault(x => x.Command.X == 3 && x.Command.Y == 0);
            Require(hiddenCellOption != null && emptyCellOption != null
                && hiddenCellOption.Command.Target == simulation.Capture().Encounter.CurrentTurnId
                && emptyCellOption.Command.Target == simulation.Capture().Encounter.CurrentTurnId
                && hiddenCellOption.Query.Admissible && emptyCellOption.Query.Admissible
                && hiddenCellOption.Query.Code == emptyCellOption.Query.Code
                && hiddenCellOption.Query.Costs.Count == 1 && emptyCellOption.Query.Costs.Count == 1
                && hiddenCellOption.Query.Costs[0].Kind == "action" && emptyCellOption.Query.Costs[0].Kind == "action"
                && hiddenCellOption.Query.Costs[0].Amount == 1 && emptyCellOption.Query.Costs[0].Amount == 1
                && beforeDiscovery.SequenceEqual(Bytes(simulation)),
                "Search discovery exposed hidden occupancy or varied candidate availability/cost by hidden contents.");

            var search = ObservationCommand(simulation, CommandKind.Search, enemy, 0, 0);
            WorldCommit(simulation, search);
            var found = simulation.Capture();
            var searchAction = found.ObservationActions.Single(x => x.Kind == ObservationActionKind.Search);
            Require(searchAction.Outcome == ObservationActionOutcome.SearchFound && searchAction.TargetId == hero
                && !ObservationRules.HiddenTo(found, enemy, hero) && ObservationRules.LocationKnown(found, enemy, hero)
                && !ObservationRules.CanSee(found, enemy, hero)
                && ObservationRules.HiddenTo(found, TestOnlyPolicy.CompanionId, hero)
                && !ObservationRules.LocationKnown(found, hero, enemy)
                && !ObservationRules.LocationKnown(found, TestOnlyPolicy.CompanionId, hero)
                && ObservationRules.KnownLocations(found, enemy).Any(x => x.ActorId == hero)
                && !ObservationRules.KnownLocations(found, hero).Any(x => x.ActorId == enemy)
                && !ObservationRules.KnownLocations(found, TestOnlyPolicy.CompanionId).Any(x => x.ActorId == hero),
                "Search did not disclose the found location only to its searcher.");

            byte[] beforeSpentSearchCheck = Bytes(simulation);
            var spentSearch = ObservationCommand(simulation, CommandKind.Search, enemy, 0, 0);
            var spentQuery = simulation.QueryCommand(host, spentSearch);
            var spentSearchOptions = simulation.DiscoverCommands(host, enemy)
                .Where(x => x.Command.Kind == CommandKind.Search).ToArray();
            Require(spentQuery.Supported && !spentQuery.Admissible && spentQuery.Code == "ActionAlreadySpent"
                && spentQuery.Costs.Count == 0 && spentSearchOptions.Length > 0
                && spentSearchOptions.All(x => !x.Query.Admissible && x.Query.Costs.Count == 0)
                && beforeSpentSearchCheck.SequenceEqual(Bytes(simulation)),
                "A spent Action remained query-admissible, exposed a payable cost or mutated state during discovery.");
            RejectUnchanged(simulation, host, spentSearch, "ActionAlreadySpent");

            var invalid = simulation.Capture();
            invalid.ObservationActions = invalid.ObservationActions.Select(x => x.Id == searchAction.Id
                ? new ObservationActionRecord(x.Id, x.ActorId, x.TargetId, x.Kind, x.Outcome, x.At, x.Revision,
                    new RuleQuantity(invalid.ObservationMapWidth), x.Y, x.First, x.Second, x.Natural, x.Modifier,
                    x.Total, x.Selection, x.RandomBefore, x.RandomAfter, x.WordsConsumed)
                : x).ToArray();
            Throws<ArgumentException>(() => ObservationValidation.Validate(invalid));
            Throws<ArgumentException>(() => new Simulation(policy, invalid, ExecutionProfile.Laboratory));

            WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance, actor: enemy, stance: (int)CombatStance.Aggressive));
            WorldCommit(simulation, Tac(simulation, CommandKind.EndRegularTurn, actor: enemy));
            WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
            RejectUnchanged(simulation, host,
                Tac(simulation, CommandKind.AttackClub, enemy, weapon: TestOnlyClubAttackPolicy.ActorClub), "TargetLocationUnknown");

            byte[] saved = Bytes(simulation);
            var restored = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
            Require(saved.SequenceEqual(Bytes(restored)) && restored.Capture().RandomState == simulation.Capture().RandomState,
                "Observation knowledge, action audit or RNG changed across save/restore.");
            return saved;
        }

        private static void AddObservationCases(Dictionary<string, Action> cases)
        {
            cases.Add("observation_invisible_latches_location_known_before_episode", () => {
                var fixture = new ObservationFixture(8, 8, Array.Empty<ObservationGridCell>(),
                    new[]
                    {
                        new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                        new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                        new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                    });
                var conditions = new ConditionCombatFixture(CCApply("known-invisible", "Invisible", AdditionalTacticalActor.Id));
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(), conditions: conditions).EnableObservation(fixture);
                var simulation = World(policy);
                var initial = simulation.Capture();
                string observer = TestOnlyPolicy.ActorId, target = AdditionalTacticalActor.Id;
                Require(ObservationRules.CanSee(initial, observer, target)
                    && ObservationRules.LocationKnown(initial, observer, target),
                    "The observer did not know the target's location before Invisible began.");
                byte[] initialBytes = Bytes(simulation);
                WorldCommit(simulation, new Command("observation.invisible.begin", observer, initial.Revision, CommandKind.BeginFixedEncounter));
                var afterBegin = simulation.Capture();
                WorldCommit(simulation, new Command("observation.invisible.apply", target, afterBegin.Revision,
                    CommandKind.DispatchConditionEvent, "event.known-invisible"));
                var invisible = simulation.Capture();
                Require(TestOnlyClubAttackPolicy.ConditionsFor(invisible, target).View().Has(ConditionKind.Invisible)
                    && !ObservationRules.CanSee(invisible, observer, target)
                    && ObservationRules.LocationKnown(invisible, observer, target),
                    "Applying Invisible failed to hide the visible target while preserving its current known location.");
                Require(ObservationRules.InvisibleRevealed(invisible, observer, target),
                    "Entering Invisible preserved the location but did not latch the new episode for that observer.");
                byte[] saved = Bytes(simulation);
                var restored = new Simulation(policy, new SnapshotCodec().Decode(saved), ExecutionProfile.Laboratory);
                Require(saved.SequenceEqual(Bytes(restored))
                    && ObservationRules.InvisibleRevealed(restored.Capture(), observer, target),
                    "The pre-known Invisible latch did not persist across save and restore.");

                for (int i = 0; i < restored.Capture().Encounter.Order.Count
                    && restored.Capture().Encounter.CurrentActor != target; i++)
                {
                    var turn = restored.Capture();
                    if (!turn.Stances.Any(x => x.ActorId == turn.Encounter.CurrentActor
                        && x.TurnOrdinal == turn.Encounter.TurnOrdinal))
                        WorldCommit(restored, Tac(restored, CommandKind.SelectCombatStance,
                            stance: (int)CombatStance.Aggressive));
                    WorldCommit(restored, Tac(restored, CommandKind.EndRegularTurn));
                }
                Require(restored.Capture().Encounter.CurrentActor == target,
                    "The deterministic fixture did not reach the Invisible target's regular turn.");
                if (!restored.Capture().Stances.Any(x => x.ActorId == target
                    && x.TurnOrdinal == restored.Capture().Encounter.TurnOrdinal))
                    WorldCommit(restored, Tac(restored, CommandKind.SelectCombatStance, stance: (int)CombatStance.Aggressive));
                WorldCommit(restored, Tac(restored, CommandKind.TacticalStep, x: 4, y: 1));
                var moved = restored.Capture();
                var movedKnowledge = moved.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target);
                Require(!movedKnowledge.CurrentLocationKnown && movedKnowledge.LastKnownX == new RuleQuantity(4)
                    && movedKnowledge.LastKnownY == default && ObservationRules.InvisibleRevealed(moved, observer, target),
                    "Unseen movement invalidated the old position but reset the same Invisible episode's latch.");
                byte[] movedBytes = Bytes(restored);
                var movedRestore = new Simulation(policy, new SnapshotCodec().Decode(movedBytes), ExecutionProfile.Laboratory);
                Require(movedBytes.SequenceEqual(Bytes(movedRestore))
                    && !ObservationRules.LocationKnown(movedRestore.Capture(), observer, target)
                    && ObservationRules.InvisibleRevealed(movedRestore.Capture(), observer, target),
                    "The latched episode or stale last-known position changed after movement save and restore.");

                var replay = new Simulation(policy, new SnapshotCodec().Decode(initialBytes), ExecutionProfile.Laboratory);
                WorldCommit(replay, new Command("observation.invisible.begin", observer,
                    replay.Capture().Revision, CommandKind.BeginFixedEncounter));
                WorldCommit(replay, new Command("observation.invisible.apply", target,
                    replay.Capture().Revision, CommandKind.DispatchConditionEvent, "event.known-invisible"));
                Require(saved.SequenceEqual(Bytes(replay)),
                    "Replaying the shared encounter and condition commands changed the Invisible revelation latch.");
            });

            cases.Add("observation_attack_rejects_known_target_through_effect_blocker", () => {
                var fixture = new ObservationFixture(8, 8,
                    new[] { new ObservationGridCell(2, 0, blocksSight: false, blocksEffect: true,
                        blocksMovement: false, solid: false) },
                    new[]
                    {
                        new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                        new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                        new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                    });
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                var simulation = World(policy);
                var initial = simulation.Capture();
                Require(ObservationRules.LocationKnown(initial, TestOnlyPolicy.ActorId, AdditionalTacticalActor.Id)
                    && ObservationGeometry.CanSee(initial, TestOnlyPolicy.ActorId, AdditionalTacticalActor.Id)
                    && !ObservationGeometry.LineOfEffectClear(initial, TestOnlyPolicy.ActorId, AdditionalTacticalActor.Id),
                    "The effect-only barrier did not preserve sight and known location independently.");
                WorldCommit(simulation, new Command("observation.effect.begin", TestOnlyPolicy.ActorId,
                    initial.Revision, CommandKind.BeginFixedEncounter));
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                    stance: (int)CombatStance.Aggressive));
                RejectUnchanged(simulation, TestOnlySharedWorldPolicy.Host(),
                    Tac(simulation, CommandKind.AttackClub, AdditionalTacticalActor.Id,
                        weapon: TestOnlyClubAttackPolicy.ActorClub), "BlockedLineOfEffect");
                Require(simulation.Capture().MeleeAttacks.Length == 0
                    && ObservationRules.LocationKnown(simulation.Capture(), TestOnlyPolicy.ActorId, AdditionalTacticalActor.Id),
                    "A blocked attack changed combat history or observer knowledge.");
            });

            cases.Add("observation_partial_exposure_clears_hidden_only_for_the_observer_who_sees", () => {
                var fixture = ObservationObserverIsolatedGapFixture();
                var seedPolicy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                uint seed = ObservationTwoObserverHideSeed(seedPolicy.Initial());
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed)).EnableObservation(fixture);
                var simulation = World(policy);
                WorldStep(simulation, 1, 0);
                WorldAdvance(simulation, 1);
                var preTraversal = simulation.Capture();
                Require(preTraversal.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && !ObservationRules.CanSee(simulation.Capture(), TestOnlyPolicy.CompanionId, TestOnlyPolicy.ActorId)
                    && !ObservationRules.CanSee(simulation.Capture(), AdditionalTacticalActor.Id, TestOnlyPolicy.ActorId),
                    "The hider did not reach the concealed pre-traversal anchor.");
                WorldCommit(simulation, new Command("observation.partial.begin", TestOnlyPolicy.ActorId,
                    preTraversal.Revision, CommandKind.BeginFixedEncounter));
                WorldCommit(simulation, Tac(simulation, CommandKind.SelectCombatStance,
                    stance: (int)CombatStance.Aggressive));
                WorldCommit(simulation, ObservationCommand(simulation, CommandKind.Hide, TestOnlyPolicy.ActorId));
                var hidden = simulation.Capture();
                Require(hidden.ObservationHideResults.Length == 2
                    && hidden.ObservationHideResults.All(x => x.HiddenEstablished)
                    && ObservationRules.HiddenTo(hidden, TestOnlyPolicy.CompanionId, TestOnlyPolicy.ActorId)
                    && ObservationRules.HiddenTo(hidden, AdditionalTacticalActor.Id, TestOnlyPolicy.ActorId),
                    "The actual Hide command did not establish Hidden against both observers.");

                byte[] beforeTraversal = Bytes(simulation);
                byte[] firstRun = RunObservationPartialExposureClearTrace(beforeTraversal);
                byte[] replay = RunObservationPartialExposureClearTrace(beforeTraversal);
                Require(firstRun.SequenceEqual(replay),
                    "Restoring the saved two-observer Hide state changed the partial-exposure transition.");
            });

            cases.Add("observation_tactical_hide_survives_exit_then_legal_exploration_sighting_is_observer_specific", () => {
                var fixture = ObservationObserverIsolatedGapFixture();
                var seedPolicy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                uint seed = ObservationTwoObserverHideSeed(seedPolicy.Initial());
                var conditions = new ConditionCombatFixture(CCApply("observation-exit-blind", "Blinded",
                    AdditionalTacticalActor.Id));
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(1, seed), conditions: conditions)
                    .EnableObservation(fixture);
                var simulation = World(policy);
                CCDispatch(simulation, "observation-exit-blind", AdditionalTacticalActor.Id);
                WorldStep(simulation, 1, 0);
                WorldAdvance(simulation, 1);
                var beforeEncounter = simulation.Capture();
                Require(beforeEncounter.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).X == 1
                    && beforeEncounter.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId).Y == 0
                    && !ObservationRules.CanSee(beforeEncounter, TestOnlyPolicy.CompanionId, TestOnlyPolicy.ActorId)
                    && !ObservationRules.CanSee(beforeEncounter, AdditionalTacticalActor.Id, TestOnlyPolicy.ActorId),
                    "The legal world approach did not reach its authored concealed encounter anchor.");
                WorldCommit(simulation, new Command("observation.hide-exit.begin", TestOnlyPolicy.ActorId,
                    beforeEncounter.Revision, CommandKind.BeginFixedEncounter));
                byte[] encounterBytes = Bytes(simulation);

                byte[] firstRun = RunObservationTacticalHideExitTrace(policy, fixture, encounterBytes);
                byte[] replay = RunObservationTacticalHideExitTrace(policy, fixture, encounterBytes);
                Require(firstRun.SequenceEqual(replay),
                    "The legal tactical Hide, combat exit and post-combat exploration sighting did not replay byte-for-byte.");
            });

            cases.Add("observation_shared_world_traversal_records_partial_sighting_before_concealed_endpoint", () => {
                var fixture = ObservationTraversalGapFixture();
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                var simulation = World(policy);
                byte[] initial = Bytes(simulation);
                byte[] firstRun = RunObservationTraversalTrace(policy, simulation);
                var replay = new Simulation(policy, new SnapshotCodec().Decode(initial), ExecutionProfile.Laboratory);
                byte[] replayed = RunObservationTraversalTrace(policy, replay);
                Require(firstRun.SequenceEqual(replayed),
                    "Replaying fractional world movement and observation after restore changed the final bytes.");
            });
            cases.Add("observation_legacy_schema51_sampled_profile_replays_pushed_save", () => {
                var fixture = ObservationTraversalGapFixture();
                var legacy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture,
                    ObservationAlgorithmVersion.LegacySampledV1);
                var current = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                byte[] bytes = ObservationLegacySaveFixture.Decode();
                var decoded = new SnapshotCodec().Decode(bytes);
                Require(decoded.SchemaVersion == Snapshot.ObservationSchema
                    && decoded.ContentFingerprint == legacy.ContentFingerprint
                    && decoded.ContentFingerprint.StartsWith("TEST_ONLY.observation-v1-", StringComparison.Ordinal)
                    && decoded.ContentFingerprint != current.ContentFingerprint
                    && decoded.ObserverKnowledge.Single(x => x.ObserverId == TestOnlyPolicy.CompanionId
                        && x.TargetId == TestOnlyPolicy.ActorId).Evidence == ObservationEvidenceKind.DirectSight,
                    "The authentic pushed schema51 save did not bind its original sampled observation profile.");
                var restored = new Simulation(legacy, decoded, ExecutionProfile.Laboratory);
                Require(bytes.SequenceEqual(Bytes(restored)),
                    "The authentic pushed schema51 save changed bytes while replaying under its explicit legacy profile.");
                Throws<ArgumentException>(() => new Simulation(current, decoded, ExecutionProfile.Laboratory));
            });
            cases.Add("observation_exact_intervals_cover_moving_observer_and_blocked_continuation", () => {
                var fixture = ObservationMovingObserverLimitFixture();
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                var whole = ObservationStateAt(policy, TestOnlyPolicy.CompanionId, 3, 2, fixture);
                string observer = TestOnlyPolicy.ActorId, target = TestOnlyPolicy.CompanionId;
                Require(ObservationGeometry.CanSee(whole, observer, target),
                    "The moving-observer fixture did not begin with direct sight of its stationary target.");

                ProcessObservationLeg(whole, observer, 0, 0, 1, 0, default, new RuleQuantity(5), T(0), T(0));
                var boundary = whole;
                var boundaryKnowledge = boundary.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target);
                Require(!ObservationGeometry.CanSee(boundary, observer, target)
                    && boundaryKnowledge.HasLastKnownLocation && boundaryKnowledge.CurrentLocationKnown
                    && boundaryKnowledge.LastKnownX == new RuleQuantity(3) && boundaryKnowledge.LastKnownY == new RuleQuantity(2)
                    && boundaryKnowledge.Evidence == ObservationEvidenceKind.DirectSightLimit
                    && boundaryKnowledge.EvidenceAt == T(0)
                    && ObservationRules.LocationKnown(boundary, observer, target),
                    "Moving the observer out of sight incorrectly made the stationary target's location stale.");
                byte[] boundaryBytes = new SnapshotCodec().Encode(boundary);
                var restoredAtBoundary = new SnapshotCodec().Decode(boundaryBytes);
                Require(boundaryBytes.SequenceEqual(new SnapshotCodec().Encode(restoredAtBoundary)),
                    "The exact observer-motion sight limit changed across schema51 save and restore.");
                ProcessObservationLeg(restoredAtBoundary, observer, 1, 0, 2, 0,
                    default, new RuleQuantity(5), T(0), T(0));
                var blockedContinuation = restoredAtBoundary;
                Require(!ObservationGeometry.CanSee(blockedContinuation, observer, target)
                    && SameKnowledgeContent(boundaryKnowledge,
                        blockedContinuation.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target)),
                    "A wholly blocked observer continuation overwrote the prior exact sight-loss evidence.");

                var split = ObservationStateAt(policy, TestOnlyPolicy.CompanionId, 3, 2, fixture);
                ProcessObservationLeg(split, observer, 0, 0, 1, 0, default, new RuleQuantity(15, 4), T(0), T(0));
                byte[] partialBytes = new SnapshotCodec().Encode(split);
                split = new SnapshotCodec().Decode(partialBytes);
                ProcessObservationLeg(split, observer, 0, 0, 1, 0,
                    new RuleQuantity(15, 4), new RuleQuantity(5), T(0), T(0));
                var splitBoundary = split;
                Require(SameKnowledgeContent(boundary, splitBoundary)
                    && boundary.RuleClock == splitBoundary.RuleClock
                    && boundary.Actors.Single(x => x.Id == observer).X == splitBoundary.Actors.Single(x => x.Id == observer).X,
                    "Splitting and restoring immediately before observer sight loss changed the complete knowledge set.");
                ProcessObservationLeg(split, observer, 1, 0, 2, 0, default, new RuleQuantity(5), T(0), T(0));
                Require(SameKnowledgeContent(blockedContinuation, split)
                    && split.ObserverKnowledge.Length == blockedContinuation.ObserverKnowledge.Length,
                    "Observer movement partitioning changed another observer's knowledge or later blocked evidence.");
            });
            cases.Add("observation_positive_time_moving_observer_loss_survives_boundary_save_and_blocked_remainder", () => {
                var fixture = ObservationMovingObserverLimitFixture();
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                string observer = TestOnlyPolicy.ActorId, target = TestOnlyPolicy.CompanionId;

                Snapshot PlaceFixture()
                {
                    var state = ObservationStateAt(policy, observer, 1, 0, fixture);
                    var stationaryTarget = state.Actors.Single(x => x.Id == target);
                    stationaryTarget.X = 4;
                    stationaryTarget.Y = 4;
                    var third = state.Actors.Single(x => x.Id == AdditionalTacticalActor.Id);
                    third.X = 7;
                    third.Y = 7;
                    ObservationRules.Initialize(state, fixture);
                    return state;
                }

                var whole = PlaceFixture();
                Require(ObservationGeometry.CanSee(whole, observer, target),
                    "The positive-time moving-observer fixture did not begin with sight.");
                ProcessObservationLeg(whole, observer, 1, 0, 2, 0,
                    default, new RuleQuantity(5), T(0), T(1));
                var wholeFinal = whole;
                var wholeKnowledge = wholeFinal.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target);
                Require(wholeFinal.RuleClock == T(1) && !ObservationGeometry.CanSee(wholeFinal, observer, target)
                    && wholeKnowledge.Evidence == ObservationEvidenceKind.DirectSightLimit
                    && wholeKnowledge.EvidenceAt == T(3, 5) && wholeKnowledge.EvidenceAt < wholeFinal.RuleClock
                    && wholeKnowledge.CurrentLocationKnown && wholeKnowledge.LastKnownX == new RuleQuantity(4)
                    && wholeKnowledge.LastKnownY == new RuleQuantity(4),
                    "Interior positive-time observer sight loss did not retain its exact pre-deadline limit.");

                var split = PlaceFixture();
                ProcessObservationLeg(split, observer, 1, 0, 2, 0,
                    default, new RuleQuantity(3), T(0), T(3, 5));
                var atLimit = split.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target);
                Require(split.RuleClock == T(3, 5)
                    && split.WorldTraversals.Single(x => x.ActorId == observer).DistanceFeet == new RuleQuantity(3)
                    && atLimit.Evidence == ObservationEvidenceKind.DirectSightLimit
                    && atLimit.EvidenceAt == T(3, 5) && atLimit.CurrentLocationKnown,
                    "Splitting at the interior sight-loss boundary did not persist the exact limit at positive time.");
                var codec = new SnapshotCodec();
                byte[] boundaryBytes = codec.Encode(split);
                split = codec.Decode(boundaryBytes);
                Require(boundaryBytes.SequenceEqual(codec.Encode(split)),
                    "The positive-time sight-loss boundary changed across save and restore.");
                ProcessObservationLeg(split, observer, 1, 0, 2, 0,
                    new RuleQuantity(3), new RuleQuantity(5), T(3, 5), T(1));

                Require(split.WorldTraversals.Length == 0 && split.RuleClock == wholeFinal.RuleClock
                    && split.Actors.Single(x => x.Id == observer).X == wholeFinal.Actors.Single(x => x.Id == observer).X
                    && SameKnowledgeContent(wholeFinal, split)
                    && split.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target).EvidenceAt < split.RuleClock,
                    "The blocked post-boundary remainder changed the complete semantic knowledge set or its earlier sight time.");
            });
            cases.Add("observation_inclusive_range_boundary_records_sight_then_stales_after_departure", () => {
                var fixture = ObservationInclusiveRangeFixture();
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                string target = TestOnlyPolicy.ActorId, observer = TestOnlyPolicy.CompanionId;
                var state = ObservationStateAt(policy, target, 0, 0, fixture);
                var observerActor = state.Actors.Single(x => x.Id == observer);
                observerActor.X = 2;
                observerActor.Y = 0;
                var third = state.Actors.Single(x => x.Id == AdditionalTacticalActor.Id);
                third.X = 6;
                third.Y = 6;
                ObservationRules.Initialize(state, fixture);
                Require(!ObservationGeometry.CanSee(state, observer, target),
                    "The range-boundary fixture unexpectedly starts inside the authored sight range.");

                ProcessObservationLeg(state, target, 0, 0, 1, 0,
                    default, new RuleQuantity(5), T(0), T(1));
                var atRange = state;
                var atRangeKnowledge = atRange.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target);
                Require(ObservationGeometry.CanSee(atRange, observer, target)
                    && atRangeKnowledge.CurrentLocationKnown
                    && atRangeKnowledge.Evidence == ObservationEvidenceKind.DirectSight
                    && atRangeKnowledge.LastKnownX == new RuleQuantity(1)
                    && atRangeKnowledge.LastKnownY == default
                    && atRangeKnowledge.EvidenceAt == T(1),
                    "The inclusive authored range endpoint was not recorded as ordinary direct sight.");

                var codec = new SnapshotCodec();
                byte[] rangeBytes = codec.Encode(atRange);
                var restored = codec.Decode(rangeBytes);
                Require(rangeBytes.SequenceEqual(codec.Encode(restored)),
                    "The exact inclusive range endpoint changed across save and restore.");
                var replay = codec.Decode(rangeBytes);
                ProcessObservationLeg(restored, target, 1, 0, 0, 0,
                    default, new RuleQuantity(5), T(1), T(2));
                ProcessObservationLeg(replay, target, 1, 0, 0, 0,
                    default, new RuleQuantity(5), T(1), T(2));
                var final = restored;
                var finalKnowledge = final.ObserverKnowledge.Single(x => x.ObserverId == observer && x.TargetId == target);
                Require(!ObservationGeometry.CanSee(final, observer, target)
                    && final.Actors.Single(x => x.Id == target).X == 0 && final.RuleClock == T(2)
                    && finalKnowledge.HasLastKnownLocation && !finalKnowledge.CurrentLocationKnown
                    && finalKnowledge.Evidence == ObservationEvidenceKind.DirectSight
                    && finalKnowledge.LastKnownX == new RuleQuantity(1) && finalKnowledge.LastKnownY == default
                    && finalKnowledge.EvidenceAt == T(1) && finalKnowledge.EvidenceAt < final.RuleClock
                    && !ObservationRules.LocationKnown(final, observer, target)
                    && codec.Encode(final).SequenceEqual(codec.Encode(replay)),
                    "Departing from the visible range boundary did not leave a deterministic stale ordinary sight record.");
            });
            cases.Add("observation_exact_path_retains_latest_of_multiple_exposure_intervals", () => {
                var fixture = ObservationMultipleExposureFixture();
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                var state = ObservationStateAt(policy, TestOnlyPolicy.CompanionId, 0, 5, fixture);
                string observer = TestOnlyPolicy.ActorId, target = TestOnlyPolicy.CompanionId;
                bool[] visibleAtDestination = { false, false, true, false, false, false, true };
                for (int x = 0; x < visibleAtDestination.Length; x++)
                {
                    ProcessObservationLeg(state, target, x, 5, x + 1, 5,
                        default, new RuleQuantity(5), T(0), T(0));
                    var current = state;
                    bool visible = ObservationGeometry.CanSee(current, observer, target);
                    var knowledge = current.ObserverKnowledge.Single(k => k.ObserverId == observer && k.TargetId == target);
                    Require(visible == visibleAtDestination[x],
                        "The authored multi-edge route did not alternate between direct sight and two opaque sight intervals.");
                    if (x == 0 || x == 3)
                        Require(!knowledge.CurrentLocationKnown && knowledge.Evidence == ObservationEvidenceKind.DirectSightLimit,
                            "A sight-loss interval did not retain its exact stale target boundary.");
                    if (x == 2 || x == 6)
                        Require(knowledge.CurrentLocationKnown && knowledge.Evidence == ObservationEvidenceKind.DirectSight
                            && knowledge.LastKnownX == new RuleQuantity(x + 1) && knowledge.LastKnownY == new RuleQuantity(5)
                            && knowledge.EvidenceAt == T(0),
                            "A later exposure interval failed to replace older blocked sight evidence.");
                }
            });

            cases.Add("observation_map_rejects_unsupported_anchor_placement", () => {
                var fixture = ObservationCoverFixture();
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(fixture);
                byte[] validBytes = new SnapshotCodec().Encode(policy.Initial());
                var invalidActor = new SnapshotCodec().Decode(validBytes);
                var hero = invalidActor.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                hero.X = 2; hero.Y = 0;
                Require(policy.ValidateState(invalidActor) == "ObservationMapPlacementOrProfileMismatch",
                    "A hero inside the authored opaque blocker was not rejected by fixture validation.");
                Throws<ArgumentException>(() => new Simulation(policy, invalidActor, ExecutionProfile.Laboratory));

                var invalidObject = new SnapshotCodec().Decode(validBytes);
                var worldObject = invalidObject.Objects.Single();
                worldObject.X = 2; worldObject.Y = 0;
                Require(policy.ValidateState(invalidObject) == "ObservationMapPlacementOrProfileMismatch",
                    "An object inside the authored opaque blocker was not rejected by fixture validation.");
                Throws<ArgumentException>(() => new Simulation(policy, invalidObject, ExecutionProfile.Laboratory));

                var baseState = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).Initial();
                var baseHero = baseState.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                var effectOnly = new ObservationFixture(8, 8,
                    new[] { new ObservationGridCell(2, 0, blocksSight: false, blocksEffect: true,
                        blocksMovement: false, solid: false) },
                    new[]
                    {
                        new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                        new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                        new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                    });
                var effectPolicy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(effectOnly);
                var validEffectState = effectPolicy.Initial();
                Require(ObservationGeometry.CanSee(validEffectState, effectOnly, TestOnlyPolicy.ActorId, AdditionalTacticalActor.Id)
                    && !ObservationGeometry.LineOfEffectClear(validEffectState, effectOnly, TestOnlyPolicy.ActorId, AdditionalTacticalActor.Id)
                    && ObservationGeometry.CanSee(validEffectState, effectOnly, AdditionalTacticalActor.Id, TestOnlyPolicy.ActorId)
                    && !ObservationGeometry.LineOfEffectClear(validEffectState, effectOnly, AdditionalTacticalActor.Id, TestOnlyPolicy.ActorId),
                    "An effect-only barrier did not preserve sight while blocking line of effect symmetrically.");
                var effectBytes = new SnapshotCodec().Encode(validEffectState);
                var invalidEffectAnchor = new SnapshotCodec().Decode(effectBytes);
                var effectHero = invalidEffectAnchor.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                effectHero.X = 2; effectHero.Y = 0;
                Require(effectPolicy.ValidateState(invalidEffectAnchor) == "ObservationMapPlacementOrProfileMismatch",
                    "An actor inside a non-solid effect blocker was treated as a supported endpoint.");
                Throws<ArgumentException>(() => new Simulation(effectPolicy, invalidEffectAnchor, ExecutionProfile.Laboratory));

                var sightOnly = new ObservationFixture(8, 8,
                    new[] { new ObservationGridCell(2, 0, blocksSight: true, blocksEffect: false,
                        blocksMovement: false, solid: false) },
                    new[]
                    {
                        new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                        new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                        new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                    });
                var sightPolicy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(sightOnly);
                var sightBytes = new SnapshotCodec().Encode(sightPolicy.Initial());
                var invalidSightAnchor = new SnapshotCodec().Decode(sightBytes);
                var sightHero = invalidSightAnchor.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                sightHero.X = 2; sightHero.Y = 0;
                Require(sightPolicy.ValidateState(invalidSightAnchor) == "ObservationMapPlacementOrProfileMismatch",
                    "An actor inside a non-solid sight blocker was treated as a supported endpoint.");
                Throws<ArgumentException>(() => new Simulation(sightPolicy, invalidSightAnchor, ExecutionProfile.Laboratory));

                var traversalFixture = new ObservationFixture(8, 8,
                    new[] { new ObservationGridCell(baseHero.X + 1, baseHero.Y, blocksSight: false, blocksEffect: false,
                        blocksMovement: true, solid: false) },
                    new[]
                    {
                        new ObservationSightProfile(TestOnlyPolicy.ActorId, 30, 30),
                        new ObservationSightProfile(TestOnlyPolicy.CompanionId, 30, 30),
                        new ObservationSightProfile(AdditionalTacticalActor.Id, 30, 30)
                    });
                var traversalPolicy = new TestOnlySharedWorldPolicy(new SharedCombatFixture()).EnableObservation(traversalFixture);
                var traversalBytes = new SnapshotCodec().Encode(traversalPolicy.Initial());
                var invalidTraversal = new SnapshotCodec().Decode(traversalBytes);
                invalidTraversal.WorldTraversals = new[] { new WorldTraversalRecord(TestOnlyPolicy.ActorId, 1,
                    baseHero.X, baseHero.Y, baseHero.X + 1, baseHero.Y) };
                Throws<ArgumentException>(() => ObservationValidation.Validate(invalidTraversal));

                var cornerState = policy.Initial();
                var cornerHero = cornerState.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                var cornerEnemy = cornerState.Actors.Single(x => x.Id == AdditionalTacticalActor.Id);
                cornerHero.X = 1; cornerHero.Y = 0; cornerEnemy.X = 2; cornerEnemy.Y = 1;
                Require(!ObservationGeometry.CanSee(cornerState, fixture, cornerHero.Id, cornerEnemy.Id)
                    && ObservationGeometry.LineOfEffectClear(cornerState, fixture, cornerHero.Id, cornerEnemy.Id)
                    && !ObservationGeometry.CanSee(cornerState, fixture, cornerEnemy.Id, cornerHero.Id)
                    && ObservationGeometry.LineOfEffectClear(cornerState, fixture, cornerEnemy.Id, cornerHero.Id),
                    "Closed-cell supercover did not block symmetrically at a corner-touch boundary.");
            });
            cases.Add("observation_shared_hide_search_save_replay_and_observer_isolation", () => {
                var fixture = ObservationCoverFixture();
                var seedProbe = new TestOnlySharedWorldPolicy(new SharedCombatFixture(), conditions: null).EnableObservation(fixture);
                var seed = ObservationHideSearchSeed(seedProbe.Initial());
                var policy = new TestOnlySharedWorldPolicy(new SharedCombatFixture(seed: seed)).EnableObservation(fixture);
                var simulation = World(policy);
                byte[] initial = Bytes(simulation);
                byte[] firstRun = RunObservationTrace(policy, simulation);
                var replay = new Simulation(policy, new SnapshotCodec().Decode(initial), ExecutionProfile.Laboratory);
                byte[] replayed = RunObservationTrace(policy, replay);
                Require(firstRun.SequenceEqual(replayed), "Replaying the complete observation command trace changed the final bytes.");
            });
        }
    }
}
#endif
