using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ExpeditionCampActivityKind { Use = 1, LyingLow = 2 }
    public enum ExpeditionCampActivityEndReason { Command = 1, Combat = 2, Travel = 3, Work = 4, PressureClosure = 5 }

    /// <summary>Immutable TEST_ONLY site facts bound to an exact checkpoint in an authored route.
    /// It contains no construction, storage, safety, discovery, or Haven result.</summary>
    public sealed class ExpeditionCampSiteRecord
    {
        public string Id { get; }
        public string CohortId { get; }
        public string RouteId { get; }
        public RuleQuantity RouteProgress { get; }
        public string RouteFingerprint { get; }
        public string ProfileFingerprint { get; }
        public int RouteX { get; }
        public int RouteY { get; }
        public int FootprintWidthFeet { get; }
        public int FootprintHeightFeet { get; }
        public bool LegalAccess { get; }
        public bool Stable { get; }
        public bool Drainage { get; }
        public bool WeatherProtection { get; }
        public bool InhabitantSpace { get; }
        public bool GearSpace { get; }
        public bool Exposed { get; }
        public bool KnownToEnemies { get; }
        public bool Concealed { get; }

        public ExpeditionCampSiteRecord(string id, string cohortId, string routeId, RuleQuantity routeProgress,
            string routeFingerprint, string profileFingerprint, int routeX, int routeY,
            int footprintWidthFeet, int footprintHeightFeet,
            bool legalAccess, bool stable, bool drainage, bool weatherProtection, bool inhabitantSpace,
            bool gearSpace, bool exposed, bool knownToEnemies, bool concealed)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(cohortId) || !Validation.ValidId(routeId)
                || routeProgress < default(RuleQuantity) || string.IsNullOrEmpty(routeFingerprint) || routeFingerprint.Length > 96
                || string.IsNullOrEmpty(profileFingerprint) || profileFingerprint.Length > 96
                || routeX < 0 || routeY < 0 || footprintWidthFeet != 20 || footprintHeightFeet != 20)
                throw new ArgumentException("Invalid TEST_ONLY camp site facts or route binding.");
            Id = id; CohortId = cohortId; RouteId = routeId; RouteProgress = routeProgress;
            RouteFingerprint = routeFingerprint; ProfileFingerprint = profileFingerprint;
            RouteX = routeX; RouteY = routeY;
            FootprintWidthFeet = footprintWidthFeet; FootprintHeightFeet = footprintHeightFeet;
            LegalAccess = legalAccess; Stable = stable; Drainage = drainage;
            WeatherProtection = weatherProtection; InhabitantSpace = inhabitantSpace; GearSpace = gearSpace;
            Exposed = exposed; KnownToEnemies = knownToEnemies; Concealed = concealed;
        }

        public bool SameAs(ExpeditionCampSiteRecord x) => x != null && Id == x.Id && CohortId == x.CohortId
            && RouteId == x.RouteId && RouteProgress == x.RouteProgress && RouteFingerprint == x.RouteFingerprint
            && ProfileFingerprint == x.ProfileFingerprint && RouteX == x.RouteX && RouteY == x.RouteY
            && FootprintWidthFeet == x.FootprintWidthFeet
            && FootprintHeightFeet == x.FootprintHeightFeet && LegalAccess == x.LegalAccess && Stable == x.Stable
            && Drainage == x.Drainage && WeatherProtection == x.WeatherProtection
            && InhabitantSpace == x.InhabitantSpace && GearSpace == x.GearSpace && Exposed == x.Exposed
            && KnownToEnemies == x.KnownToEnemies && Concealed == x.Concealed;

        public bool SupportsUse => LegalAccess && Stable && Drainage && WeatherProtection
            && InhabitantSpace && GearSpace;
    }

    /// <summary>One actual, receipt-bound camp-use or lying-low interval. Lying-low intervals are
    /// nested in a physical Use interval; ending lying low need not end camp occupancy.</summary>
    public sealed class ExpeditionCampActivityRecord
    {
        public string Id { get; }
        public string CohortId { get; }
        public string ExposureId { get; }
        public string CampId { get; }
        public ExpeditionCampActivityKind Kind { get; }
        public string ParentUseId { get; }
        public RuleTime StartedAt { get; }
        public long StartedRevision { get; }
        public string StartCommandId { get; }
        public RuleTime? EndedAt { get; }
        public long EndRevision { get; }
        public string EndCommandId { get; }
        public ExpeditionCampActivityEndReason EndReason { get; }

        public ExpeditionCampActivityRecord(string id, string cohortId, string exposureId, string campId,
            ExpeditionCampActivityKind kind, string parentUseId, RuleTime startedAt, long startedRevision,
            string startCommandId, RuleTime? endedAt = null, long endRevision = 0, string endCommandId = "",
            ExpeditionCampActivityEndReason endReason = 0)
        {
            bool isUse = kind == ExpeditionCampActivityKind.Use;
            if (!Validation.ValidId(id) || !Validation.ValidId(cohortId) || !Validation.ValidId(exposureId)
                || !Validation.ValidId(campId) || !Enum.IsDefined(typeof(ExpeditionCampActivityKind), kind)
                || (isUse ? parentUseId != "" : !Validation.ValidId(parentUseId))
                || startedAt < default(RuleTime) || startedRevision < 1 || !Validation.ValidId(startCommandId)
                || endedAt.HasValue != (endRevision > 0) || endedAt.HasValue != (endCommandId.Length > 0)
                || endedAt.HasValue != Enum.IsDefined(typeof(ExpeditionCampActivityEndReason), endReason)
                || endRevision != 0 && endRevision <= startedRevision || endedAt.HasValue && endedAt.Value < startedAt)
                throw new ArgumentException("Invalid camp activity interval.");
            Id = id; CohortId = cohortId; ExposureId = exposureId; CampId = campId; Kind = kind;
            ParentUseId = parentUseId; StartedAt = startedAt; StartedRevision = startedRevision;
            StartCommandId = startCommandId; EndedAt = endedAt; EndRevision = endRevision;
            EndCommandId = endCommandId; EndReason = endReason;
        }

        public bool Active => !EndedAt.HasValue;
        public ExpeditionCampActivityRecord End(RuleTime at, long revision, string commandId,
            ExpeditionCampActivityEndReason reason)
            => new ExpeditionCampActivityRecord(Id, CohortId, ExposureId, CampId, Kind, ParentUseId,
                StartedAt, StartedRevision, StartCommandId, at, revision, commandId, reason);

        public bool SameAs(ExpeditionCampActivityRecord x) => x != null && Id == x.Id
            && CohortId == x.CohortId && ExposureId == x.ExposureId && CampId == x.CampId && Kind == x.Kind
            && ParentUseId == x.ParentUseId && StartedAt == x.StartedAt && StartedRevision == x.StartedRevision
            && StartCommandId == x.StartCommandId && EndedAt == x.EndedAt && EndRevision == x.EndRevision
            && EndCommandId == x.EndCommandId && EndReason == x.EndReason;
    }

    public static class ExpeditionCampValidation
    {
        public const int MaxSites = 8;
        public const int MaxActivities = 512;

        public static void Validate(Snapshot s)
        {
            if (s.ExpeditionCampSites == null || s.ExpeditionCampActivities == null
                || s.ExpeditionCampSites.Length > MaxSites || s.ExpeditionCampActivities.Length > MaxActivities
                || s.ExpeditionCampSites.Any(x => x == null) || s.ExpeditionCampActivities.Any(x => x == null))
                throw new ArgumentException("Invalid expedition camp collections.");
            if (s.SchemaVersion < Snapshot.ExpeditionCampUseSchema)
            {
                if (s.ExpeditionCampSites.Length + s.ExpeditionCampActivities.Length != 0)
                    throw new ArgumentException("Expedition camp use requires schema69.");
                return;
            }
            if (!s.TestOnly || s.ExpeditionCampSites.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionCampSites.Length
                || s.ExpeditionCampActivities.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.ExpeditionCampActivities.Length
                || s.ExpeditionCampSites.Any(x => !s.ExpeditionPressureCohorts.Any(c => c.Id == x.CohortId)))
                throw new ArgumentException("Invalid TEST_ONLY expedition camp site references.");

            foreach (var site in s.ExpeditionCampSites)
            {
                if (site.FootprintWidthFeet != 20 || site.FootprintHeightFeet != 20
                    || site.RouteProgress < default(RuleQuantity))
                    throw new ArgumentException("Invalid TEST_ONLY expedition camp site facts.");
            }

            foreach (var activity in s.ExpeditionCampActivities)
            {
                var site = s.ExpeditionCampSites.SingleOrDefault(x => x.Id == activity.CampId
                    && x.CohortId == activity.CohortId);
                var exposure = s.ExpeditionPressureExposures.SingleOrDefault(x => x.Id == activity.ExposureId
                    && x.CohortId == activity.CohortId && x.RouteId == site?.RouteId);
                if (site == null || exposure == null || activity.StartedRevision > s.Revision
                    || activity.StartedAt > s.RuleClock || !s.Receipts.Any(r => r.Revision == activity.StartedRevision
                        && r.Id == activity.StartCommandId)
                    || activity.StartedAt < exposure.StartedAt
                    || activity.EndedAt.HasValue && exposure.EndedAt.HasValue
                        && activity.EndedAt.Value > exposure.EndedAt.Value
                    || activity.StartedAt == exposure.StartedAt && activity.StartedRevision < exposure.StartedRevision)
                    throw new ArgumentException("Invalid camp activity source references.");
                var start = CommandHistory.Read(s.Receipts.Single(r => r.Revision == activity.StartedRevision));
                CommandKind expectedStart = activity.Kind == ExpeditionCampActivityKind.Use
                    ? CommandKind.BeginCampUse : CommandKind.BeginLyingLow;
                if (start.Kind != expectedStart || start.Actor != s.ExpeditionPressureCohorts.Single(c => c.Id == activity.CohortId).Members[0]
                    || start.Target != activity.CampId)
                    throw new ArgumentException("Camp activity start is not backed by its command receipt.");

                if (activity.EndedAt.HasValue)
                {
                    var receipt = s.Receipts.SingleOrDefault(r => r.Revision == activity.EndRevision
                        && r.Id == activity.EndCommandId);
                    if (activity.EndRevision > s.Revision || activity.EndedAt.Value > s.RuleClock
                        || activity.EndedAt.Value < activity.StartedAt || receipt == null)
                        throw new ArgumentException("Invalid camp activity end source.");
                    var end = CommandHistory.Read(receipt);
                    if (!EndCommandMatches(activity, end.Kind)
                        || RequiresMemberEndActor(activity.EndReason) && end.Actor != s.ExpeditionPressureCohorts
                            .Single(c => c.Id == activity.CohortId).Members[0]
                        || !EndEvidenceExists(s, activity))
                        throw new ArgumentException("Camp activity end is not backed by its command receipt.");
                }
                if (activity.Kind == ExpeditionCampActivityKind.LyingLow)
                {
                    var parent = s.ExpeditionCampActivities.SingleOrDefault(x => x.Id == activity.ParentUseId
                        && x.Kind == ExpeditionCampActivityKind.Use && x.CohortId == activity.CohortId
                        && x.ExposureId == activity.ExposureId && x.CampId == activity.CampId);
                    if (parent == null || !site.Concealed || activity.StartedAt < parent.StartedAt
                        || parent.EndedAt.HasValue && (!activity.EndedAt.HasValue || activity.EndedAt.Value > parent.EndedAt.Value)
                        || !activity.EndedAt.HasValue && parent.EndedAt.HasValue)
                        throw new ArgumentException("Lying-low interval is not contained by physical camp use.");
                }
            }

            if (s.ExpeditionCampActivities.Where(x => x.Active).GroupBy(x => x.CohortId + "|" + (int)x.Kind,
                    StringComparer.Ordinal).Any(g => g.Count() > 1))
                throw new ArgumentException("Only one active camp interval per cohort and kind is supported.");

            foreach (var group in s.ExpeditionCampActivities.GroupBy(x => x.CohortId + "|" + (int)x.Kind,
                StringComparer.Ordinal))
            {
                var ordered = group.OrderBy(x => x.StartedAt).ThenBy(x => x.StartedRevision).ToArray();
                for (int i = 1; i < ordered.Length; i++)
                    if (!ordered[i - 1].EndedAt.HasValue || ordered[i - 1].EndedAt.Value > ordered[i].StartedAt)
                        throw new ArgumentException("Camp activity history contains overlapping intervals.");
            }

            foreach (var use in s.ExpeditionCampActivities.Where(x => x.Kind == ExpeditionCampActivityKind.Use && x.Active))
            {
                var member = s.ExpeditionPressureCohorts.Single(x => x.Id == use.CohortId).Members[0];
                var site = s.ExpeditionCampSites.Single(x => x.Id == use.CampId);
                var exposure = s.ExpeditionPressureExposures.Single(x => x.Id == use.ExposureId);
                var travel = s.RouteTravels.SingleOrDefault(x => x.RouteId == site.RouteId && x.TravelerId == member
                    && (x.Status == ExpeditionRouteTravelStatus.Moving || x.Status == ExpeditionRouteTravelStatus.Paused));
                var position = s.RouteTravelSpatial.SingleOrDefault(x => x.RouteId == site.RouteId
                    && x.TravelerId == member);
                var detached = s.RouteTravelSpatial.Any(x => x.RouteId == site.RouteId
                    && x.TravelerId == member && x.Detached);
                if (!site.SupportsUse || exposure.EndedAt.HasValue
                    || travel == null || travel.Status != ExpeditionRouteTravelStatus.Paused
                    || travel.Progress != site.RouteProgress || detached
                    || position != null && (position.X != new RuleQuantity(site.RouteX)
                        || position.Y != new RuleQuantity(site.RouteY))
                    || s.Actors.Single(x => x.Id == member).X != site.RouteX
                    || s.Actors.Single(x => x.Id == member).Y != site.RouteY
                    || s.WorldTraversals.Length != 0)
                    throw new ArgumentException("Active camp use requires paused route travel at its bound checkpoint.");
            }

            foreach (var low in s.ExpeditionCampActivities.Where(x => x.Kind == ExpeditionCampActivityKind.LyingLow && x.Active))
            {
                var member = s.ExpeditionPressureCohorts.Single(x => x.Id == low.CohortId).Members[0];
                if (s.InventoryCombat || s.MeleeAttacks.Any(x => x.At >= low.StartedAt
                        && (x.AttackerId == member || x.TargetId == member))
                    || s.RangedAttacks.Any(x => x.At >= low.StartedAt && (x.AttackerId == member || x.TargetId == member))
                    || s.Work.WorkerIntervals.Any(x => x.WorkerId == member && x.Start <= s.RuleClock && x.End > low.StartedAt)
                    || s.RestIntervals.Any(x => x.ActorId == member && x.StartedAt < s.RuleClock
                        && x.ScheduledEnd > low.StartedAt))
                    throw new ArgumentException("Lying-low activity overlaps incompatible combat or work.");
            }
        }

        public static bool EndCommandMatches(ExpeditionCampActivityRecord activity, CommandKind kind)
        {
            switch (activity.EndReason)
            {
                case ExpeditionCampActivityEndReason.Command:
                    return activity.Kind == ExpeditionCampActivityKind.Use ? kind == CommandKind.EndCampUse
                        : kind == CommandKind.EndLyingLow || kind == CommandKind.EndCampUse;
                case ExpeditionCampActivityEndReason.Combat:
                    return kind == CommandKind.BeginFixedEncounter || kind == CommandKind.EnterInventoryCombat;
                case ExpeditionCampActivityEndReason.Travel:
                    return kind == CommandKind.BeginWorldStep || kind == CommandKind.ResumeWorldStep
                        || kind == CommandKind.StartRouteTravel || kind == CommandKind.ResumeRouteTravel
                        || kind == CommandKind.TacticalStep || kind == CommandKind.TacticalRepositionStep;
                case ExpeditionCampActivityEndReason.Work:
                    return true;
                case ExpeditionCampActivityEndReason.PressureClosure:
                    return kind == CommandKind.AdvanceClock;
                default: return false;
            }
        }

        private static bool RequiresMemberEndActor(ExpeditionCampActivityEndReason reason)
            => reason == ExpeditionCampActivityEndReason.Command
                || reason == ExpeditionCampActivityEndReason.Travel;

        private static bool EndEvidenceExists(Snapshot s, ExpeditionCampActivityRecord activity)
        {
            var receipt = s.Receipts.SingleOrDefault(x => x.Id == activity.EndCommandId
                && x.Revision == activity.EndRevision);
            if (receipt == null || !activity.EndedAt.HasValue) return false;
            var command = CommandHistory.Read(receipt);
            string member = s.ExpeditionPressureCohorts.Single(x => x.Id == activity.CohortId).Members[0];
            switch (activity.EndReason)
            {
                case ExpeditionCampActivityEndReason.Command:
                    return command.Target == activity.CampId;
                case ExpeditionCampActivityEndReason.Combat:
                    return command.Kind == CommandKind.BeginFixedEncounter || command.Kind == CommandKind.EnterInventoryCombat;
                case ExpeditionCampActivityEndReason.Travel:
                    return command.Kind == CommandKind.BeginWorldStep || command.Kind == CommandKind.ResumeWorldStep
                        || command.Kind == CommandKind.StartRouteTravel || command.Kind == CommandKind.ResumeRouteTravel
                        || command.Kind == CommandKind.TacticalStep || command.Kind == CommandKind.TacticalRepositionStep;
                case ExpeditionCampActivityEndReason.Work:
                    return s.Work.WorkerIntervals.Any(x => x.WorkerId == member && x.Start == activity.EndedAt.Value
                        && x.End > x.Start);
                case ExpeditionCampActivityEndReason.PressureClosure:
                    var site = s.ExpeditionCampSites.Single(x => x.Id == activity.CampId);
                    return command.Kind == CommandKind.AdvanceClock && s.ExpeditionPressureCheckpoints.Any(x =>
                        x.CohortId == activity.CohortId && x.RouteId == site.RouteId
                        && x.At == activity.EndedAt.Value && x.CommandId == activity.EndCommandId
                        && x.AppliedRevision == activity.EndRevision
                        && x.Consequence == ExpeditionPressureConsequenceKind.RouteClosure);
                default: return false;
            }
        }

        internal static bool HasPositiveUseOverlap(ExpeditionCampActivityRecord activity, long watch, RuleTime through)
        {
            RuleTime watchStart = new RuleTime(checked(watch * ExpeditionPressureRules.WatchSeconds));
            RuleTime watchEnd = new RuleTime(checked((watch + 1) * ExpeditionPressureRules.WatchSeconds));
            RuleTime end = activity.EndedAt.HasValue && activity.EndedAt.Value < through ? activity.EndedAt.Value : through;
            if (end > watchEnd) end = watchEnd;
            RuleTime start = activity.StartedAt > watchStart ? activity.StartedAt : watchStart;
            return end > start;
        }

        public static bool CoversWatch(ExpeditionCampActivityRecord activity, long watch)
        {
            RuleTime watchStart = new RuleTime(checked(watch * ExpeditionPressureRules.WatchSeconds));
            RuleTime watchEnd = new RuleTime(checked((watch + 1) * ExpeditionPressureRules.WatchSeconds));
            return activity.StartedAt <= watchStart
                && (!activity.EndedAt.HasValue || activity.EndedAt.Value >= watchEnd);
        }

        internal static bool SourceExists(Snapshot s, ExpeditionPressureExposureRecord exposure,
            ExpeditionPressureChangeRecord change)
        {
            var activity = s.ExpeditionCampActivities.SingleOrDefault(x => x.Id == change.SourceId
                && x.CohortId == change.CohortId && x.ExposureId == change.ExposureId);
            var site = s.ExpeditionCampSites.SingleOrDefault(x => x.Id == activity?.CampId
                && x.CohortId == change.CohortId);
            if (activity == null || site == null || exposure == null || site.RouteId != change.RouteId
                || activity.StartedRevision != change.SourceRevision)
                return false;

            RuleTime watchStart = new RuleTime(checked(change.WatchIndex * ExpeditionPressureRules.WatchSeconds));
            RuleTime watchEnd = new RuleTime(checked((change.WatchIndex + 1) * ExpeditionPressureRules.WatchSeconds));
            if (change.Kind == ExpeditionPressureChangeKind.ExposedCampUse)
            {
                if (activity.Kind != ExpeditionCampActivityKind.Use || !site.Exposed && !site.KnownToEnemies)
                    return false;
                RuleTime start = activity.StartedAt > watchStart ? activity.StartedAt : watchStart;
                if (exposure.StartedAt > start) start = exposure.StartedAt;
                RuleTime end = activity.EndedAt.HasValue && activity.EndedAt.Value < watchEnd
                    ? activity.EndedAt.Value : watchEnd;
                if (exposure.EndedAt.HasValue && exposure.EndedAt.Value < end) end = exposure.EndedAt.Value;
                return change.At == start && end > start;
            }
            if (change.Kind != ExpeditionPressureChangeKind.FullWatchLyingLow
                || activity.Kind != ExpeditionCampActivityKind.LyingLow || !site.Concealed
                || change.At != watchEnd || !CoversWatch(activity, change.WatchIndex))
                return false;
            var parent = s.ExpeditionCampActivities.SingleOrDefault(x => x.Id == activity.ParentUseId
                && x.Kind == ExpeditionCampActivityKind.Use && x.CohortId == activity.CohortId
                && x.CampId == activity.CampId && x.ExposureId == activity.ExposureId);
            if (parent == null || !CoversWatch(parent, change.WatchIndex)
                || exposure.StartedAt > watchStart || exposure.EndedAt.HasValue && exposure.EndedAt.Value < watchEnd)
                return false;
            var member = s.ExpeditionPressureCohorts.Single(x => x.Id == change.CohortId).Members[0];
            if (s.Work.WorkerIntervals.Any(x => x.WorkerId == member && x.Start < watchEnd && x.End > watchStart)
                || s.RestIntervals.Any(x => x.ActorId == member && x.StartedAt < watchEnd && x.ScheduledEnd > watchStart)
                || s.MeleeAttacks.Any(x => x.At >= watchStart && x.At < watchEnd
                    && (x.AttackerId == member || x.TargetId == member))
                || s.RangedAttacks.Any(x => x.At >= watchStart && x.At < watchEnd
                    && (x.AttackerId == member || x.TargetId == member)))
                return false;
            return true;
        }
    }
}
