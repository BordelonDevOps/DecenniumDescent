using System;
using System.Globalization;
using System.Linq;

namespace Decennium.Foundation
{
    public enum TemporaryHpEnd { None, Depleted, Expired, Replaced }

    /// <summary>Source and lifecycle evidence. ActorLife owns the remaining temporary HP.</summary>
    public sealed class ConsumeDecayRecord
    {
        public string CommandId { get; }
        public long Revision { get; }
        public RuleTime StartedAt { get; }
        public RuleTime Deadline => StartedAt.AddSeconds(3600);
        public int Offer { get; }
        public bool Accepted { get; }
        public TemporaryHpEnd End { get; }
        public RuleTime? EndedAt { get; }
        public long EndRevision { get; }
        public bool Active => Accepted && End == TemporaryHpEnd.None;

        public ConsumeDecayRecord(string commandId, long revision, RuleTime startedAt, int offer, bool accepted,
            TemporaryHpEnd end = TemporaryHpEnd.None, RuleTime? endedAt = null, long endRevision = 0)
        {
            if (!Validation.ValidId(commandId) || revision <= 0 || startedAt < default(RuleTime)
                || offer < 1 || offer > 20 || !Enum.IsDefined(typeof(TemporaryHpEnd), end)
                || (end == TemporaryHpEnd.None ? endedAt.HasValue || endRevision != 0
                    : !accepted || !endedAt.HasValue || endedAt < startedAt || endRevision <= revision)
                || (end == TemporaryHpEnd.Expired ? endedAt != startedAt.AddSeconds(3600)
                    : endedAt >= startedAt.AddSeconds(3600)))
                throw new ArgumentException("Invalid Consume Decay grant history.");
            CommandId = commandId;
            Revision = revision;
            StartedAt = startedAt;
            Offer = offer;
            Accepted = accepted;
            End = end;
            EndedAt = endedAt;
            EndRevision = endRevision;
        }

        internal static void Validate(Snapshot state)
        {
            bool selected = ConsumeDecaySite.SelectedFingerprint(state.ContentFingerprint);
            var grant = state.ConsumeDecay;
            if (selected != state.ConnectedConsumeDecay || !selected && grant != null)
                throw new ArgumentException("Invalid Consume Decay envelope.");
            if (!selected) return;
            if (!state.TestOnly || !state.ConnectedWoundTreatment || state.SchemaVersion != Snapshot.SurpriseEntrySchema)
                throw new ArgumentException("Consume Decay requires its selected connected profile.");
            string kind = ((int)CommandKind.ConsumeDecay).ToString(CultureInfo.InvariantCulture) + "|";
            var starts = state.Receipts.Where(x => x.Fingerprint.StartsWith(kind, StringComparison.Ordinal)).ToArray();
            var life = state.Lives.Single(x => x.ActorId == ConsumeDecaySite.Actor);
            if (grant == null) {
                if (starts.Length != 0 || life.TemporaryHp != 0) throw new ArgumentException("Unattributed temporary HP or spent use.");
                return;
            }
            var command = new Command(grant.CommandId, ConsumeDecaySite.Actor, grant.Revision - 1, CommandKind.ConsumeDecay, ConsumeDecaySite.Id);
            var fight = EncounterHistory.AtRevision(state, grant.Revision);
            int start = fight == null ? -1 : fight.StartRevisions.Count - 1;
            while (start >= 0 && fight.StartRevisions[start] >= grant.Revision) start--;
            if (starts.Length != 1 || starts[0].Principal != "TEST_ONLY.host" || !command.MatchesReceipt(starts[0])
                || fight?.Id != state.LaterEncounter?.Definition.EncounterId || start < 0
                || !EncounterHistory.MatchesTurn(fight, fight.ObservedOrdinals[start], ConsumeDecaySite.Actor)
                || grant.StartedAt != fight.StartAt(fight.ObservedOrdinals[start])
                || grant.Revision > state.Revision || grant.EndRevision > state.Revision || grant.EndedAt > state.RuleClock
                || grant.Active && (grant.Deadline <= state.RuleClock || life.TemporaryHp <= 0 || life.TemporaryHp > grant.Offer)
                || !grant.Active && life.TemporaryHp != 0
                || grant.EndRevision > 0 && !state.Receipts.Any(x => x.Revision == grant.EndRevision))
                throw new ArgumentException("Invalid receipt-bound Consume Decay grant or balance.");
        }
    }

    public static class ConsumeDecaySite
    {
        public const string FingerprintPrefix = "TEST_ONLY.consume-decay-v1-";
        public const string Id = "TEST_ONLY.consume-decay-bed";
        public const string Source = "decay-mycelian--consume-decay";
        public const string Actor = ConnectedVialRules.CarrierId;
        public const int X = 1;
        public const int Y = 3;
        public const byte Marker = 7;
        public static bool SelectedFingerprint(string fingerprint) => fingerprint.StartsWith(FingerprintPrefix, StringComparison.Ordinal)
            || ShortRestBerth.SelectedFingerprint(fingerprint);
    }
}
