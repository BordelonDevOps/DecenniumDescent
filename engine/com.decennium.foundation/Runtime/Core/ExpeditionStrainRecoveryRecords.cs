using System;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Append-only point metadata update supported by a later complete daily provisioning
    /// settlement. The original gain record remains unchanged for source history.</summary>
    public sealed class ExpeditionStrainRecoveryGateUpdateRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string PointId { get; }
        public string SettlementId { get; }
        public RuleTime At { get; }
        public long Revision { get; }

        public ExpeditionStrainRecoveryGateUpdateRecord(string id, string actorId, string pointId,
            string settlementId, RuleTime at, long revision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Validation.ValidId(pointId)
                || !Validation.ValidId(settlementId) || revision < 1)
                throw new ArgumentException("Invalid Expedition Strain recovery gate update.");
            Id = id; ActorId = actorId; PointId = pointId; SettlementId = settlementId; At = at; Revision = revision;
        }
    }

    /// <summary>One completed, beneficial secure Long Rest. A recovery offer is optional when the
    /// source's 24-hour limit applies or a separate removal gate prevents point reduction.</summary>
    public sealed class ExpeditionBeneficialRestRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string RecoveryOfferId { get; }
        public string RestIntervalId { get; }
        public RuleTime CompletedAt { get; }
        public long Revision { get; }

        public ExpeditionBeneficialRestRecord(string id, string actorId, string recoveryOfferId,
            string restIntervalId, RuleTime completedAt, long revision)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || recoveryOfferId == null
                || recoveryOfferId != "" && !Validation.ValidId(recoveryOfferId)
                || !Validation.ValidId(restIntervalId) || revision < 1)
                throw new ArgumentException("Invalid beneficial Long Rest record.");
            Id = id; ActorId = actorId; RecoveryOfferId = recoveryOfferId; RestIntervalId = restIntervalId;
            CompletedAt = completedAt; Revision = revision;
        }
    }

    /// <summary>Persisted patient choice opened only after the shared clock has completed a secure
    /// Rest and every mandatory boundary effect has been settled.</summary>
    public sealed class ExpeditionStrainRecoveryOfferRecord
    {
        private readonly string[] pointIds;
        public string Id { get; }
        public string ActorId { get; }
        public string RestIntervalId { get; }
        public string InitiatingCommandId { get; }
        public RuleTime CompletedAt { get; }
        public long Revision { get; }
        public string[] PointIds => (string[])pointIds.Clone();
        public string ChosenPointId { get; }
        public long ResolvedRevision { get; }
        public bool Pending => ChosenPointId == "";

        public ExpeditionStrainRecoveryOfferRecord(string id, string actorId, string restIntervalId,
            string initiatingCommandId, RuleTime completedAt, long revision, string[] pointIds,
            string chosenPointId = "", long resolvedRevision = 0)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Validation.ValidId(restIntervalId)
                || !Validation.ValidId(initiatingCommandId) || revision < 1 || pointIds == null
                || chosenPointId == null || chosenPointId != "" && !Validation.ValidId(chosenPointId)
                || chosenPointId == "" && resolvedRevision != 0
                || chosenPointId != "" && resolvedRevision <= revision)
                throw new ArgumentException("Invalid Expedition Strain recovery offer.");
            var selected = pointIds.ToArray();
            if (selected.Length == 0 || selected.Length > 6 || selected.Any(x => !Validation.ValidId(x))
                || selected.Distinct(StringComparer.Ordinal).Count() != selected.Length
                || !selected.SequenceEqual(selected.OrderBy(x => x, StringComparer.Ordinal))
                || chosenPointId != "" && !selected.Contains(chosenPointId, StringComparer.Ordinal))
                throw new ArgumentException("Recovery offer requires a canonical non-empty point list.");
            Id = id; ActorId = actorId; RestIntervalId = restIntervalId; InitiatingCommandId = initiatingCommandId;
            CompletedAt = completedAt; Revision = revision; this.pointIds = selected;
            ChosenPointId = chosenPointId; ResolvedRevision = resolvedRevision;
        }
    }

    /// <summary>One active Expedition Strain point removed by a selected beneficial Long Rest.
    /// Its sequence shares the actor's Strain event order with gains.</summary>
    public sealed class ExpeditionStrainRemovalRecord
    {
        public string Id { get; }
        public string ActorId { get; }
        public string PointId { get; }
        public string GainId { get; }
        public string BeneficialRestId { get; }
        public RuleTime At { get; }
        public long Revision { get; }
        public int MutationSequence { get; }

        public ExpeditionStrainRemovalRecord(string id, string actorId, string pointId, string gainId,
            string beneficialRestId, RuleTime at, long revision, int mutationSequence)
        {
            if (!Validation.ValidId(id) || !Validation.ValidId(actorId) || !Validation.ValidId(pointId)
                || !Validation.ValidId(gainId) || !Validation.ValidId(beneficialRestId)
                || revision < 1 || mutationSequence < 0)
                throw new ArgumentException("Invalid Expedition Strain point removal.");
            Id = id; ActorId = actorId; PointId = pointId; GainId = gainId; BeneficialRestId = beneficialRestId;
            At = at; Revision = revision; MutationSequence = mutationSequence;
        }
    }
}
