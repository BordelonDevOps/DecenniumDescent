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
        private static SharedWorldConfiguration ArchitectureConfiguration(string id, string siteId, int siteX, int siteY,
            string lotId, params SharedActorInstanceDefinition[] actors)
            => new SharedWorldConfiguration(id,
                new[] { new SharedActorDefinition("profile.numeric-warrior3", "TEST_ONLY.numeric-warrior3", 30) }, actors,
                new[] { new SharedSiteDefinition("profile.fish-harvest", SharedSiteDefinition.FishHarvestProfile) },
                new SharedSiteInstanceDefinition(siteId, "profile.fish-harvest", siteX, siteY), lotId);

        private static Command ArchitectureStep(Simulation s, string actor, int dx, int dy, string id = null)
        {
            var state = s.Capture();
            return new Command(id ?? "architecture.step." + state.Revision, actor, state.Revision, CommandKind.BeginWorldStep, "walk", dx, dy);
        }

        private static Command ArchitectureAdvance(Simulation s, int seconds, int denominator = 1)
        {
            var state = s.Capture();
            return new Command("architecture.advance." + state.Revision, TestOnlyPolicy.ActorId, state.Revision,
                CommandKind.AdvanceClock, x: seconds, y: denominator);
        }

        private static Command ArchitectureHarvestStart(Simulation s, string worker)
        {
            var state = s.Capture();
            return new Command("architecture.harvest." + state.Revision, worker, state.Revision,
                CommandKind.StartHarvest, SharedHarvestFixture.CategoryRecordId);
        }

        private static RuleTime ArchitectureDifference(RuleTime end, RuleTime start)
            => RuleTime.FromFraction((BigInteger)end.Numerator * start.Denominator - (BigInteger)start.Numerator * end.Denominator,
                (BigInteger)end.Denominator * start.Denominator);

        private static void ArchitectureCommit(Simulation s, Authority authority, Command command)
        {
            var result = s.Execute(authority, command);
            Require(result.Outcome == Outcome.Committed, command.Kind + " rejected: " + result.Code);
        }

        private static void ArchitectureRejectUnchanged(Simulation s, Authority authority, Command command, string code)
        {
            byte[] before = Bytes(s);
            var result = s.Execute(authority, command);
            Require(result.Outcome == Outcome.Rejected && result.Code == code,
                "Expected " + code + ", got " + result.Outcome + "/" + result.Code + ".");
            Require(before.SequenceEqual(Bytes(s)), "Rejected scenario command changed state, clock, RNG, receipts, or claims.");
        }

        private static void ArchitectureMove(Simulation s, TestOnlySharedWorldPolicy policy, Authority authority,
            string actor, int dx, int dy, bool compareControllers = false)
        {
            var option = s.DiscoverCommands(authority, actor).SingleOrDefault(x => x.Command.Kind == CommandKind.BeginWorldStep
                && x.Command.Target == "walk" && x.Command.X == dx && x.Command.Y == dy && x.Query.Admissible);
            Require(option != null, "Shared discovery did not offer the admitted data-defined actor step.");
            if (compareControllers)
            {
                var parallel = new Simulation(policy, s.Capture(), ExecutionProfile.Laboratory);
                ArchitectureCommit(s, authority, option.Command);
                ArchitectureCommit(parallel, policy.HostAuthority(), new Command(option.Command.Id, option.Command.Actor,
                    option.Command.ExpectedRevision, option.Command.Kind, option.Command.Target, option.Command.X, option.Command.Y));
                Require(Bytes(s).SequenceEqual(Bytes(parallel)), "Equivalent authorized controller commands produced different snapshots.");
            }
            else ArchitectureCommit(s, authority, option.Command);
            ArchitectureCommit(s, authority, ArchitectureAdvance(s, 1));
        }

        private static void ArchitectureAdvanceTo(Simulation s, Authority authority, long seconds)
        {
            var now = s.Capture().RuleClock;
            Require(now.Denominator == 1 && seconds > now.Numerator, "Architecture test expected an integral future time.");
            ArchitectureCommit(s, authority, ArchitectureAdvance(s, checked((int)(seconds - now.Numerator))));
        }

        private static void RunWorldArchitectureScenario(SharedWorldConfiguration configuration, string worker,
            string[] route, string contender, string directory)
        {
            var events = new ConditionCombatFixture(CCApply("architecture-stun", "Stunned", worker,
                new ConditionStamp(T(220)), new ConditionStamp(T(200))));
            var policy = new TestOnlySharedWorldPolicy(configuration, new SharedCombatFixture(1, seed: 1),
                new SharedHarvestFixture(), conditions: events);
            var authority = policy.HostAuthority();
            var s = ConnectedArena(policy);
            DefeatConnectedEnemy(s);
            WorldCommit(s, Tac(s, CommandKind.EndFixedEncounter));

            var initial = s.Capture();
            Require(initial.SchemaVersion == Snapshot.HarvestSchema && initial.WorldSchedule.Order.Contains(TestOnlyPolicy.ActorId)
                && !initial.WorldSchedule.Order.Contains(worker) && initial.Actors.Any(x => x.Id == worker)
                && initial.Conditions.Length == initial.Actors.Length
                && initial.WorldActivityIntervals.Any(x => x.ActorId == worker)
                && initial.FishingCreatures.Single().SiteId == configuration.WorkSite.Id
                && initial.HarvestManifests.Single().SiteId == configuration.WorkSite.Id
                && initial.HarvestUnits.Single().Id == configuration.FiniteLotId,
                "Scenario definitions did not produce an off-calendar physical actor, site, and independent finite lot.");

            var blocked = ArchitectureStep(s, worker, 1, 0, "architecture.blocked");
            var blockedQuery = s.QueryCommand(authority, blocked);
            Require(blockedQuery.Supported && !blockedQuery.Admissible && blockedQuery.Code == "Blocked",
                "Shared spatial query admitted the authored blocked cell.");

            var premature = ArchitectureHarvestStart(s, worker);
            byte[] beforeQueries = Bytes(s);
            var prematureQuery = s.QueryCommand(authority, premature);
            var discoveredBeforeTravel = s.DiscoverCommands(authority, worker);
            var repeated = s.QueryCommand(authority, premature);
            s.DiscoverCommands(authority, worker);
            var discoveredPremature = discoveredBeforeTravel.SingleOrDefault(x => x.Command.Kind == CommandKind.StartHarvest
                && x.Command.Target == SharedHarvestFixture.CategoryRecordId);
            Require(prematureQuery.Supported && !prematureQuery.Admissible && prematureQuery.Code == "HarvestWorksiteOutOfReach"
                && discoveredPremature != null && discoveredPremature.Query.Supported && !discoveredPremature.Query.Admissible
                && discoveredPremature.Query.Code == prematureQuery.Code && repeated.Code == prematureQuery.Code
                && beforeQueries.SequenceEqual(Bytes(s)),
                "Repeated discovery or an unreachable-site preview mutated authoritative state or bypassed access.");

            // Exercise the fixed tactical roster while the configured expedition actors remain outside initiative.
            Require(!s.Capture().WorldSchedule.Order.Contains(worker), "Configured worker joined the tactical roster.");

            // Persist an exact partial edge, then continue the same data-defined route after load.
            var first = route[0].Split(',').Select(int.Parse).ToArray();
            var firstOption = s.DiscoverCommands(authority, worker).Single(x => x.Command.Kind == CommandKind.BeginWorldStep
                && x.Command.Target == "walk" && x.Command.X == first[0] && x.Command.Y == first[1] && x.Query.Admissible);
            var parallel = new Simulation(policy, s.Capture(), ExecutionProfile.Laboratory);
            ArchitectureCommit(s, authority, firstOption.Command);
            ArchitectureCommit(parallel, policy.HostAuthority(), new Command(firstOption.Command.Id, firstOption.Command.Actor,
                firstOption.Command.ExpectedRevision, firstOption.Command.Kind, firstOption.Command.Target, firstOption.Command.X, firstOption.Command.Y));
            Require(Bytes(s).SequenceEqual(Bytes(parallel)), "Discovered and directly submitted commands diverged.");
            ArchitectureCommit(s, authority, ArchitectureAdvance(s, 1, 2));
            string partialPath = Path.Combine(directory, configuration.Id + ".partial.ddsave");
            var store = new FileSaveStore(); store.Save(partialPath, s.Capture());
            s = new Simulation(policy, store.Load(partialPath), ExecutionProfile.Laboratory);
            Require(s.Capture().WorldTraversals.Single().ActorId == worker
                && s.Capture().WorldTraversals.Single().DistanceFeet == new RuleQuantity(5, 2),
                "Partial scenario traversal did not survive disk restore.");
            ArchitectureCommit(s, authority, ArchitectureAdvance(s, 1, 2));
            foreach (var text in route.Skip(1))
            {
                var delta = text.Split(',').Select(int.Parse).ToArray();
                ArchitectureMove(s, policy, authority, worker, delta[0], delta[1]);
            }

            var arrived = s.Capture();
            var body = arrived.Actors.Single(x => x.Id == worker);
            Require(WorldSpatialQueries.WithinCardinalRange(body.X, body.Y, configuration.WorkSite.X, configuration.WorkSite.Y, 1),
                "Existing traversal commands did not bring the worker within physical worksite reach.");

            var startOption = s.DiscoverCommands(authority, worker).SingleOrDefault(x => x.Command.Kind == CommandKind.StartHarvest
                && x.Command.Target == SharedHarvestFixture.CategoryRecordId && x.Query.Admissible);
            Require(startOption != null, "A reachable data-defined worksite did not discover the existing harvest command.");
            var start = startOption.Command;
            byte[] beforePreview = Bytes(s);
            var preview = s.QueryCommand(authority, start);
            Require(preview.Supported && preview.Admissible && preview.Costs.Any(x => x.Kind == "work-seconds" && x.Amount == 600)
                && beforePreview.SequenceEqual(Bytes(s)), "Harvest preview failed to expose the existing procedure cost without reserving or mutating state.");

            // Change access-related world state after the preview. The old command must be stale and free.
            if (contender != null)
                ArchitectureMove(s, policy, authority, contender, 0, 1);
            else
                ArchitectureMove(s, policy, authority, TestOnlyPolicy.ActorId, 0, 1);
            ArchitectureRejectUnchanged(s, authority, start, "StaleRevision");
            start = s.DiscoverCommands(authority, worker).Single(x => x.Command.Kind == CommandKind.StartHarvest
                && x.Command.Target == SharedHarvestFixture.CategoryRecordId && x.Query.Admissible).Command;
            var currentPreview = s.QueryCommand(authority, start);
            Require(currentPreview.Admissible, "Fresh query did not admit the existing harvest procedure.");
            ArchitectureCommit(s, authority, start);
            var working = s.Capture().HarvestAttempts.Single();
            Require(working.WorkerId == worker && working.Status == HarvestAttemptStatus.Working
                && WorldActivityProjection.CurrentWork(s.Capture()).Any(x => x.Id == working.Id && x.ActorId == worker),
                "Procedure dispatch did not bind its existing activity and work records to the configured actor.");
            var discoveredWorkOptions = s.DiscoverCommands(authority, worker);
            var conflictViewIds = WorldActivityProjection.CurrentWork(s.Capture()).Select(x => x.Id).ToArray();
            var activity = WorldActivityProjection.CurrentWork(s.Capture(), discoveredWorkOptions).Single(x => x.Id == working.Id);
            var workerInterval = s.Capture().Work.WorkerIntervals.Single(x => x.JobId == working.Id && x.WorkerId == worker);
            Require(conflictViewIds.SequenceEqual(WorldActivityProjection.CurrentWork(s.Capture(), discoveredWorkOptions).Select(x => x.Id))
                && activity.Status == working.Status.ToString() && activity.RecordedWorkDone == working.WorkDone
                && activity.RecordedWorkRequired == working.Duration && activity.WorkerIntervals.Count == 1
                && activity.WorkerIntervals[0].Id == workerInterval.Id
                && activity.ResourceReservations.SequenceEqual(s.Capture().Work.Reservations.Where(x => x.JobId == working.Id))
                && activity.NextWorkerBoundary == workerInterval.End
                && activity.AvailableCommands.Any(x => x.Command.Kind == CommandKind.PauseHarvest && x.Query.Admissible),
                "The derived activity view did not expose stored harvest progress, linked claims, its next worker boundary, and the discovered pause option.");

            if (contender != null)
            {
                var contested = ArchitectureHarvestStart(s, contender);
                var contentionQuery = s.QueryCommand(authority, contested);
                Require(contentionQuery.Supported && !contentionQuery.Admissible && contentionQuery.Code == "HarvestSelectionExhausted",
                    "Two eligible workers were permitted to claim the same finite body.");
                ArchitectureRejectUnchanged(s, authority, contested, "HarvestSelectionExhausted");
            }

            Require(s.Capture().RuleClock.Numerator < 200 && s.Capture().RuleClock.Denominator == 1,
                "The configured interruption marker must remain ahead of the scenario work.");
            ArchitectureAdvanceTo(s, authority, 200);
            var interruption = new Command("architecture.condition." + s.Capture().Revision, worker, s.Capture().Revision,
                CommandKind.DispatchConditionEvent, "event.architecture-stun");
            ArchitectureCommit(s, authority, interruption);
            var paused = s.Capture().HarvestAttempts.Single();
            Require(paused.Status == HarvestAttemptStatus.Paused && paused.WorkDone > default(RuleTime)
                && !s.Capture().Work.WorkerIntervals.Any(x => x.JobId == paused.Id && x.Start <= s.Capture().RuleClock && x.End > s.Capture().RuleClock),
                "The existing condition interruption did not pause work at its exact earned-progress boundary.");

            // A different actor can still explore while the companion's procedure is paused.
            ArchitectureMove(s, policy, authority, TestOnlyPolicy.ActorId, 0, 1);
            string pausedPath = Path.Combine(directory, configuration.Id + ".paused.ddsave");
            store.Save(pausedPath, s.Capture());
            var saved = s.Capture();
            s = new Simulation(policy, store.Load(pausedPath), ExecutionProfile.Laboratory);
            Require(Bytes(s).SequenceEqual(Bytes(new Simulation(policy, saved, ExecutionProfile.Laboratory)))
                && s.Capture().HarvestAttempts.Single().WorkDone == paused.WorkDone,
                "Paused work, claims, or its exact progress changed across disk save/load.");

            ArchitectureAdvanceTo(s, authority, 220);
            Require(s.Capture().HarvestAttempts.Single().Status == HarvestAttemptStatus.Paused,
                "Condition recovery automatically resumed a saved job.");
            var resume = new Command("architecture.resume." + s.Capture().Revision, worker, s.Capture().Revision,
                CommandKind.ResumeHarvest, paused.Id);
            var resumePreview = s.QueryCommand(authority, resume);
            Require(resumePreview.Supported && resumePreview.Admissible, "Explicit legal resume was not discoverable through the shared query path.");
            ArchitectureCommit(s, authority, resume);
            var progress = s.Capture().HarvestAttempts.Single();
            var remaining = ArchitectureDifference(progress.Duration, progress.WorkDone);
            Require(remaining.Denominator == 1, "Existing procedure has an unexpected fractional remainder.");
            ArchitectureCommit(s, authority, ArchitectureAdvance(s, checked((int)remaining.Numerator)));

            var result = s.Capture();
            var unit = result.HarvestUnits.Single(x => x.Id == configuration.FiniteLotId);
            var lot = result.Work.Lots.Single(x => x.Id == configuration.FiniteLotId);
            var inventory = result.InventoryLots.Single(x => x.LotId == configuration.FiniteLotId);
            var cargo = result.PortableEquipment.Single(x => x.Id == configuration.FiniteLotId);
            Require(result.HarvestAttempts.Single().Status == HarvestAttemptStatus.Success && unit.Status == HarvestUnitStatus.Extracted,
                "Configured harvest did not complete successfully: " + result.HarvestAttempts.Single().Status + "/" + unit.Status + ".");
            Require(lot.Amount == unit.MassPounds && lot.UnitId == SharedHarvestFixture.MaterialUnit
                && inventory.OwnerId == configuration.Actors.OrderBy(x => x.Id, StringComparer.Ordinal).First().Id
                && inventory.FreshUntil == unit.OriginAt.AddSeconds(unit.PreservationIntervalSeconds),
                "Completed harvest lot lost material provenance, quantity, owner, or freshness.");
            Require(cargo.LinkedId == configuration.FiniteLotId && cargo.MassBasis == PortableMassBasis.GenericPounds
                && PortableEquipmentValidation.Mass(result, cargo) == unit.MassPounds,
                "Completed harvest portable mass mismatch: link=" + cargo.LinkedId + ", basis=" + cargo.MassBasis
                + ", computed weight=" + PortableEquipmentValidation.Mass(result, cargo) + ", unit mass=" + unit.MassPounds + ".");
            Require(result.FishingCreatures.Single().MassPounds == new RuleQuantity(1) - unit.MassPounds,
                "Completed harvest did not debit the extracted mass from the remains.");

            // Carry the result using the existing physical-equipment command, then save and resume exploration.
            var retrieve = new Command("architecture.retrieve." + result.Revision, worker, result.Revision,
                CommandKind.HandlePortableEquipment, configuration.FiniteLotId,
                inventory: new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Retrieve));
            ArchitectureCommit(s, authority, retrieve);
            var carried = s.Capture();
            var carriedLot = carried.InventoryLots.Single(x => x.LotId == configuration.FiniteLotId);
            var carriedItem = carried.PortableEquipment.Single(x => x.Id == configuration.FiniteLotId);
            Require(carriedItem.Placement == PortablePlacement.Carried && carriedItem.CustodianId == worker
                && carriedLot.OwnerId == inventory.OwnerId && carriedLot.FreshUntil == inventory.FreshUntil
                && carriedLot.CreatedAmount == inventory.CreatedAmount, "Carrying the harvested result changed its lot identity, ownership, mass, or age.");
            string carriedPath = Path.Combine(directory, configuration.Id + ".carried.ddsave");
            store.Save(carriedPath, carried);
            s = new Simulation(policy, store.Load(carriedPath), ExecutionProfile.Laboratory);
            var afterCarry = s.Capture().Actors.Single(x => x.Id == worker);
            var next = afterCarry.Y > 0 ? new[] { 0, -1 } : new[] { 0, 1 };
            ArchitectureMove(s, policy, authority, worker, next[0], next[1]);
            Require(s.Capture().Actors.Single(x => x.Id == worker).Y == afterCarry.Y + next[1]
                && s.Capture().PortableEquipment.Single(x => x.Id == configuration.FiniteLotId).CustodianId == worker,
                "Exploration did not continue with the saved physical output in the configured actor's custody.");
        }

        private static void AddSharedWorldArchitectureCases(Dictionary<string, Action> cases, string directory)
        {
            cases.Add("shared_world_data_defined_handlers_run_two_distinct_configurations", () => {
                var first = ArchitectureConfiguration("scenario.river.west", "site.river.west", 1, 3,
                    "lot.fish.west", new SharedActorInstanceDefinition("worker.west", "profile.numeric-warrior3", 1, 1));
                var second = ArchitectureConfiguration("scenario.river.east", "site.river.east", 0, 4,
                    "lot.fish.east", new SharedActorInstanceDefinition("worker.east", "profile.numeric-warrior3", 4, 4),
                    new SharedActorInstanceDefinition("worker.east.second", "profile.numeric-warrior3", 0, 3));
                var westPolicy = new TestOnlySharedWorldPolicy(first, new SharedCombatFixture(1, seed: 1), new SharedHarvestFixture(),
                    conditions: new ConditionCombatFixture(CCApply("architecture-stun", "Stunned", "worker.west",
                        new ConditionStamp(T(220)), new ConditionStamp(T(200)))));
                var eastPolicy = new TestOnlySharedWorldPolicy(second, new SharedCombatFixture(1, seed: 1), new SharedHarvestFixture(),
                    conditions: new ConditionCombatFixture(CCApply("architecture-stun", "Stunned", "worker.east",
                        new ConditionStamp(T(220)), new ConditionStamp(T(200)))));
                Require(westPolicy.ContentFingerprint != eastPolicy.ContentFingerprint,
                    "Different stable world content resolved to the same fingerprint.");
                RunWorldArchitectureScenario(first, "worker.west", new[] { "0,1", "0,1" }, null, Path.Combine(directory, "west"));
                RunWorldArchitectureScenario(second, "worker.east", new[] { "-1,0", "-1,0", "-1,0" }, "worker.east.second", Path.Combine(directory, "east"));
            });
        }
    }
}
#endif
