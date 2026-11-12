using System;
using System.Globalization;

namespace Decennium.Foundation
{
    public enum SurpriseAwareness { Warned, Surprised }

    public sealed class SurpriseAwarenessBinding
    {
        public const string RuleRevision = "46a4d52728ee6956f0bebcb5d2103ffd5bc67ba4";
        public const string Director = "TEST_ONLY.director.surprise-aware-entry.v1";
        public string SourceRevision { get; }
        public string DirectorId { get; }
        public string EncounterId { get; }
        public string ParticipantId { get; }
        public string ThreatId { get; }
        public string EvidenceId { get; }
        public SurpriseAwareness Outcome { get; }

        public static string EvidenceFor(SurpriseAwareness outcome)
        {
            switch (outcome) {
                case SurpriseAwareness.Warned: return "TEST_ONLY.hero-explicitly-warned-of-later-defender.v1";
                case SurpriseAwareness.Surprised: return "TEST_ONLY.hero-first-recognizes-later-threat-at-contact.v1";
                default: throw new ArgumentOutOfRangeException(nameof(outcome));
            }
        }

        public SurpriseAwarenessBinding(string source, string director, string encounter, string participant,
            string threat, string evidence, SurpriseAwareness outcome)
        {
            if (source != RuleRevision || director != Director || evidence != EvidenceFor(outcome)
                || !Validation.ValidId(encounter) || !Validation.ValidId(participant) || !Validation.ValidId(threat)
                || participant == threat)
                throw new ArgumentException("Invalid authored surprise authority or awareness evidence.");
            SourceRevision = source;
            DirectorId = director;
            EncounterId = encounter;
            ParticipantId = participant;
            ThreatId = threat;
            EvidenceId = evidence;
            Outcome = outcome;
        }

        public bool SameAs(SurpriseAwarenessBinding other) => other != null && SourceRevision == other.SourceRevision
            && DirectorId == other.DirectorId && EncounterId == other.EncounterId && ParticipantId == other.ParticipantId
            && ThreatId == other.ThreatId && EvidenceId == other.EvidenceId && Outcome == other.Outcome;
    }

    public sealed class SurpriseEntryDecision
    {
        public long Revision { get; }
        public string CommandId { get; }
        public RuleTime At { get; }

        public SurpriseEntryDecision(long revision, string commandId, RuleTime at)
        {
            if (revision < 1 || !Validation.ValidId(commandId)) throw new ArgumentException("Invalid surprise entry receipt.");
            Revision = revision;
            CommandId = commandId;
            At = at;
        }
    }

    public sealed class SurpriseFirstStart
    {
        public long Revision { get; }
        public int Ordinal { get; }
        public RuleTime At { get; }

        public SurpriseFirstStart(long revision, int ordinal, RuleTime at)
        {
            if (revision < 1 || ordinal < 0) throw new ArgumentException("Invalid surprise regular Start.");
            Revision = revision;
            Ordinal = ordinal;
            At = at;
        }

        public string TurnId(string encounterId) => encounterId + ".turn." + Ordinal.ToString(CultureInfo.InvariantCulture);
    }

    public sealed class SurpriseFirstEnd
    {
        public long EndRevision { get; }
        public string EndCommandId { get; }
        public long CompletedRevision { get; }
        public RuleTime At { get; }

        public SurpriseFirstEnd(long endRevision, string endCommandId, long completedRevision, RuleTime at)
        {
            if (endRevision < 1 || completedRevision < endRevision || !Validation.ValidId(endCommandId))
                throw new ArgumentException("Invalid surprise regular End.");
            EndRevision = endRevision;
            EndCommandId = endCommandId;
            CompletedRevision = completedRevision;
            At = at;
        }
    }

    /// <summary>The recorded Director decision and its actual slot markers. The interval owns resource availability.</summary>
    public sealed class SurpriseEntryRecord
    {
        public SurpriseAwarenessBinding Binding { get; }
        public SurpriseEntryDecision Decision { get; }
        public SurpriseFirstStart FirstStart { get; }
        public SurpriseFirstEnd FirstEnd { get; }
        public bool SurprisePending => Decision != null && Binding.Outcome == SurpriseAwareness.Surprised && FirstEnd == null;

        public SurpriseEntryRecord(SurpriseAwarenessBinding binding, SurpriseEntryDecision decision = null,
            SurpriseFirstStart start = null, SurpriseFirstEnd end = null)
        {
            Binding = binding ?? throw new ArgumentNullException(nameof(binding));
            if (start != null && (decision == null || start.Revision < decision.Revision || start.At < decision.At)
                || end != null && (start == null || end.EndRevision <= start.Revision || end.At <= start.At))
                throw new ArgumentException("Invalid surprise lifecycle ordering.");
            Decision = decision;
            FirstStart = start;
            FirstEnd = end;
        }

        public SurpriseEntryRecord Apply(SurpriseEntryDecision decision) => new SurpriseEntryRecord(Binding, decision);
        public SurpriseEntryRecord Start(SurpriseFirstStart start) => new SurpriseEntryRecord(Binding, Decision, start);
        public SurpriseEntryRecord Complete(SurpriseFirstEnd end) => new SurpriseEntryRecord(Binding, Decision, FirstStart, end);
    }
}
