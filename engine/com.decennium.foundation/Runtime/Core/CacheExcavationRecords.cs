using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    public enum CacheExcavationStatus { Working = 1, Paused = 2, Completed = 3 }

    /// <summary>Physical state for one explicitly authored, initially buried supply cache.</summary>
    public sealed class BuriedCacheSiteRecord
    {
        public string CacheId { get; }
        public string ShovelId { get; }
        public int X { get; }
        public int Y { get; }
        public RuleTime? ExposedAt { get; }
        public bool Buried => !ExposedAt.HasValue;

        public BuriedCacheSiteRecord(string cacheId, string shovelId, int x, int y, RuleTime? exposedAt = null)
        {
            if (!Validation.ValidId(cacheId) || !Validation.ValidId(shovelId) || x < 0 || y < 0)
                throw new ArgumentException("Invalid buried-cache site.");
            CacheId = cacheId; ShovelId = shovelId; X = x; Y = y; ExposedAt = exposedAt;
        }
        public BuriedCacheSiteRecord Expose(RuleTime at)
        {
            if (ExposedAt.HasValue) throw new InvalidOperationException("Cache is already exposed.");
            return new BuriedCacheSiteRecord(CacheId, ShovelId, X, Y, at);
        }
    }

    /// <summary>Persistent finite work on one buried cache. WorkDone is exact shared-clock labor seconds.</summary>
    public sealed class CacheExcavationRecord
    {
        public const int RequiredWorkSeconds = 300;
        public string Id { get; }
        public string AssignmentId { get; }
        public string CacheId { get; }
        public string WorkerId { get; }
        public string ShovelId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime WorkDone { get; }
        public CacheExcavationStatus Status { get; }

        public CacheExcavationRecord(string id, string assignmentId, string cacheId, string workerId, string shovelId,
            RuleTime startedAt, RuleTime updatedAt, RuleTime workDone, CacheExcavationStatus status)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(assignmentId) || !Validation.ValidId(cacheId)
                || !Validation.ValidId(workerId) || !Validation.ValidId(shovelId) || startedAt > updatedAt
                || workDone > new RuleTime(RequiredWorkSeconds) || !Enum.IsDefined(typeof(CacheExcavationStatus), status)
                || (status == CacheExcavationStatus.Completed) != (workDone == new RuleTime(RequiredWorkSeconds)))
                throw new ArgumentException("Invalid cache excavation progress.");
            Id = id; AssignmentId = assignmentId; CacheId = cacheId; WorkerId = workerId; ShovelId = shovelId;
            StartedAt = startedAt; UpdatedAt = updatedAt; WorkDone = workDone; Status = status;
        }
        public CacheExcavationRecord WithWork(RuleTime at, RuleTime workDone, CacheExcavationStatus status)
            => new CacheExcavationRecord(Id, AssignmentId, CacheId, WorkerId, ShovelId, StartedAt, at, workDone, status);
    }

    public static class CacheExcavationValidation
    {
        public const int MaxSites = 1, MaxExcavations = 1;
        private static RuleTime Add(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((BigInteger)a.Numerator * b.Denominator + (BigInteger)b.Numerator * a.Denominator,
                (BigInteger)a.Denominator * b.Denominator);
        private static RuleTime Subtract(RuleTime a, RuleTime b)
            => RuleTime.FromFraction((BigInteger)a.Numerator * b.Denominator - (BigInteger)b.Numerator * a.Denominator,
                (BigInteger)a.Denominator * b.Denominator);
        public static void Validate(Snapshot s)
        {
            if (s.BuriedCacheSites == null || s.CacheExcavations == null
                || s.BuriedCacheSites.Length > MaxSites || s.CacheExcavations.Length > MaxExcavations
                || s.BuriedCacheSites.Any(x => x == null) || s.CacheExcavations.Any(x => x == null))
                throw new ArgumentException("Invalid cache excavation collections.");
            if (s.SchemaVersion < Snapshot.BuriedCacheSchema)
            {
                if (s.BuriedCacheSites.Length != 0 || s.CacheExcavations.Length != 0)
                    throw new ArgumentException("Cache excavation requires schema57.");
                return;
            }
            // Later schemas may add unrelated optional records without selecting the optional
            // buried-cache fixture. Its founding schema still requires the authored site.
            if(s.SchemaVersion>Snapshot.BuriedCacheSchema&&s.BuriedCacheSites.Length==0&&s.CacheExcavations.Length==0)return;
            if (s.BuriedCacheSites.Length != 1 || s.SupplyCaches.Length != 1 || s.PortableEquipment.Length == 0)
                throw new ArgumentException("Schema57 requires its authored buried-cache fixture.");
            var site = s.BuriedCacheSites[0];
            var cache = s.SupplyCaches.SingleOrDefault(x => x.Id == site.CacheId);
            var shovel = s.PortableEquipment.SingleOrDefault(x => x.Id == site.ShovelId);
            if (cache == null || cache.X != site.X || cache.Y != site.Y || cache.Open && site.Buried
                || shovel == null || shovel.ProfileId != "adventuring-gear.shovel" || shovel.LinkKind != PortableLinkKind.None
                || shovel.MassBasis != PortableMassBasis.Fixed || shovel.SourceWeightLb != new RuleQuantity(5)
                || shovel.OperationalWeightLb != new RuleQuantity(5) || shovel.Placement != PortablePlacement.Ground
                || shovel.GroundX != site.X || shovel.GroundY != site.Y)
                throw new ArgumentException("Buried-cache site does not match its physical cache and shovel.");
            if (s.CacheExcavations.Length == 0)
            {
                if (!site.Buried) throw new ArgumentException("An exposed cache requires completed excavation history.");
                return;
            }
            var work = s.CacheExcavations[0];
            var assignment = s.ExpeditionAssignments.SingleOrDefault(x => x.Id == work.AssignmentId);
            if (work.CacheId != site.CacheId || work.ShovelId != site.ShovelId || work.UpdatedAt > s.RuleClock
                || assignment == null || assignment.Procedure != ExpeditionWorkProcedure.CacheExcavation
                || assignment.TargetId != site.CacheId || assignment.WorkerId != work.WorkerId || assignment.WorkId != work.Id
                || assignment.Status != ExpeditionAssignmentStatus.Started)
                throw new ArgumentException("Cache excavation is not linked to its assigned worker and site.");
            var intervals = s.Work.WorkerIntervals.Where(x => x.JobId == work.Id).ToArray();
            var open = intervals.Where(x => x.Start <= s.RuleClock && x.End > s.RuleClock).ToArray();
            if (work.Status == CacheExcavationStatus.Working)
            {
                RuleTime expectedEnd = Add(s.RuleClock,
                    Subtract(new RuleTime(CacheExcavationRecord.RequiredWorkSeconds), work.WorkDone));
                if (open.Length != 1 || open[0].WorkerId != work.WorkerId || open[0].End != expectedEnd
                    || work.WorkDone >= new RuleTime(CacheExcavationRecord.RequiredWorkSeconds) || !site.Buried)
                    throw new ArgumentException("Working cache excavation has an inconsistent worker interval or site state.");
            }
            else if (open.Length != 0) throw new ArgumentException("Paused or completed excavation still reserves active labor.");
            if (work.Status == CacheExcavationStatus.Completed)
            {
                if (site.Buried || site.ExposedAt != work.UpdatedAt || work.WorkDone != new RuleTime(CacheExcavationRecord.RequiredWorkSeconds))
                    throw new ArgumentException("Completed cache excavation did not expose the same site exactly at completion.");
            }
            else if (!site.Buried || site.ExposedAt.HasValue)
                throw new ArgumentException("Unfinished cache excavation cannot expose its site.");
            if (intervals.Any(x => x.WorkerId != work.WorkerId || x.End > s.RuleClock && x.Start > s.RuleClock))
                throw new ArgumentException("Cache excavation has an invalid or future worker reservation.");
        }
    }
}
