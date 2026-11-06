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
                && knowledge.Evidence == ObservationEvidenceKind.DirectSight
                && knowledge.EvidenceAt > T(1) && knowledge.EvidenceAt < T(2)
                && knowledge.LastKnownX > new RuleQuantity(1) && knowledge.LastKnownX < new RuleQuantity(2)
                && knowledge.LastKnownX.Denominator > 1 && knowledge.LastKnownY == default,
                "A brief sighting during partial travel did not preserve the exact stale intermediate location after concealment at arrival.");
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
