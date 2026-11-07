using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Player-selected helpers for one executable Map Route task.</summary>
    public sealed class RouteMappingWorkRequest
    {
        private readonly string[] assistantIds;
        public string[] AssistantIds => (string[])assistantIds.Clone();
        internal string Fingerprint => string.Join(",", assistantIds);

        public RouteMappingWorkRequest(System.Collections.Generic.IEnumerable<string> assistants)
        {
            if (assistants == null) throw new ArgumentNullException(nameof(assistants));
            assistantIds = assistants.ToArray();
            if (assistantIds.Length > 3 || assistantIds.Any(x => !Validation.ValidId(x))
                || assistantIds.Distinct(StringComparer.Ordinal).Count() != assistantIds.Length)
                throw new ArgumentException("Map Route allows at most three distinct assistants.");
            Array.Sort(assistantIds, StringComparer.Ordinal);
        }
    }

    public enum ExpeditionRouteMappingWorkStatus { Working = 1, Paused = 2, Resolved = 3, AwaitingCheck = 4 }

    /// <summary>Auditable result of the real task check that consumed the shared RNG stream.</summary>
    public sealed class ExpeditionRouteMappingWorkCheckRecord
    {
        public string CommandId { get; }
        public long AppliedRevision { get; }
        public RuleTime At { get; }
        public int LeadModifier { get; }
        public int ProficiencyRank { get; }
        public int ProficiencyBonus { get; }
        public int AssistantBonus { get; }
        public int Dc { get; }
        public int ConditionOperationCount { get; }
        public bool Disadvantage { get; }
        public int FirstRoll { get; }
        public int SecondRoll { get; }
        public int Natural { get; }
        public long Total { get; }
        public ExpeditionRouteMappingResultDegree Degree { get; }
        public uint RandomBefore { get; }
        public uint RandomAfter { get; }
        public long WordsConsumed { get; }
        public ExpeditionRouteMapping MappingBefore { get; }
        public ExpeditionRouteMapping MappingAfter { get; }
        public int MarksBefore { get; }
        public int MarksGranted { get; }
        public int MarksAfter { get; }

        public ExpeditionRouteMappingWorkCheckRecord(string commandId, long appliedRevision, RuleTime at,
            int leadModifier, int proficiencyRank, int proficiencyBonus, int assistantBonus, int dc,
            int conditionOperationCount, bool disadvantage, int firstRoll, int secondRoll, int natural, long total,
            ExpeditionRouteMappingResultDegree degree, uint randomBefore, uint randomAfter, long wordsConsumed, ExpeditionRouteMapping mappingBefore,
            ExpeditionRouteMapping mappingAfter, int marksBefore, int marksGranted, int marksAfter)
        {
            if (!Validation.ValidId(commandId) || appliedRevision < 1 || at < default(RuleTime)
                || proficiencyRank < 0 || proficiencyRank > 2 || proficiencyBonus < 0
                || assistantBonus < 0 || assistantBonus > 3 || dc < 1 || conditionOperationCount < 0
                || conditionOperationCount > ConditionJournal.MaxOperations || natural < 1 || natural > 20
                || firstRoll < 1 || firstRoll > 20 || (disadvantage
                    ? secondRoll < 1 || secondRoll > 20 || natural != Math.Min(firstRoll, secondRoll)
                    : secondRoll != 0 || natural != firstRoll)
                || total != (long)natural + leadModifier + assistantBonus
                || !Enum.IsDefined(typeof(ExpeditionRouteMappingResultDegree), degree)
                || randomBefore == 0 || randomAfter == 0 || wordsConsumed != (disadvantage ? 2 : 1)
                || !Enum.IsDefined(typeof(ExpeditionRouteMapping), mappingBefore)
                || !Enum.IsDefined(typeof(ExpeditionRouteMapping), mappingAfter)
                || marksBefore < 0 || marksGranted < 0 || marksGranted > 2 || marksAfter < 0)
                throw new ArgumentException("Invalid Map Route check evidence.");
            CommandId = commandId; AppliedRevision = appliedRevision; At = at; LeadModifier = leadModifier;
            ProficiencyRank = proficiencyRank; ProficiencyBonus = proficiencyBonus; AssistantBonus = assistantBonus;
            Dc = dc; ConditionOperationCount = conditionOperationCount; Disadvantage = disadvantage;
            FirstRoll = firstRoll; SecondRoll = secondRoll;
            Natural = natural; Total = total; Degree = degree; RandomBefore = randomBefore;
            RandomAfter = randomAfter; WordsConsumed = wordsConsumed; MappingBefore = mappingBefore;
            MappingAfter = mappingAfter; MarksBefore = marksBefore; MarksGranted = marksGranted; MarksAfter = marksAfter;
        }
    }

    /// <summary>Persistent state for one stationary Map Route task. Worker time is reserved in the
    /// shared WorkLedger; fully credited work may await a capable lead before its check is resolved.</summary>
    public sealed class ExpeditionRouteMappingWorkAttemptRecord
    {
        private readonly string[] assistantIds;
        public string Id { get; }
        public string RouteId { get; }
        public string LeadId { get; }
        public string[] AssistantIds => (string[])assistantIds.Clone();
        public long StartedRevision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime UpdatedAt { get; }
        public RuleTime WorkDone { get; }
        public RuleTime WorkRequired { get; }
        public ExpeditionRouteMappingWorkStatus Status { get; }
        public ExpeditionRouteMappingWorkCheckRecord Check { get; }

        public ExpeditionRouteMappingWorkAttemptRecord(string id, string routeId, string leadId,
            System.Collections.Generic.IEnumerable<string> assistants, long startedRevision, RuleTime startedAt,
            RuleTime updatedAt, RuleTime workDone, RuleTime workRequired,
            ExpeditionRouteMappingWorkStatus status, ExpeditionRouteMappingWorkCheckRecord check = null)
        {
            assistantIds = (assistants ?? throw new ArgumentNullException(nameof(assistants))).ToArray();
            if (!Validation.ValidId(id) || !Validation.ValidId(routeId) || !Validation.ValidId(leadId)
                || assistantIds.Length > 3 || assistantIds.Any(x => !Validation.ValidId(x) || x == leadId)
                || assistantIds.Distinct(StringComparer.Ordinal).Count() != assistantIds.Length
                || startedRevision < 1 || startedAt < default(RuleTime) || startedAt > updatedAt
                || workDone < default(RuleTime) || workRequired <= default(RuleTime)
                || workDone > workRequired || !Enum.IsDefined(typeof(ExpeditionRouteMappingWorkStatus), status)
                || (status == ExpeditionRouteMappingWorkStatus.Resolved) != (check != null)
                || (status == ExpeditionRouteMappingWorkStatus.Resolved || status == ExpeditionRouteMappingWorkStatus.AwaitingCheck)
                    && workDone != workRequired
                || status != ExpeditionRouteMappingWorkStatus.Resolved && status != ExpeditionRouteMappingWorkStatus.AwaitingCheck
                    && workDone >= workRequired)
                throw new ArgumentException("Invalid Map Route work attempt.");
            Array.Sort(assistantIds, StringComparer.Ordinal);
            Id = id; RouteId = routeId; LeadId = leadId; StartedRevision = startedRevision; StartedAt = startedAt;
            UpdatedAt = updatedAt; WorkDone = workDone; WorkRequired = workRequired; Status = status; Check = check;
        }

        public ExpeditionRouteMappingWorkAttemptRecord WithWork(RuleTime at, RuleTime workDone,
            ExpeditionRouteMappingWorkStatus status)
            => new ExpeditionRouteMappingWorkAttemptRecord(Id, RouteId, LeadId, assistantIds, StartedRevision,
                StartedAt, at, workDone, WorkRequired, status);

        public ExpeditionRouteMappingWorkAttemptRecord Resolve(RuleTime at, ExpeditionRouteMappingWorkCheckRecord check)
            => new ExpeditionRouteMappingWorkAttemptRecord(Id, RouteId, LeadId, assistantIds, StartedRevision,
                StartedAt, at, WorkRequired, WorkRequired, ExpeditionRouteMappingWorkStatus.Resolved, check);

        public ExpeditionRouteMappingWorkAttemptRecord AwaitCheck(RuleTime at)
            => new ExpeditionRouteMappingWorkAttemptRecord(Id, RouteId, LeadId, assistantIds, StartedRevision,
                StartedAt, at, WorkRequired, WorkRequired, ExpeditionRouteMappingWorkStatus.AwaitingCheck);
    }

    public static class ExpeditionRouteMappingWorkValidation
    {
        public const int MaxAttempts = 128;

        public static void Validate(Snapshot s)
        {
            if (s.RouteMappingWorkAttempts == null || s.RouteMappingWorkAttempts.Length > MaxAttempts
                || s.RouteMappingWorkAttempts.Any(x => x == null))
                throw new ArgumentException("Invalid Map Route work attempts.");
            if (s.SchemaVersion < Snapshot.RouteMappingWorkSchema)
            {
                if (s.RouteMappingWorkAttempts.Length != 0)
                    throw new ArgumentException("Map Route work requires schema59.");
                return;
            }
            if (!s.TestOnly || s.RouteMappingWorkAttempts.Select(x => x.Id).Distinct(StringComparer.Ordinal).Count()
                    != s.RouteMappingWorkAttempts.Length
                || s.RouteMappingWorkAttempts.Any(x => x.StartedRevision > s.Revision || x.UpdatedAt > s.RuleClock
                    || !s.Actors.Any(a => a.Id == x.LeadId)
                    || x.AssistantIds.Any(id => !s.Actors.Any(a => a.Id == id))
                    || x.Check != null && (x.Check.AppliedRevision > s.Revision || x.Check.AppliedRevision <= x.StartedRevision
                        || x.Check.At != x.UpdatedAt || !s.Receipts.Any(r => r.Revision == x.Check.AppliedRevision
                            && r.Id == x.Check.CommandId))))
                throw new ArgumentException("Invalid Map Route work references.");
            if (s.RouteMappingWorkAttempts.Where(x => x.Status != ExpeditionRouteMappingWorkStatus.Resolved)
                .GroupBy(x => x.RouteId, StringComparer.Ordinal).Any(g => g.Count() > 1))
                throw new ArgumentException("A route already has an open Map Route task.");
        }
    }
}
