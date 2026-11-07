#if DECENNIUM_TEST_ONLY && (UNITY_EDITOR || DEVELOPMENT_BUILD || HEADLESS_TESTS)
using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation.Laboratory
{
    public static class CacheExcavationFixture
    {
        public const string ShovelId = "TEST_ONLY.cache-shovel";
    }

    public sealed partial class TestOnlySharedWorldPolicy
    {
        private static RuleTime AddCacheWork(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((BigInteger)a.Numerator * b.Denominator + (BigInteger)b.Numerator * a.Denominator,
                (BigInteger)a.Denominator * b.Denominator);
        private static RuleTime SubtractCacheWork(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((BigInteger)a.Numerator * b.Denominator - (BigInteger)b.Numerator * a.Denominator,
                (BigInteger)a.Denominator * b.Denominator);
        private static BuriedCacheSiteRecord BuriedCacheSite(Snapshot s, string cacheId)
            => s.BuriedCacheSites.SingleOrDefault(x => x.CacheId == cacheId);
        private static void PutCacheExcavation(Snapshot s, CacheExcavationRecord value)
            => s.CacheExcavations = s.CacheExcavations.Select(x => x.Id == value.Id ? value : x).ToArray();
        private static bool CacheExcavationCommand(Command c)
            => c.Kind == CommandKind.PauseCacheExcavation || c.Kind == CommandKind.ResumeCacheExcavation;
        private bool CacheExcavationSelected(Snapshot s)
            => cacheExcavationEnabled && s.SchemaVersion >= Snapshot.BuriedCacheSchema;

        private void InitializeBuriedCache(Snapshot s)
        {
            if (!cacheExcavationEnabled) return;
            var cache = s.SupplyCaches.Single();
            s.BuriedCacheSites = new[] { new BuriedCacheSiteRecord(cache.Id, CacheExcavationFixture.ShovelId, cache.X, cache.Y) };
            s.PortableEquipment = s.PortableEquipment.Concat(new[] { new PortableEquipmentRecord(
                CacheExcavationFixture.ShovelId, "adventuring-gear.shovel", TestOnlyPolicy.ActorId, TestOnlyPolicy.ActorId, "",
                PortablePlacement.Ground, PortableLinkKind.None, "", PortableMassBasis.Fixed, new RuleQuantity(5), new RuleQuantity(5),
                groundX: cache.X, groundY: cache.Y) }).ToArray();
        }

        private string CacheExcavationAccess(Snapshot s, ExpeditionWorkAssignmentRecord assignment,
            CacheExcavationRecord current = null)
        {
            if (!CacheExcavationSelected(s)) return "CacheExcavationNotSelected";
            if (s.InventoryCombat) return "CacheExcavationRequiresExploration";
            if (assignment == null || assignment.Procedure != ExpeditionWorkProcedure.CacheExcavation)
                return "UnknownCacheExcavationAssignment";
            var site = BuriedCacheSite(s, assignment.TargetId);
            if (site == null) return "UnknownBuriedCacheSite";
            if (!site.Buried) return "CacheAlreadyExposed";
            if (assignment.SiteX != site.X || assignment.SiteY != site.Y) return "CacheExcavationSiteChanged";
            var worker = s.Actors.SingleOrDefault(x => x.Id == assignment.WorkerId);
            if (worker == null || worker.X != site.X || worker.Y != site.Y || s.WorldTraversals.Any(x => x.ActorId == assignment.WorkerId))
                return "CacheExcavationWorkerNotAtSite";
            if (!CapableWorker(s, assignment.WorkerId)) return "CacheExcavationWorkerIncapable";
            if (AvailableHands(s, assignment.WorkerId) < 2) return "TwoHandsRequired";
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == assignment.WorkerId && x.JobId != current?.Id
                && x.Start <= s.RuleClock && x.End > s.RuleClock)
                || WorldActivityProjection.CurrentWork(s).Any(x => x.ActorId == assignment.WorkerId && x.Id != current?.Id))
                return "WorkerBusy";
            var shovel = s.PortableEquipment.SingleOrDefault(x => x.Id == site.ShovelId
                && x.ProfileId == "adventuring-gear.shovel" && x.Placement == PortablePlacement.Ground
                && x.GroundX == site.X && x.GroundY == site.Y);
            if (shovel == null || !PortableEquipmentRules.Accessible(s, assignment.WorkerId, shovel))
                return "ActualShovelUnavailable";
            return null;
        }

        private static void BookCacheExcavation(Snapshot s, CacheExcavationRecord work)
        {
            RuleTime end = AddCacheWork(s.RuleClock,
                SubtractCacheWork(new RuleTime(CacheExcavationRecord.RequiredWorkSeconds), work.WorkDone));
            int index = s.Work.WorkerIntervals.Count(x => x.JobId == work.Id);
            string intervalId = work.Id + ".labor." + index.ToString(CultureInfo.InvariantCulture);
            s.Work = s.Work.Reserve(work.Id, new[] { new WorkerInterval(intervalId, work.Id, work.WorkerId, s.RuleClock, end) },
                Array.Empty<ResourceReservation>());
        }

        private string StartCacheExcavation(Snapshot s, ExpeditionWorkAssignmentRecord assignment, out string workId)
        {
            workId = "";
            if (s.CacheExcavations.Length != 0) return "CacheExcavationAlreadyStarted";
            string failure = CacheExcavationAccess(s, assignment);
            if (failure != null) return failure;
            var site = BuriedCacheSite(s, assignment.TargetId);
            workId = "cache.excavation." + (s.Revision + 1).ToString(CultureInfo.InvariantCulture);
            var work = new CacheExcavationRecord(workId, assignment.Id, site.CacheId, assignment.WorkerId, site.ShovelId,
                s.RuleClock, s.RuleClock, default, CacheExcavationStatus.Working);
            BookCacheExcavation(s, work);
            s.CacheExcavations = s.CacheExcavations.Concat(new[] { work }).ToArray();
            return null;
        }

        private static void PauseCacheExcavation(Snapshot s, CacheExcavationRecord work)
        {
            if (work.Status != CacheExcavationStatus.Working) return;
            s.Work = s.Work.CancelFutureWork(work.Id, s.RuleClock);
            PutCacheExcavation(s, work.WithWork(s.RuleClock, work.WorkDone, CacheExcavationStatus.Paused));
        }

        private void PauseIncompatibleCacheExcavation(Snapshot s)
        {
            if (!CacheExcavationSelected(s)) return;
            foreach (var work in s.CacheExcavations.Where(x => x.Status == CacheExcavationStatus.Working).ToArray())
            {
                var assignment = s.ExpeditionAssignments.Single(x => x.Id == work.AssignmentId);
                if (CacheExcavationAccess(s, assignment, work) != null) PauseCacheExcavation(s, work);
            }
        }

        private static RuleTime? NextCacheExcavationBoundary(Snapshot s)
        {
            var ends = s.CacheExcavations.Where(x => x.Status == CacheExcavationStatus.Working)
                .Select(x => s.Work.WorkerIntervals.Single(w => w.JobId == x.Id && w.Start <= s.RuleClock && w.End > s.RuleClock).End)
                .ToArray();
            return ends.Length == 0 ? (RuleTime?)null : ends.Min();
        }

        private static void CreditCacheExcavationWork(Snapshot s, RuleTime elapsed)
        {
            foreach (var work in s.CacheExcavations.Where(x => x.Status == CacheExcavationStatus.Working).ToArray())
            {
                if (!s.Work.WorkerIntervals.Any(w => w.JobId == work.Id && w.Start <= work.UpdatedAt && w.End >= s.RuleClock)) continue;
                RuleTime progress = AddCacheWork(work.WorkDone, elapsed);
                if (progress >= new RuleTime(CacheExcavationRecord.RequiredWorkSeconds))
                {
                    var complete = work.WithWork(s.RuleClock, new RuleTime(CacheExcavationRecord.RequiredWorkSeconds), CacheExcavationStatus.Completed);
                    PutCacheExcavation(s, complete);
                    var site = BuriedCacheSite(s, work.CacheId);
                    s.BuriedCacheSites = s.BuriedCacheSites.Select(x => x.CacheId == site.CacheId ? site.Expose(s.RuleClock) : x).ToArray();
                }
                else PutCacheExcavation(s, work.WithWork(s.RuleClock, progress, CacheExcavationStatus.Working));
            }
        }

        private CommandQueryResult QueryCacheExcavationControl(Snapshot s, Command c)
        {
            if (!CacheExcavationCommand(c)) return new CommandQueryResult(false, false, "UnsupportedOperation", s.Revision);
            string failure = AssessCacheExcavationControl(s, c, out var work);
            var costs = new System.Collections.Generic.List<CommandCost>();
            if (failure == null && c.Kind == CommandKind.ResumeCacheExcavation)
            {
                RuleTime remaining = SubtractCacheWork(new RuleTime(CacheExcavationRecord.RequiredWorkSeconds), work.WorkDone);
                if (remaining.Denominator == 1) costs.Add(new CommandCost("work-seconds", "", remaining.Numerator));
            }
            return new CommandQueryResult(true, failure == null, failure ?? "Available", s.Revision, costs);
        }

        private string AssessCacheExcavationControl(Snapshot s, Command c, out CacheExcavationRecord work)
        {
            work = null;
            if (!CacheExcavationSelected(s)) return "CacheExcavationNotSelected";
            if (c.Inventory != null || c.Combat != null || c.Target == "" || c.X != 0 || c.Y != 0)
                return "InvalidCacheExcavationCommand";
            if (s.InventoryCombat) return "CacheExcavationRequiresExploration";
            var current = s.CacheExcavations.SingleOrDefault(x => x.Id == c.Target && x.WorkerId == c.Actor);
            work = current;
            if (current == null) return "UnknownCacheExcavation";
            if (c.Kind == CommandKind.PauseCacheExcavation)
                return current.Status == CacheExcavationStatus.Working ? null : "CacheExcavationNotWorking";
            if (c.Kind != CommandKind.ResumeCacheExcavation) return "InvalidCacheExcavationCommand";
            if (current.Status == CacheExcavationStatus.Working) return "CacheExcavationAlreadyWorking";
            if (current.Status == CacheExcavationStatus.Completed) return "CacheExcavationComplete";
            var assignment = s.ExpeditionAssignments.SingleOrDefault(x => x.Id == current.AssignmentId && x.WorkerId == c.Actor);
            return CacheExcavationAccess(s, assignment, current);
        }

        private string ResolveCacheExcavationControl(Snapshot s, Command c)
        {
            string failure = AssessCacheExcavationControl(s, c, out var work);
            if (failure != null) return failure;
            if (c.Kind == CommandKind.PauseCacheExcavation) PauseCacheExcavation(s, work);
            else
            {
                var resumed = work.WithWork(s.RuleClock, work.WorkDone, CacheExcavationStatus.Working);
                BookCacheExcavation(s, resumed);
                PutCacheExcavation(s, resumed);
            }
            return null;
        }

        private IEnumerable<Command> DiscoverCacheExcavationControls(Snapshot s, string actor)
        {
            var work = s.CacheExcavations.SingleOrDefault(x => x.WorkerId == actor
                && (x.Status == CacheExcavationStatus.Working || x.Status == CacheExcavationStatus.Paused));
            if (work == null) yield break;
            CommandKind kind = work.Status == CacheExcavationStatus.Working
                ? CommandKind.PauseCacheExcavation : CommandKind.ResumeCacheExcavation;
            yield return new Command("option." + s.Revision.ToString(CultureInfo.InvariantCulture) + ".cache-excavation",
                actor, s.Revision, kind, work.Id);
        }
    }
}
#endif
