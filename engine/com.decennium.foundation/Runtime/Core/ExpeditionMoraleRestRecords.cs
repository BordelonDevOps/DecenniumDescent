using System;

namespace Decennium.Foundation
{
    public enum MoraleRestIntervalStatus { Active, Completed, Interrupted }

    /// <summary>An actual voluntary recreation interval on the shared RuleClock. Its site and
    /// activity are authorized by the TEST_ONLY host profile, not inferred from Long Rest facts.</summary>
    public sealed class ExpeditionMoraleRestIntervalRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string SiteId { get; }
        public string ActivityId { get; }
        public RuleTime StartedAt { get; }
        public RuleTime ScheduledEnd { get; }
        public RuleTime? EndedAt { get; }
        public MoraleRestIntervalStatus Status { get; }
        public string StartCommandId { get; }
        public long StartRevision { get; }
        public string EndCommandId { get; }
        public long EndRevision { get; }

        public ExpeditionMoraleRestIntervalRecord(string id, string actorId, string siteId, string activityId,
            RuleTime startedAt, RuleTime scheduledEnd, RuleTime? endedAt, MoraleRestIntervalStatus status,
            string startCommandId, long startRevision, string endCommandId = "", long endRevision = 0)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Validation.ValidId(siteId)
                || !Validation.ValidId(activityId) || !Validation.ValidId(startCommandId) || startRevision < 1
                || endCommandId == null || endCommandId != "" && !Validation.ValidId(endCommandId)
                || !Enum.IsDefined(typeof(MoraleRestIntervalStatus), status) || scheduledEnd <= startedAt
                || status == MoraleRestIntervalStatus.Active && (endedAt.HasValue || endCommandId != "" || endRevision != 0)
                || status != MoraleRestIntervalStatus.Active && (!endedAt.HasValue || endRevision < startRevision)
                || endedAt.HasValue && (endedAt.Value < startedAt || endedAt.Value > scheduledEnd))
                throw new ArgumentException("Invalid Morale Rest interval.");
            Id = id; ActorId = actorId; SiteId = siteId; ActivityId = activityId; StartedAt = startedAt;
            ScheduledEnd = scheduledEnd; EndedAt = endedAt; Status = status; StartCommandId = startCommandId;
            StartRevision = startRevision; EndCommandId = endCommandId; EndRevision = endRevision;
        }

        public ExpeditionMoraleRestIntervalRecord With(RuleTime? endedAt, MoraleRestIntervalStatus status,
            string endCommandId, long endRevision)
            => new ExpeditionMoraleRestIntervalRecord(Id, ActorId, SiteId, ActivityId, StartedAt, ScheduledEnd,
                endedAt, status, StartCommandId, StartRevision, endCommandId, endRevision);
    }

    /// <summary>One qualifying completed Morale interval that consumes this actor's independent
    /// 24-hour Morale allowance. The point offer is optional and never owns a second Strain ledger.</summary>
    public sealed class ExpeditionMoraleRestBenefitRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string IntervalId { get; }
        public string RecoveryOfferId { get; }
        public RuleTime CompletedAt { get; }
        public long Revision { get; }

        public ExpeditionMoraleRestBenefitRecord(string id, string actorId, string intervalId,
            string recoveryOfferId, RuleTime completedAt, long revision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Validation.ValidId(intervalId)
                || recoveryOfferId == null || recoveryOfferId != "" && !Validation.ValidId(recoveryOfferId)
                || revision < 1)
                throw new ArgumentException("Invalid Morale Rest benefit.");
            Id = id; ActorId = actorId; IntervalId = intervalId; RecoveryOfferId = recoveryOfferId;
            CompletedAt = completedAt; Revision = revision;
        }

        public ExpeditionMoraleRestBenefitRecord WithOffer(string recoveryOfferId, long revision)
            => new ExpeditionMoraleRestBenefitRecord(Id, ActorId, IntervalId, recoveryOfferId, CompletedAt, revision);
    }
}
