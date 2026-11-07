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
        private static void AddCacheExcavationCases(Dictionary<string, Action> cases, string directory)
        {
            var host = TestOnlySharedWorldPolicy.Host();
            const string worker = TestOnlyPolicy.CompanionId;
            cases.Add("cache_excavation_assignment_resumes_exact_work_and_exposes_cache_once", () => {
                var manifest = TestOnlyContentManifest.CreateBuriedCacheExcavationProfile();
                var policy = new TestOnlySharedWorldPolicy(manifest, new PortableKitFixture(),
                    new SharedCombatFixture(seed: SuccessfulPickSeed(true)), new SupplyCacheFixture()).EnableBuriedCacheExcavation();
                var s = World(policy);
                var initial = s.Capture();
                var site = initial.BuriedCacheSites.Single();
                var shovel = initial.PortableEquipment.Single(x => x.Id == CacheExcavationFixture.ShovelId);
                Require(initial.SchemaVersion == Snapshot.BuriedCacheSchema && site.Buried
                    && site.CacheId == SupplyCacheFixture.CacheId && site.X == SupplyCacheFixture.CacheX
                    && site.Y == SupplyCacheFixture.CacheY && initial.CacheExcavations.Length == 0
                    && shovel.ProfileId == "adventuring-gear.shovel" && shovel.Placement == PortablePlacement.Ground
                    && shovel.GroundX == site.X && shovel.GroundY == site.Y,
                    "The opt-in profile did not create one buried physical cache and its actual shovel.");

                PortableMoveToCache(s);
                var hiddenOptions = s.DiscoverCommands(host, TestOnlyPolicy.ActorId);
                Require(!hiddenOptions.Any(x => x.Command.Target == site.CacheId),
                    "A buried cache leaked through inventory access or contextual command discovery.");
                RejectUnchanged(s, host, SupplyCommand(s, SupplyCacheInteraction.Open), "SupplyCacheBuried");
                RejectUnchanged(s, host, IC(s, CommandKind.HandleInventory, TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Pickup)), "InventoryOutOfReach");
                WorldStep(s, -1, 0); WorldAdvance(s, 3, 2);
                WorldStep(s, 0, -1); WorldAdvance(s, 3, 2);

                var request = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.CacheExcavation, site.CacheId);
                WorldCommit(s, ExpeditionCommand(s, CommandKind.AssignExpeditionWork, request: request, actor: worker));
                var assignment = s.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Travelling
                    && assignment.SiteX == site.X && assignment.SiteY == site.Y,
                    "The assignment did not derive its destination from the authored cache site.");
                WorldStep(s, -1, 0, actor: worker); WorldAdvance(s, 1);
                WorldStep(s, -1, 0, actor: worker); WorldAdvance(s, 1);
                WorldStep(s, 0, -1, actor: worker); WorldAdvance(s, 1);
                assignment = s.Capture().ExpeditionAssignments.Single();
                Require(assignment.Status == ExpeditionAssignmentStatus.Ready,
                    "The remote worker did not become ready at the cache after exploration movement.");
                var start = ExpeditionCommand(s, CommandKind.StartExpeditionWork, assignment.Id, actor: worker);
                WorldCommit(s, start);
                var work = s.Capture().CacheExcavations.Single();
                Require(work.Status == CacheExcavationStatus.Working && work.WorkDone == default
                    && s.Capture().ExpeditionAssignments.Single().WorkId == work.Id,
                    "Starting the assignment did not reserve the actual worker, shovel, and finite excavation job.");
                WorldAdvance(s, 100);
                var running = s.Capture(); work = running.CacheExcavations.Single();
                var options = s.DiscoverCommands(host, worker);
                var projection = WorldActivityProjection.CurrentWork(running, options).Single(x => x.Id == work.Id);
                Require(work.WorkDone == new RuleTime(100) && work.Status == CacheExcavationStatus.Working
                    && projection.Kind == WorldProcedureKind.CacheExcavation
                    && projection.RecordedWorkDone == new RuleTime(100)
                    && projection.RecordedWorkRequired == new RuleTime(CacheExcavationRecord.RequiredWorkSeconds)
                    && projection.AvailableCommands.Any(x => x.Command.Kind == CommandKind.PauseCacheExcavation),
                    "Excavation labor or its shared activity projection did not advance exactly.");

                var pause = new Command("cache-excavation.pause", worker, running.Revision,
                    CommandKind.PauseCacheExcavation, work.Id);
                WorldCommit(s, pause);
                var forgedProgress = s.Capture();
                var pausedRecord = forgedProgress.CacheExcavations.Single();
                forgedProgress.CacheExcavations = new[] { pausedRecord.WithWork(pausedRecord.UpdatedAt,
                    new RuleTime(101), CacheExcavationStatus.Paused) };
                string forgedError = "";
                try { new Simulation(policy, forgedProgress, ExecutionProfile.Laboratory); }
                catch (ArgumentException error) { forgedError = error.Message; }
                Require(forgedError == "InvalidSharedWorldReplay",
                    "A paused progress edit without matching worker-time history must fail canonical replay; got " + forgedError + ".");
                string path = Path.Combine(directory, "cache-excavation-paused.bin");
                var store = new FileSaveStore(); store.Save(path, s.Capture());
                var pausedBytes = Bytes(s);
                s = new Simulation(policy, store.Load(path), ExecutionProfile.Laboratory);
                Require(pausedBytes.SequenceEqual(Bytes(s)) && s.Capture().CacheExcavations.Single().Status == CacheExcavationStatus.Paused,
                    "Paused labor or its retained shovel claim changed across save/restore.");
                WorldAdvance(s, 90);
                Require(s.Capture().CacheExcavations.Single().WorkDone == new RuleTime(100)
                    && s.Capture().BuriedCacheSites.Single().Buried,
                    "Paused excavation gained labor or exposed its cache.");
                var current = s.Capture(); work = current.CacheExcavations.Single();
                WorldCommit(s, new Command("cache-excavation.resume", worker, current.Revision,
                    CommandKind.ResumeCacheExcavation, work.Id));
                WorldAdvance(s, 199);
                var almost = s.Capture(); work = almost.CacheExcavations.Single();
                Require(work.Status == CacheExcavationStatus.Working && work.WorkDone == new RuleTime(299)
                    && almost.BuriedCacheSites.Single().Buried,
                    "The site exposed before the final active work second.");
                WorldAdvance(s, 1);
                var completed = s.Capture(); work = completed.CacheExcavations.Single();
                site = completed.BuriedCacheSites.Single();
                Require(work.Status == CacheExcavationStatus.Completed
                    && work.WorkDone == new RuleTime(CacheExcavationRecord.RequiredWorkSeconds)
                    && site.ExposedAt == completed.RuleClock && !site.Buried
                    && completed.SupplyCaches.Single().Locked && !completed.SupplyCaches.Single().Open,
                    "Completing the exact retained labor did not expose the same still-locked physical cache.");
                RejectUnchanged(s, host, SupplyCommand(s, SupplyCacheInteraction.Open), "SupplyCacheOutOfReach");

                // Exposure removes only the burial gate. Ordinary reach, lock, opening and stock
                // custody rules still resolve through the existing cache and inventory handlers.
                WorldStep(s, 0, 1, actor: worker); WorldAdvance(s, 1);
                WorldStep(s, 1, 0); WorldAdvance(s, 2);
                WorldStep(s, 0, 1); WorldAdvance(s, 2);
                PortableCommit(s, Portable(s, CommandKind.HandlePortableEquipment, PortableKitFixture.Tools,
                    handling: HandlingKind.Retrieve));
                var atCache = s.Capture();
                var cacheBefore = atCache.SupplyCaches.Single();
                var heroAtCache = atCache.Actors.Single(x => x.Id == TestOnlyPolicy.ActorId);
                var cacheOptions = s.DiscoverCommands(host, TestOnlyPolicy.ActorId).ToArray();
                Require(cacheBefore.Id == site.CacheId && cacheBefore.OwnerId == TestOnlyPolicy.ActorId
                    && cacheBefore.Locked && !cacheBefore.Open
                    && cacheOptions.Any(x => x.Command.Target == site.CacheId
                        && x.Command.X == (int)SupplyCacheInteraction.PickWithTools),
                    "After exposure, the existing cache identity, lock or lawful tools interaction was not available. Hero=("
                        + heroAtCache.X + "," + heroAtCache.Y + "), traversals=" + atCache.WorldTraversals.Length
                        + ", options=" + string.Join(";", cacheOptions.Select(x => x.Command.Kind + "/" + x.Command.Target
                            + "/" + x.Command.X + "/" + x.Query.Code)) + ".");
                SupplyCommit(s, SupplyCommand(s, SupplyCacheInteraction.PickWithTools));
                WorldAdvance(s, 6);
                Require(s.Capture().SupplyCacheAttempts.Single().Status == SupplyCacheAttemptStatus.Succeeded
                    && !s.Capture().SupplyCaches.Single().Locked,
                    "The existing six-second lock procedure did not succeed after exposure.");
                SupplyCommit(s, SupplyCommand(s, SupplyCacheInteraction.Open));
                var openedState = s.Capture();
                Require(openedState.SupplyCaches.Single().Id == site.CacheId
                    && !openedState.SupplyCaches.Single().Locked && openedState.SupplyCaches.Single().Open
                    && openedState.Work.Lots.Single(x => x.Id == TestOnlyInventoryPolicy.FoodId).Amount
                        == atCache.Work.Lots.Single(x => x.Id == TestOnlyInventoryPolicy.FoodId).Amount,
                    "Opening after exposure changed cache identity or generated/reduced its finite stock.");
                SupplyCommit(s, IC(s, CommandKind.HandleInventory, TestOnlyInventoryPolicy.FoodId,
                    new InventoryRequest(new RuleQuantity(1), handling: HandlingKind.Pickup)));
                var retrieved = s.Capture();
                var foodChild = retrieved.InventoryLots.Single(x => x.ParentId == TestOnlyInventoryPolicy.FoodId);
                Require(retrieved.SupplyCaches.Single().Id == site.CacheId
                    && foodChild.OwnerId == TestOnlyPolicy.ActorId && foodChild.CreatedAmount == new RuleQuantity(1)
                    && retrieved.Work.Lots.Single(x => x.Id == TestOnlyInventoryPolicy.FoodId).Amount
                        == openedState.Work.Lots.Single(x => x.Id == TestOnlyInventoryPolicy.FoodId).Amount - new RuleQuantity(1),
                    "Existing retrieval did not conserve the original finite stock and its ownership lineage.");
                var finalBytes = Bytes(s);
                var restored = new Simulation(policy, new SnapshotCodec().Decode(finalBytes), ExecutionProfile.Laboratory);
                Require(finalBytes.SequenceEqual(Bytes(restored))
                    && restored.Capture().BuriedCacheSites.Single().ExposedAt == completed.RuleClock
                    && restored.Capture().CacheExcavations.Single().Status == CacheExcavationStatus.Completed,
                    "Completed excavation and later cache retrieval did not preserve exposure, custody and stock across persistence.");
            });

            cases.Add("cache_excavation_requires_assignment_site_and_can_only_be_started_once", () => {
                var policy = PortablePolicy().EnableBuriedCacheExcavation();
                var s = World(policy);
                var site = s.Capture().BuriedCacheSites.Single();
                var request = new ExpeditionAssignmentRequest(ExpeditionWorkProcedure.CacheExcavation, site.CacheId);
                WorldCommit(s, ExpeditionCommand(s, CommandKind.AssignExpeditionWork, request: request, actor: worker));
                var assignment = s.Capture().ExpeditionAssignments.Single();
                RejectUnchanged(s, host, ExpeditionCommand(s, CommandKind.StartExpeditionWork, assignment.Id, actor: worker),
                    "ExpeditionAssignmentNotReady");
                WorldStep(s, -1, 0, actor: worker); WorldAdvance(s, 1);
                WorldStep(s, -1, 0, actor: worker); WorldAdvance(s, 1);
                WorldStep(s, 0, -1, actor: worker); WorldAdvance(s, 1);
                assignment = s.Capture().ExpeditionAssignments.Single();
                WorldCommit(s, ExpeditionCommand(s, CommandKind.StartExpeditionWork, assignment.Id, actor: worker));
                var work = s.Capture().CacheExcavations.Single();
                RejectUnchanged(s, host, new Command("cache-excavation-duplicate-start", worker,
                    s.Capture().Revision, CommandKind.StartExpeditionWork, assignment.Id), "ExpeditionAssignmentNotReady");
                Require(s.Capture().CacheExcavations.Length == 1 && work.Status == CacheExcavationStatus.Working,
                    "A repeated assignment start created a second excavation.");
            });
        }
    }
}
#endif
