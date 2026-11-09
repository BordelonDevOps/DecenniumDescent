using System;
using System.Linq;

namespace Decennium.Foundation
{
    public enum HavenCareIntervalStatus { Active, Completed, Interrupted }

    /// <summary>One patient's use of a qualified Haven-care service over the shared RuleClock.</summary>
    public sealed class ExpeditionHavenCareIntervalRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string ProviderId { get; }
        public string ServiceId { get; }
        public string SiteId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime ScheduledEnd { get; }
        public RuleTime? EndedAt { get; }
        public HavenCareIntervalStatus Status { get; }
        public string StartCommandId { get; }
        public long StartRevision { get; }
        public string EndCommandId { get; }
        public long EndCommandRevision { get; }
        public long EndRevision { get; }

        public ExpeditionHavenCareIntervalRecord(string id, string actorId, string providerId, string serviceId,
            string siteId, RuleTime startedAt, RuleTime scheduledEnd, RuleTime? endedAt,
            HavenCareIntervalStatus status, string startCommandId, long startRevision,
            string endCommandId = "", long endCommandRevision = 0, long endRevision = 0)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Validation.ValidId(providerId)
                || !Validation.ValidId(serviceId) || !Validation.ValidId(siteId)
                || !Validation.ValidId(startCommandId) || startRevision < 1
                || endCommandId == null || endCommandId != "" && !Validation.ValidId(endCommandId)
                || !Enum.IsDefined(typeof(HavenCareIntervalStatus), status) || scheduledEnd <= startedAt
                || status == HavenCareIntervalStatus.Active
                    && (endedAt.HasValue || endCommandId != "" || endCommandRevision != 0 || endRevision != 0)
                || status != HavenCareIntervalStatus.Active
                    && (!endedAt.HasValue || endCommandId == "" || endCommandRevision < startRevision
                        || endRevision < endCommandRevision)
                || endedAt.HasValue && (endedAt.Value < startedAt || endedAt.Value > scheduledEnd))
                throw new ArgumentException("Invalid Haven-care interval.");
            Id = id; ActorId = actorId; ProviderId = providerId; ServiceId = serviceId; SiteId = siteId;
            StartedAt = startedAt; ScheduledEnd = scheduledEnd; EndedAt = endedAt; Status = status;
            StartCommandId = startCommandId; StartRevision = startRevision;
            EndCommandId = endCommandId; EndCommandRevision = endCommandRevision; EndRevision = endRevision;
        }

        public ExpeditionHavenCareIntervalRecord With(RuleTime endedAt, HavenCareIntervalStatus status,
            string endCommandId, long endCommandRevision, long endRevision)
            => new ExpeditionHavenCareIntervalRecord(Id, ActorId, ProviderId, ServiceId, SiteId,
                StartedAt, ScheduledEnd, endedAt, status, StartCommandId, StartRevision,
                endCommandId, endCommandRevision, endRevision);
    }

    /// <summary>Auditable completion-time assessment. IntakeIds refer to existing consumed
    /// reservation history; they are evidence references, not a second consumption ledger.</summary>
    public sealed class ExpeditionHavenCareAssessmentRecord
    {
        private readonly string[] intakeIds;
        private readonly string[] eligiblePointIds;
        public string Id { get; }
        public string IntervalId { get; }
        public string ActorId { get; }
        public RuleTime CompletedAt { get; }
        public long Revision { get; }
        public RuleQuantity FoodConsumed { get; }
        public RuleQuantity WaterConsumed { get; }
        public bool SupportQualified { get; }
        public bool ProvisioningBlockActive { get; }
        public string[] IntakeIds => (string[])intakeIds.Clone();
        public string[] EligiblePointIds => (string[])eligiblePointIds.Clone();
        public bool RecoveryApplied => eligiblePointIds.Length != 0;

        public ExpeditionHavenCareAssessmentRecord(string id, string intervalId, string actorId,
            RuleTime completedAt, long revision, RuleQuantity foodConsumed, RuleQuantity waterConsumed,
            bool supportQualified, bool provisioningBlockActive, string[] intakeIds, string[] eligiblePointIds)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(intervalId) || !Validation.ValidId(actorId)
                || revision < 1 || foodConsumed < default(RuleQuantity) || waterConsumed < default(RuleQuantity)
                || intakeIds == null || eligiblePointIds == null)
                throw new ArgumentException("Invalid Haven-care completion assessment.");
            var intakes = intakeIds.ToArray();
            var points = eligiblePointIds.ToArray();
            if (intakes.Any(x => !Validation.ValidId(x))
                || intakes.Distinct(StringComparer.Ordinal).Count() != intakes.Length
                || !intakes.SequenceEqual(intakes.OrderBy(x => x, StringComparer.Ordinal))
                || points.Length > 6 || points.Any(x => !Validation.ValidId(x))
                || points.Distinct(StringComparer.Ordinal).Count() != points.Length
                || !points.SequenceEqual(points.OrderBy(x => x, StringComparer.Ordinal))
                || points.Length != 0 && (!supportQualified || provisioningBlockActive))
                throw new ArgumentException("Haven-care assessment evidence is not canonical.");
            Id = id; IntervalId = intervalId; ActorId = actorId; CompletedAt = completedAt; Revision = revision;
            FoodConsumed = foodConsumed; WaterConsumed = waterConsumed; SupportQualified = supportQualified;
            ProvisioningBlockActive = provisioningBlockActive; this.intakeIds = intakes; this.eligiblePointIds = points;
        }
    }
}
