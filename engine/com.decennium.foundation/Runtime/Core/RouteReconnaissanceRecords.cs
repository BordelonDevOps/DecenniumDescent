using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum ExpeditionRouteSegmentStatus { ReconnaissanceRequired = 1, Feasible = 2, Traveling = 3, Complete = 4 }
    public enum ExpeditionRouteReconnaissanceStatus { Working = 1, Paused = 2, AwaitingCheck = 3, Resolved = 4 }
    public enum ExpeditionRouteReconnaissanceDegree { CriticalFailure = 1, Failure = 2, Success = 3, CriticalSuccess = 4 }

    /// <summary>TEST_ONLY singleton-cohort segment identity. Captures the route's knowledge and
    /// directed starting position before a reconnaissance attempt, then owns one feasibility proof
    /// and one subsequent travel settlement. Route travel remains the position/time authority.</summary>
    public sealed class ExpeditionRouteSegmentRecord
    {
        public string Id { get; }
        public string RouteId { get; }
        public string TravelerId { get; }
        public long StartedRevision { get; }
        public RuleQuantity StartingProgress { get; }
        public ExpeditionRouteMapping StartingMapping { get; }
        public string LatestAttemptId { get; }
        public string FeasibilityAttemptId { get; }
        public RuleQuantity ProgressAward { get; }
        public ExpeditionRouteSegmentStatus Status { get; }
        public long TravelStartedRevision { get; }
        public long TravelCompletedRevision { get; }
        public bool PressureReductionBlockedAtFloor { get; }

        public ExpeditionRouteSegmentRecord(string id, string routeId, string travelerId, long startedRevision,
            RuleQuantity startingProgress, ExpeditionRouteMapping startingMapping, string latestAttemptId,
            string feasibilityAttemptId, RuleQuantity progressAward, ExpeditionRouteSegmentStatus status,
            long travelStartedRevision, long travelCompletedRevision, bool pressureReductionBlockedAtFloor)
        {
            bool hasFeasibility = feasibilityAttemptId != "";
            if (!Validation.ValidId(id) || !Validation.ValidId(routeId) || !Validation.ValidId(travelerId)
                || startedRevision < 1 || startingProgress < default(RuleQuantity)
                || startingMapping != ExpeditionRouteMapping.Unknown || latestAttemptId == null
                || latestAttemptId != "" && !Validation.ValidId(latestAttemptId)
                || feasibilityAttemptId == null || hasFeasibility && !Validation.ValidId(feasibilityAttemptId)
                || !Enum.IsDefined(typeof(ExpeditionRouteSegmentStatus), status)
                || travelStartedRevision < 0 || travelCompletedRevision < 0
                || (status == ExpeditionRouteSegmentStatus.ReconnaissanceRequired) != !hasFeasibility
                || (status == ExpeditionRouteSegmentStatus.ReconnaissanceRequired) != (progressAward == default)
                || hasFeasibility && progressAward != new RuleQuantity(2)
                || (status == ExpeditionRouteSegmentStatus.Traveling || status == ExpeditionRouteSegmentStatus.Complete)
                    != (travelStartedRevision > 0)
                || (status == ExpeditionRouteSegmentStatus.Complete) != (travelCompletedRevision > 0)
                || status == ExpeditionRouteSegmentStatus.Traveling && travelCompletedRevision != 0
                || travelCompletedRevision > 0 && travelCompletedRevision < travelStartedRevision
                || pressureReductionBlockedAtFloor && !hasFeasibility)
                throw new ArgumentException("Invalid route segment settlement record.");
            Id = id; RouteId = routeId; TravelerId = travelerId; StartedRevision = startedRevision;
            StartingProgress = startingProgress; StartingMapping = startingMapping; LatestAttemptId = latestAttemptId;
            FeasibilityAttemptId = feasibilityAttemptId; ProgressAward = progressAward; Status = status;
            TravelStartedRevision = travelStartedRevision; TravelCompletedRevision = travelCompletedRevision;
            PressureReductionBlockedAtFloor = pressureReductionBlockedAtFloor;
        }

        public ExpeditionRouteSegmentRecord WithLatestAttempt(string attemptId)
            => new ExpeditionRouteSegmentRecord(Id, RouteId, TravelerId, StartedRevision, StartingProgress,
                StartingMapping, attemptId, FeasibilityAttemptId, ProgressAward, Status, TravelStartedRevision,
                TravelCompletedRevision, PressureReductionBlockedAtFloor);

        public ExpeditionRouteSegmentRecord MakeFeasible(string attemptId, bool criticalSuccess)
            => new ExpeditionRouteSegmentRecord(Id, RouteId, TravelerId, StartedRevision, StartingProgress,
                StartingMapping, attemptId, attemptId, new RuleQuantity(2), ExpeditionRouteSegmentStatus.Feasible,
                0, 0, criticalSuccess);

        public ExpeditionRouteSegmentRecord StartTravel(long revision)
        {
            if (Status != ExpeditionRouteSegmentStatus.Feasible || revision <= 0)
                throw new InvalidOperationException("Route segment is not available for travel.");
            return new ExpeditionRouteSegmentRecord(Id, RouteId, TravelerId, StartedRevision, StartingProgress,
                StartingMapping, LatestAttemptId, FeasibilityAttemptId, ProgressAward,
                ExpeditionRouteSegmentStatus.Traveling, revision, 0, PressureReductionBlockedAtFloor);
        }

        public ExpeditionRouteSegmentRecord CompleteTravel(long revision)
        {
            if (Status != ExpeditionRouteSegmentStatus.Traveling || revision < TravelStartedRevision)
                throw new InvalidOperationException("Route segment travel completion is invalid.");
            return new ExpeditionRouteSegmentRecord(Id, RouteId, TravelerId, StartedRevision, StartingProgress,
                StartingMapping, LatestAttemptId, FeasibilityAttemptId, ProgressAward,
                ExpeditionRouteSegmentStatus.Complete, TravelStartedRevision, revision, PressureReductionBlockedAtFloor);
        }
    }

    /// <summary>One lead's active reconnaissance work and check against a single captured route segment.</summary>
    public sealed class ExpeditionRouteReconnaissanceCheckRecord
    {
        public string CommandId { get; }
        public long AppliedRevision { get; }
        public RuleTime At { get; }
        public int LeadModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int Dc { get; }
        public int ConditionOperationCount { get; }
        public bool Disadvantage { get; }
        public int FirstRoll { get; }
        public int SecondRoll { get; }
        public int Natural { get; }
        public long Total { get; }
        public ExpeditionRouteReconnaissanceDegree Degree { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }

        public ExpeditionRouteReconnaissanceCheckRecord(string commandId, long appliedRevision, RuleTime at,
            int leadModifier, int proficiencyRank, int proficiencyBonus, int dc, int conditionOperationCount,
            bool disadvantage, int firstRoll, int secondRoll, int natural, long total,
            ExpeditionRouteReconnaissanceDegree degree, uint randomBefore, uint randomAfter, long wordsConsumed)
        {
            if (!Validation.ValidId(commandId) || appliedRevision < 1 || at < default(RuleTime)
                || proficiencyRank < 0 || proficiencyRank > 2 || proficiencyBonus < 0 || dc < 1
                || conditionOperationCount < 0 || conditionOperationCount > ConditionJournal.MaxOperations
                || firstRoll < 1 || firstRoll > 20 || (disadvantage
                    ? secondRoll < 1 || secondRoll > 20 || natural != Math.Min(firstRoll, secondRoll)
                    : secondRoll != 0 || natural != firstRoll)
                || total != (long)natural + leadModifier || !Enum.IsDefined(typeof(ExpeditionRouteReconnaissanceDegree), degree)
                || randomBefore == 0 || randomAfter == 0 || wordsConsumed != (disadvantage ? 2 : 1))
                throw new ArgumentException("Invalid reconnaissance check evidence.");
            CommandId = commandId; AppliedRevision = appliedRevision; At = at; LeadModifier = leadModifier;
            ProficiencyRank = proficiencyRank; ProficiencyBonus = proficiencyBonus; Dc = dc;
            ConditionOperationCount = conditionOperationCount; Disadvantage = disadvantage;
            FirstRoll = firstRoll; SecondRoll = secondRoll; Natural = natural; Total = total; Degree = degree;
            RandomBefore = randomBefore; RandomAfter = randomAfter; WordsConsumed = wordsConsumed;
        }
    }

    /// <summary>Immutable attempt history. Failed work is retained; a retry creates a new attempt
    /// against the same segment and must reserve a fresh full duration.</summary>
    public sealed class ExpeditionRouteReconnaissanceAttemptRecord
    {
        public string Id { get; }
        public string SegmentId { get; }
        public string RouteId { get; }
        public string LeadId { get; }
        public string InspectionProfileId { get; }
        public string InspectionProfileFingerprint { get; }
        public long StartedRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime WorkDone { get; }
        public RuleTime WorkRequired { get; }
        public ExpeditionRouteReconnaissanceStatus Status { get; }
        public ExpeditionRouteReconnaissanceCheckRecord Check { get; }

        public ExpeditionRouteReconnaissanceAttemptRecord(string id, string segmentId, string routeId, string leadId,
            string inspectionProfileId, string inspectionProfileFingerprint,
            long startedRevision, RuleTime startedAt, RuleTime updatedAt, RuleTime workDone,
            RuleTime workRequired, ExpeditionRouteReconnaissanceStatus status,
            ExpeditionRouteReconnaissanceCheckRecord check = null)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(segmentId) || !Validation.ValidId(routeId)
                || !Validation.ValidId(leadId) || !Validation.ValidId(inspectionProfileId)
                || !Validation.ValidId(inspectionProfileFingerprint) || startedRevision < 1 || startedAt < default(RuleTime)
                || startedAt > updatedAt || workDone < default(RuleTime) || workRequired <= default(RuleTime)
                || workDone > workRequired || !Enum.IsDefined(typeof(ExpeditionRouteReconnaissanceStatus), status)
                || (status == ExpeditionRouteReconnaissanceStatus.Resolved) != (check != null)
                || (status == ExpeditionRouteReconnaissanceStatus.Resolved || status == ExpeditionRouteReconnaissanceStatus.AwaitingCheck)
                    && workDone != workRequired
                || status != ExpeditionRouteReconnaissanceStatus.Resolved && status != ExpeditionRouteReconnaissanceStatus.AwaitingCheck
                    && workDone >= workRequired)
                throw new ArgumentException("Invalid reconnaissance attempt record.");
            Id = id; SegmentId = segmentId; RouteId = routeId; LeadId = leadId; StartedRevision = startedRevision;
            InspectionProfileId = inspectionProfileId; InspectionProfileFingerprint = inspectionProfileFingerprint;
            StartedAt = startedAt; UpdatedAt = updatedAt; WorkDone = workDone; WorkRequired = workRequired;
            Status = status; Check = check;
        }

        public ExpeditionRouteReconnaissanceAttemptRecord WithWork(RuleTime at, RuleTime workDone,
            ExpeditionRouteReconnaissanceStatus status)
            => new ExpeditionRouteReconnaissanceAttemptRecord(Id, SegmentId, RouteId, LeadId,
                InspectionProfileId, InspectionProfileFingerprint, StartedRevision,
                StartedAt, at, workDone, WorkRequired, status);

        public ExpeditionRouteReconnaissanceAttemptRecord AwaitCheck(RuleTime at)
            => new ExpeditionRouteReconnaissanceAttemptRecord(Id, SegmentId, RouteId, LeadId,
                InspectionProfileId, InspectionProfileFingerprint, StartedRevision,
                StartedAt, at, WorkRequired, WorkRequired, ExpeditionRouteReconnaissanceStatus.AwaitingCheck);

        public ExpeditionRouteReconnaissanceAttemptRecord Resolve(RuleTime at, ExpeditionRouteReconnaissanceCheckRecord check)
            => new ExpeditionRouteReconnaissanceAttemptRecord(Id, SegmentId, RouteId, LeadId,
                InspectionProfileId, InspectionProfileFingerprint, StartedRevision,
                StartedAt, at, WorkRequired, WorkRequired, ExpeditionRouteReconnaissanceStatus.Resolved, check);
    }

    public static class ExpeditionRouteReconnaissanceValidation
    {
        public const int MaxSegments = 128;
        public const int MaxAttempts = 256;

        public static void Validate(Snapshot s)
        {
            if (s.RouteSegments == null || s.RouteSegments.Length > MaxSegments || s.RouteSegments.Any(x => x == null)
                || s.RouteReconnaissanceAttempts == null || s.RouteReconnaissanceAttempts.Length > MaxAttempts
                || s.RouteReconnaissanceAttempts.Any(x => x == null))
                throw new ArgumentException("Invalid route reconnaissance records.");
            if (s.SchemaVersion < Snapshot.RouteReconnaissanceSchema)
            {
                if (s.RouteSegments.Length != 0 || s.RouteReconnaissanceAttempts.Length != 0)
                    throw new ArgumentException("Route reconnaissance requires schema60.");
                return;
            }
            if (!s.TestOnly || s.RouteSegments.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.RouteSegments.Length
                || s.RouteReconnaissanceAttempts.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count() != s.RouteReconnaissanceAttempts.Length
                || s.RouteSegments.Select(x => x.StartedRevision).Distinct().Count() != s.RouteSegments.Length
                || s.RouteSegments.Any(x => x.StartedRevision > s.Revision || !s.Actors.Any(a => a.Id == x.TravelerId)
                    || !s.RouteReconnaissanceAttempts.Any(a => a.Id == x.LatestAttemptId && a.SegmentId == x.Id)
                    || x.Status == ExpeditionRouteSegmentStatus.Feasible && x.TravelStartedRevision != 0
                    || (x.Status == ExpeditionRouteSegmentStatus.Traveling || x.Status == ExpeditionRouteSegmentStatus.Complete)
                        && !s.RouteTravels.Any(t => t.StartedRevision == x.TravelStartedRevision && t.RouteId == x.RouteId
                            && t.TravelerId == x.TravelerId && t.SegmentStartProgress == x.StartingProgress
                            && t.StartingMapping == x.StartingMapping && t.SegmentProgressAward == x.ProgressAward)
                    || x.Status == ExpeditionRouteSegmentStatus.Complete
                        && s.RouteTravels.Single(t => t.StartedRevision == x.TravelStartedRevision).Status != ExpeditionRouteTravelStatus.SegmentComplete
                    || x.Status == ExpeditionRouteSegmentStatus.Traveling
                        && s.RouteTravels.Single(t => t.StartedRevision == x.TravelStartedRevision).Status == ExpeditionRouteTravelStatus.SegmentComplete)
                || s.RouteReconnaissanceAttempts.Any(x => x.StartedRevision > s.Revision || x.UpdatedAt > s.RuleClock
                    || !s.RouteSegments.Any(g => g.Id == x.SegmentId && g.RouteId == x.RouteId && g.TravelerId == x.LeadId)
                    || x.Check != null && (x.Check.AppliedRevision > s.Revision || x.Check.AppliedRevision <= x.StartedRevision
                        || x.Check.At != x.UpdatedAt || !s.Receipts.Any(r => r.Revision == x.Check.AppliedRevision
                            && r.Id == x.Check.CommandId))))
                throw new ArgumentException("Invalid route reconnaissance references.");
            if (s.RouteSegments.Any(g => !s.RouteReconnaissanceAttempts.Any(a => a.Id == g.LatestAttemptId
                    && a.SegmentId == g.Id && a.StartedRevision == s.RouteReconnaissanceAttempts
                        .Where(x => x.SegmentId == g.Id).Max(x => x.StartedRevision))
                || (g.Status == ExpeditionRouteSegmentStatus.Feasible || g.Status == ExpeditionRouteSegmentStatus.Traveling
                    || g.Status == ExpeditionRouteSegmentStatus.Complete)
                    && !s.RouteReconnaissanceAttempts.Any(a => a.Id == g.FeasibilityAttemptId && a.SegmentId == g.Id
                        && a.Status == ExpeditionRouteReconnaissanceStatus.Resolved && a.Check != null
                        && (a.Check.Degree == ExpeditionRouteReconnaissanceDegree.Success
                            || a.Check.Degree == ExpeditionRouteReconnaissanceDegree.CriticalSuccess))))
                throw new ArgumentException("Route segment feasibility lacks its successful attempt.");
            if (s.RouteSegments.Any(g => g.Status != ExpeditionRouteSegmentStatus.ReconnaissanceRequired
                    && g.PressureReductionBlockedAtFloor != (s.RouteReconnaissanceAttempts.Single(a => a.Id == g.FeasibilityAttemptId)
                        .Check.Degree == ExpeditionRouteReconnaissanceDegree.CriticalSuccess)))
                throw new ArgumentException("Route segment critical benefit accounting is invalid.");
            if (s.RouteSegments.GroupBy(x => x.RouteId + "|" + x.StartingProgress, StringComparer.Ordinal)
                .Any(g => g.Count() > 1))
                throw new ArgumentException("Route segment identity is duplicated for one directed position and singleton cohort.");
            if (s.RouteReconnaissanceAttempts.Where(x => x.Status != ExpeditionRouteReconnaissanceStatus.Resolved)
                .GroupBy(x => x.SegmentId, StringComparer.Ordinal).Any(g => g.Count() > 1))
                throw new ArgumentException("A route segment has more than one open reconnaissance attempt.");
        }
    }
}
