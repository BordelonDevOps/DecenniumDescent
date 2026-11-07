using System;
using System.Linq;
using System.Numerics;

namespace Decennium.Foundation
{
    /// <summary>Authored physical travel condition; independent from route knowledge and Risk.</summary>
    public enum ExpeditionRouteQuality { Secured, Known, Contested, Collapsed }
    /// <summary>Recorded knowledge of a route; it does not imply its physical condition.</summary>
    public enum ExpeditionRouteMapping { Unknown, Sketched, Mapped, Secured }
    public enum ExpeditionRouteTravelStatus { Moving, Paused, SegmentComplete }

    /// <summary>Exact shared travel-rate arithmetic. Speed is current otherwise-lawful walking
    /// Speed in feet per six-second round; route profiles supply the physical-quality fraction.</summary>
    public static class ExpeditionRouteTravelRules
    {
        public const long NominalSegmentSeconds = 480 * 60;

        public static RuleQuantity QualityFactor(ExpeditionRouteQuality quality)
        {
            switch (quality)
            {
                case ExpeditionRouteQuality.Secured: return new RuleQuantity(3, 4);
                case ExpeditionRouteQuality.Known: return new RuleQuantity(1);
                case ExpeditionRouteQuality.Contested: return new RuleQuantity(5, 4);
                case ExpeditionRouteQuality.Collapsed: return new RuleQuantity(3, 2);
                default: throw new ArgumentOutOfRangeException(nameof(quality));
            }
        }

        /// <summary>Source FL-10 base Progress for a completed segment. Unknown requires the
        /// separate, successful-reconnaissance path before ordinary travel is admitted.</summary>
        public static RuleQuantity BaseProgress(ExpeditionRouteMapping startingMapping)
        {
            switch (startingMapping)
            {
                case ExpeditionRouteMapping.Unknown: return default;
                case ExpeditionRouteMapping.Sketched: return new RuleQuantity(1);
                case ExpeditionRouteMapping.Mapped:
                case ExpeditionRouteMapping.Secured: return new RuleQuantity(2);
                default: throw new ArgumentOutOfRangeException(nameof(startingMapping));
            }
        }

        /// <summary>Earned nominal route-work seconds over an actual moving interval.</summary>
        public static RuleTime EarnedNominalEffort(RuleTime movingSeconds, long currentWalkingSpeed,
            ExpeditionRouteQuality quality)
        {
            if (currentWalkingSpeed < 0) throw new ArgumentOutOfRangeException(nameof(currentWalkingSpeed));
            if (currentWalkingSpeed == 0 || movingSeconds == default) return default;
            var factor = QualityFactor(quality);
            return RuleTime.FromFraction((BigInteger)movingSeconds.Numerator * currentWalkingSpeed * factor.Denominator,
                (BigInteger)movingSeconds.Denominator * 30 * factor.Numerator);
        }

        /// <summary>Actual moving seconds needed for an exact amount of nominal route work.</summary>
        public static RuleTime ActualMovingTime(RuleTime nominalEffort, long currentWalkingSpeed,
            ExpeditionRouteQuality quality)
        {
            if (currentWalkingSpeed <= 0) throw new ArgumentOutOfRangeException(nameof(currentWalkingSpeed));
            var factor = QualityFactor(quality);
            return RuleTime.FromFraction((BigInteger)nominalEffort.Numerator * 30 * factor.Numerator,
                (BigInteger)nominalEffort.Denominator * currentWalkingSpeed * factor.Denominator);
        }

        public static RuleQuantity ProgressAtEffort(RuleQuantity segmentStart, RuleQuantity segmentAward,
            RuleTime nominalEffort)
        {
            if (nominalEffort > new RuleTime(NominalSegmentSeconds)) throw new ArgumentOutOfRangeException(nameof(nominalEffort));
            var partial = RuleQuantity.FromFraction((BigInteger)segmentAward.Numerator * nominalEffort.Numerator,
                (BigInteger)segmentAward.Denominator * nominalEffort.Denominator * NominalSegmentSeconds);
            return segmentStart + partial;
        }

        public static RuleTime EffortAtProgress(RuleQuantity segmentStart, RuleQuantity segmentAward,
            RuleQuantity progress)
        {
            if (segmentAward == default || progress < segmentStart || progress > segmentStart + segmentAward)
                throw new ArgumentOutOfRangeException(nameof(progress));
            RuleQuantity distance = progress - segmentStart;
            return RuleTime.FromFraction((BigInteger)distance.Numerator * NominalSegmentSeconds * segmentAward.Denominator,
                (BigInteger)distance.Denominator * segmentAward.Numerator);
        }
    }

    /// <summary>Persisted state for one 480-nominal-minute travel segment. Route geometry and
    /// source-derived content are immutable, fingerprinted profile data; this record owns exact
    /// current Progress and effort across pauses, saves, pace changes and replay.</summary>
    public sealed class ExpeditionRouteTravelRecord
    {
        public string RouteId { get; }
        public string TravelerId { get; }
        public long StartedRevision { get; }
        public RuleQuantity SegmentStartProgress { get; }
        public RuleQuantity SegmentProgressAward { get; }
        public RuleQuantity Progress { get; }
        public RuleTime NominalEffort { get; }
        public ExpeditionRouteMapping StartingMapping { get; }
        public ExpeditionRouteTravelStatus Status { get; }

        public ExpeditionRouteTravelRecord(string routeId, string travelerId, long startedRevision,
            RuleQuantity segmentStartProgress, RuleQuantity segmentProgressAward, RuleQuantity progress,
            RuleTime nominalEffort, ExpeditionRouteMapping startingMapping, ExpeditionRouteTravelStatus status,
            bool reconnaissanceAuthorized = false)
        {
            if (!Validation.ValidId(routeId) || !Validation.ValidId(travelerId) || startedRevision < 1
                || segmentProgressAward == default || progress < segmentStartProgress
                || progress > segmentStartProgress + segmentProgressAward || nominalEffort > new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds)
                || !Enum.IsDefined(typeof(ExpeditionRouteMapping), startingMapping)
                || startingMapping == ExpeditionRouteMapping.Unknown && !reconnaissanceAuthorized
                || !Enum.IsDefined(typeof(ExpeditionRouteTravelStatus), status)
                || (status == ExpeditionRouteTravelStatus.SegmentComplete) != (nominalEffort == new RuleTime(ExpeditionRouteTravelRules.NominalSegmentSeconds))
                || ExpeditionRouteTravelRules.ProgressAtEffort(segmentStartProgress, segmentProgressAward, nominalEffort) != progress)
                throw new ArgumentException("Invalid expedition route travel record.");
            RouteId = routeId; TravelerId = travelerId; StartedRevision = startedRevision;
            SegmentStartProgress = segmentStartProgress; SegmentProgressAward = segmentProgressAward;
            Progress = progress; NominalEffort = nominalEffort; StartingMapping = startingMapping; Status = status;
        }

        public ExpeditionRouteTravelRecord With(RuleTime nominalEffort, ExpeditionRouteTravelStatus status)
            => new ExpeditionRouteTravelRecord(RouteId, TravelerId, StartedRevision, SegmentStartProgress,
                SegmentProgressAward, ExpeditionRouteTravelRules.ProgressAtEffort(SegmentStartProgress,
                    SegmentProgressAward, nominalEffort), nominalEffort, StartingMapping, status,
                StartingMapping == ExpeditionRouteMapping.Unknown);
    }

    public static class ExpeditionRouteTravelValidation
    {
        public const int MaxRecords = 128;
        public static void Validate(Snapshot s)
        {
            if (s.RouteTravels == null || s.RouteTravels.Length > MaxRecords || s.RouteTravels.Any(x => x == null))
                throw new ArgumentException("Invalid expedition route travel records.");
            if (s.SchemaVersion < Snapshot.ExpeditionRouteSchema)
            {
                if (s.RouteTravels.Length != 0) throw new ArgumentException("Expedition route travel requires schema52.");
                return;
            }
            if (s.RouteTravels.Select(x => x.StartedRevision).Distinct().Count() != s.RouteTravels.Length
                || s.RouteTravels.Any(x => !s.Actors.Any(a => a.Id == x.TravelerId)
                    || x.StartedRevision > s.Revision || x.Progress > x.SegmentStartProgress + x.SegmentProgressAward)
                || s.RouteTravels.Where(x => x.Status != ExpeditionRouteTravelStatus.SegmentComplete)
                    .GroupBy(x => x.TravelerId, StringComparer.Ordinal).Any(g => g.Count() > 1))
                throw new ArgumentException("Invalid expedition route travel references.");
        }
    }
}
