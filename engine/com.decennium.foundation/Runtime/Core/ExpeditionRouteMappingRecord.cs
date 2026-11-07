using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Task degree supplied by a resolved route-mapping result. This representation
    /// belongs to Core and does not depend on the TEST_ONLY laboratory roll helpers.</summary>
    public enum ExpeditionRouteMappingResultDegree
    {
        CriticalFailure, Failure, Success, CriticalSuccess
    }

    /// <summary>One persisted, append-only route-knowledge result. The result profile and its
    /// TEST_ONLY synthetic evidence are validated by the laboratory host policy.</summary>
    public sealed class ExpeditionRouteMappingResultRecord
    {
        public string RouteId { get; }
        public string ResultId { get; }
        public string ActorId { get; }
        public string CommandId { get; }
        public string OperationId { get; }
        public string EvidenceId { get; }
        public string ResultProfileFingerprint { get; }
        public long AppliedRevision { get; }
        public RuleTime CompletedAt { get; }
        public ExpeditionRouteMappingResultDegree Degree { get; }
        public ExpeditionRouteMapping MappingBefore { get; }
        public ExpeditionRouteMapping MappingAfter { get; }
        public int MarksBefore { get; }
        public int MarksGranted { get; }
        public int MarksAfter { get; }
        public bool Synthetic { get; }

        public ExpeditionRouteMappingResultRecord(string routeId, string resultId, string actorId,
            string commandId, string operationId, string evidenceId, string resultProfileFingerprint,
            long appliedRevision, RuleTime completedAt, ExpeditionRouteMappingResultDegree degree,
            ExpeditionRouteMapping mappingBefore, ExpeditionRouteMapping mappingAfter,
            int marksBefore, int marksGranted, int marksAfter, bool synthetic)
        {
            if (!Validation.ValidId(routeId) || !Validation.ValidId(resultId) || !Validation.ValidId(actorId)
                || !Validation.ValidId(commandId) || !Validation.ValidId(operationId) || !Validation.ValidId(evidenceId)
                || !Validation.ValidId(resultProfileFingerprint) || appliedRevision < 1 || completedAt < default(RuleTime)
                || !Enum.IsDefined(typeof(ExpeditionRouteMappingResultDegree), degree)
                || !Enum.IsDefined(typeof(ExpeditionRouteMapping), mappingBefore)
                || !Enum.IsDefined(typeof(ExpeditionRouteMapping), mappingAfter)
                || marksBefore < 0 || marksGranted < 0 || marksGranted > 2 || marksAfter < 0 || !synthetic)
                throw new ArgumentException("Invalid expedition route-mapping result record.");
            RouteId = routeId; ResultId = resultId; ActorId = actorId; CommandId = commandId;
            OperationId = operationId; EvidenceId = evidenceId; ResultProfileFingerprint = resultProfileFingerprint;
            AppliedRevision = appliedRevision; CompletedAt = completedAt; Degree = degree;
            MappingBefore = mappingBefore; MappingAfter = mappingAfter; MarksBefore = marksBefore;
            MarksGranted = marksGranted; MarksAfter = marksAfter; Synthetic = synthetic;
        }
    }

    /// <summary>Current knowledge derived from a route's immutable initial Mapping and its
    /// append-only result history.</summary>
    public struct ExpeditionRouteMappingKnowledge
    {
        public ExpeditionRouteMapping Mapping { get; }
        public int UnspentMarks { get; }

        public ExpeditionRouteMappingKnowledge(ExpeditionRouteMapping mapping, int unspentMarks)
        {
            if (!Enum.IsDefined(typeof(ExpeditionRouteMapping), mapping) || unspentMarks < 0)
                throw new ArgumentException("Invalid route-mapping knowledge.");
            Mapping = mapping; UnspentMarks = unspentMarks;
        }
    }

    /// <summary>FL-10 Map Route result accounting. The one-level-per-distinct-success completion
    /// and carried surplus are delegated TEST_ONLY prototype policy, not source wording.</summary>
    public static class ExpeditionRouteMappingRules
    {
        public const int MaxResults = 128;
        public const string MapRouteOperationId = "EX58.FL10.MapRoute";

        public static int RequiredMarks(int recordedRisk)
        {
            if (recordedRisk < 0) throw new ArgumentOutOfRangeException(nameof(recordedRisk));
            return Math.Max(1, recordedRisk);
        }

        public static ExpeditionRouteMappingKnowledge Current(Snapshot snapshot, string routeId,
            ExpeditionRouteMapping initialMapping)
        {
            if (snapshot == null || !Validation.ValidId(routeId)
                || !Enum.IsDefined(typeof(ExpeditionRouteMapping), initialMapping))
                throw new ArgumentException("Invalid route-mapping query.");
            var latest = (snapshot.RouteMappingResults ?? Array.Empty<ExpeditionRouteMappingResultRecord>())
                .Where(x => x.RouteId == routeId).OrderBy(x => x.AppliedRevision).LastOrDefault();
            long latestRevision = latest?.AppliedRevision ?? 0;
            var work = snapshot.SchemaVersion >= Snapshot.RouteMappingWorkSchema
                ? (snapshot.RouteMappingWorkAttempts ?? Array.Empty<ExpeditionRouteMappingWorkAttemptRecord>())
                    .Where(x => x.RouteId == routeId && x.Check != null)
                    .OrderBy(x => x.Check.AppliedRevision).LastOrDefault()
                : null;
            if (work != null && work.Check.AppliedRevision > latestRevision)
                return new ExpeditionRouteMappingKnowledge(work.Check.MappingAfter, work.Check.MarksAfter);
            return latest == null ? new ExpeditionRouteMappingKnowledge(initialMapping, 0)
                : new ExpeditionRouteMappingKnowledge(latest.MappingAfter, latest.MarksAfter);
        }

        public static ExpeditionRouteMappingKnowledge Apply(ExpeditionRouteMappingKnowledge current,
            int recordedRisk, ExpeditionRouteMappingResultDegree degree, out int marksGranted)
        {
            if (recordedRisk < 0 || !Enum.IsDefined(typeof(ExpeditionRouteMappingResultDegree), degree))
                throw new ArgumentOutOfRangeException(nameof(recordedRisk));
            marksGranted = 0;
            if (current.Mapping == ExpeditionRouteMapping.Secured
                || degree == ExpeditionRouteMappingResultDegree.Failure
                || degree == ExpeditionRouteMappingResultDegree.CriticalFailure)
                return current;

            marksGranted = degree == ExpeditionRouteMappingResultDegree.CriticalSuccess ? 2 : 1;
            long accumulated = (long)current.UnspentMarks + marksGranted;
            int required = RequiredMarks(recordedRisk);
            if (accumulated < required)
                return new ExpeditionRouteMappingKnowledge(current.Mapping, (int)accumulated);

            // Delegated completion: one distinct successful result promotes one step only.
            // Surplus remains available to a later distinct successful result.
            return new ExpeditionRouteMappingKnowledge((ExpeditionRouteMapping)((int)current.Mapping + 1),
                (int)(accumulated - required));
        }
    }

    public static class ExpeditionRouteMappingValidation
    {
        public static void Validate(Snapshot snapshot)
        {
            if (snapshot.RouteMappingResults == null
                || snapshot.RouteMappingResults.Length > ExpeditionRouteMappingRules.MaxResults
                || snapshot.RouteMappingResults.Any(x => x == null))
                throw new ArgumentException("Invalid expedition route-mapping result records.");
            if (snapshot.SchemaVersion < Snapshot.RouteMappingSchema)
            {
                if (snapshot.RouteMappingResults.Length != 0)
                    throw new ArgumentException("Route-mapping results require schema54.");
                return;
            }
            if (snapshot.RouteMappingResults.Select(x => x.ResultId).Distinct(StringComparer.Ordinal).Count()
                    != snapshot.RouteMappingResults.Length
                || snapshot.RouteMappingResults.Select(x => x.AppliedRevision).Distinct().Count()
                    != snapshot.RouteMappingResults.Length
                || snapshot.RouteMappingResults.Any(x => x.AppliedRevision > snapshot.Revision
                    || x.MarksAfter > ExpeditionRouteMappingRules.MaxResults * 2))
                throw new ArgumentException("Invalid expedition route-mapping result references.");
        }
    }
}
