using System;
using System.Collections.Generic;
using System.Linq;

namespace Decennium.Foundation
{
    public enum MagicalSettlementReason { RegularEnd, OutsideDeadline, ReplacementStartPartial }

    /// <summary>The real allowance follows its source Start across context changes. A null origin
    /// is only the explicitly recorded initial reinforcement carry, never a casting entitlement.</summary>
    public sealed class MagicalAllowanceRecord
    {
        public SpellTurnIdentity Origin { get; }
        public RuleTime OriginAt { get; }
        public RuleTime Deadline { get; }
        public string ContextEpoch { get; }
        public bool InInitiative { get; }
        public bool Consumed { get; }
        public long SegmentOrdinal { get; }
        public MagicalAllowanceRecord(SpellTurnIdentity origin, RuleTime originAt, RuleTime deadline,
            string contextEpoch, bool initiative, bool consumed, long segmentOrdinal)
        {
            if (origin != null && (origin.IsCarried || origin.ActorId != ClericRpProfile.Actor || deadline != originAt.AddSeconds(6))
                || origin == null && (originAt != default || deadline != default || !consumed)
                || !Validation.ValidId(contextEpoch) || segmentOrdinal < 1)
                throw new ArgumentException("Invalid magical allowance origin or accounting state.");
            Origin = origin; OriginAt = originAt; Deadline = deadline; ContextEpoch = contextEpoch;
            InInitiative = initiative; Consumed = consumed; SegmentOrdinal = segmentOrdinal;
        }
        public MagicalAllowanceRecord SetConsumed() => new MagicalAllowanceRecord(Origin, OriginAt, Deadline,
            ContextEpoch, InInitiative, true, SegmentOrdinal);
    }

    /// <summary>A context segment is not a new allowance. Empty intervening outside allowances
    /// can instead be represented by a qualified zero-idle range.</summary>
    public sealed class MagicalSegmentRecord
    {
        public long Ordinal { get; }
        public SpellTurnIdentity Origin { get; }
        public string ContextEpoch { get; }
        public bool InInitiative { get; }
        public bool ConsumedAtOpen { get; }
        public string CauseId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public bool Closed { get; }
        public string CloseCauseId { get; }
        public long CloseRevision { get; }
        public RuleTime CloseAt { get; }
        public MagicalSegmentRecord(long ordinal, SpellTurnIdentity origin, string epoch, bool initiative,
            bool consumed, string cause, long revision, RuleTime at, bool closed = false,
            string closeCause = "", long closeRevision = 0, RuleTime closeAt = default)
        {
            OrdinaryMagicProfile.RequireEvent(ordinal, cause, revision);
            if (!Validation.ValidId(epoch) || origin?.IsCarried == true || origin != null && origin.ActorId != ClericRpProfile.Actor
                || origin == null && !consumed || closed && (!Validation.ValidId(closeCause) || closeRevision < revision || closeAt < at)
                || !closed && (closeCause != "" || closeRevision != 0 || closeAt != default))
                throw new ArgumentException("Invalid magical activity segment.");
            Ordinal = ordinal; Origin = origin; ContextEpoch = epoch; InInitiative = initiative; ConsumedAtOpen = consumed;
            CauseId = cause; Revision = revision; At = at; Closed = closed;
            CloseCauseId = closeCause; CloseRevision = closeRevision; CloseAt = closeAt;
        }
        public MagicalSegmentRecord Close(string cause, long revision, RuleTime at)
        {
            if (Closed) throw new InvalidOperationException("Magical segment already closed.");
            return new MagicalSegmentRecord(Ordinal, Origin, ContextEpoch, InInitiative, ConsumedAtOpen,
                CauseId, Revision, At, true, cause, revision, at);
        }
    }

    public sealed class MagicalActivityContextRecord
    {
        public long Ordinal { get; }
        public string CommandId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public SpellTurnIdentity Origin { get; }
        public long SegmentOrdinal { get; }
        public string ContextEpoch { get; }
        public bool InInitiative { get; }
        public bool ConsumedAtUse { get; }
        public CastingActivityKind Kind { get; }
        public MagicalActivityContextRecord(long ordinal, string command, long revision, RuleTime at,
            SpellTurnIdentity origin, long segment, string epoch, bool initiative, bool consumed, CastingActivityKind kind)
        {
            OrdinaryMagicProfile.RequireEvent(ordinal, command, revision);
            OrdinaryMagicProfile.RequireOrigin(origin);
            if (segment < 1 || segment >= ordinal || !Validation.ValidId(epoch)
                || !Enum.IsDefined(typeof(CastingActivityKind), kind) || consumed && kind == CastingActivityKind.Grounding)
                throw new ArgumentException("Invalid paid magical activity context.");
            Ordinal = ordinal; CommandId = command; Revision = revision; At = at; Origin = origin;
            SegmentOrdinal = segment; ContextEpoch = epoch; InInitiative = initiative; ConsumedAtUse = consumed; Kind = kind;
        }
    }

    public sealed class MagicalSettlementRecord
    {
        public long Ordinal { get; }
        public SpellTurnIdentity Origin { get; }
        public long SegmentOrdinal { get; }
        public string ContextEpoch { get; }
        public string CauseId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public MagicalSettlementReason Reason { get; }
        public bool IdleEligible { get; }
        public bool MagicalActivity { get; }
        public bool Grounding { get; }
        public int Proficiency { get; }
        public int Before { get; }
        public int After { get; }
        public int Reduction => MagicalActivity ? 0 : Grounding ? Proficiency : IdleEligible ? 1 : 0;
        public MagicalSettlementRecord(long ordinal, SpellTurnIdentity origin, long segment, string epoch,
            string cause, long revision, RuleTime at, MagicalSettlementReason reason, bool idleEligible,
            bool magical, bool grounding, int proficiency, int before, int after)
        {
            OrdinaryMagicProfile.RequireEvent(ordinal, cause, revision);
            OrdinaryMagicProfile.RequireOrigin(origin);
            if (segment < 1 || segment >= ordinal || !Validation.ValidId(epoch) || !Enum.IsDefined(typeof(MagicalSettlementReason), reason)
                || idleEligible != (reason != MagicalSettlementReason.ReplacementStartPartial) || proficiency < 0 || before < 0
                || after != Math.Max(0, before - (magical ? 0 : grounding ? proficiency : idleEligible ? 1 : 0)))
                throw new ArgumentException("Invalid single magical settlement.");
            Ordinal = ordinal; Origin = origin; SegmentOrdinal = segment; ContextEpoch = epoch; CauseId = cause;
            Revision = revision; At = at; Reason = reason; IdleEligible = idleEligible; MagicalActivity = magical;
            Grounding = grounding; Proficiency = proficiency; Before = before; After = after;
        }
    }

    /// <summary>Only completed, empty, zero-Dissonance outside intervals. The final still-open
    /// allowance is never included. A skipped refresh splits or excludes the corresponding row.</summary>
    public sealed class MagicalZeroIdleRange
    {
        public long Ordinal { get; }
        public string EpochId { get; }
        public long FirstLocalStart { get; }
        public long LastLocalStart { get; }
        public long Count { get; }
        public string CauseId { get; }
        public long Revision { get; }
        public RuleTime Through { get; }
        public MagicalZeroIdleRange(long ordinal, string epoch, long first, long last, long count,
            string cause, long revision, RuleTime through)
        {
            OrdinaryMagicProfile.RequireEvent(ordinal, cause, revision);
            if (!Validation.ValidId(epoch) || first < 0 || last < first || count < 1)
                throw new ArgumentException("Invalid zero-idle coverage range.");
            Ordinal = ordinal; EpochId = epoch; FirstLocalStart = first; LastLocalStart = last; Count = count;
            CauseId = cause; Revision = revision; Through = through;
        }
    }

    public sealed class MagicalTransitionRecord
    {
        public long Ordinal { get; }
        public string CauseId { get; }
        public long Revision { get; }
        public RuleTime At { get; }
        public SpellTurnIdentity Origin { get; }
        public string FromEpoch { get; }
        public string ToEpoch { get; }
        public bool FromInitiative { get; }
        public bool ToInitiative { get; }
        public bool Consumed { get; }
        public ReinforcementCarry AdmissionCarry { get; }
        public MagicalTransitionRecord(long ordinal, string cause, long revision, RuleTime at,
            SpellTurnIdentity origin, string fromEpoch, string toEpoch, bool fromInitiative, bool toInitiative,
            bool consumed, ReinforcementCarry admissionCarry)
        {
            OrdinaryMagicProfile.RequireEvent(ordinal, cause, revision);
            if (origin?.IsCarried == true || origin != null && origin.ActorId != ClericRpProfile.Actor
                || fromEpoch == null || fromEpoch != "" && !Validation.ValidId(fromEpoch) || !Validation.ValidId(toEpoch)
                || (fromEpoch != toEpoch) != (admissionCarry != null)
                || admissionCarry != null && admissionCarry.Interval.ActorId != ClericRpProfile.Actor || origin == null && !consumed)
                throw new ArgumentException("Invalid magical allowance carry.");
            Ordinal = ordinal; CauseId = cause; Revision = revision; At = at; Origin = origin; FromEpoch = fromEpoch;
            ToEpoch = toEpoch; FromInitiative = fromInitiative; ToInitiative = toInitiative; Consumed = consumed;
            AdmissionCarry = admissionCarry;
        }
    }

    public sealed class MagicalActivityCalendarRecord
    {
        public const int MaxRows = 16384;
        public string PredecessorFingerprint { get; }
        public long NextOrdinal { get; }
        public MagicalAllowanceRecord Current { get; }
        public IReadOnlyList<MagicalSegmentRecord> Segments { get; }
        public IReadOnlyList<MagicalActivityContextRecord> Activities { get; }
        public IReadOnlyList<MagicalSettlementRecord> Settlements { get; }
        public IReadOnlyList<MagicalZeroIdleRange> ZeroIdleRanges { get; }
        public IReadOnlyList<MagicalTransitionRecord> Transitions { get; }
        public MagicalActivityCalendarRecord(string predecessor, long nextOrdinal = 1, MagicalAllowanceRecord current = null,
            IEnumerable<MagicalSegmentRecord> segments = null, IEnumerable<MagicalActivityContextRecord> activities = null,
            IEnumerable<MagicalSettlementRecord> settlements = null, IEnumerable<MagicalZeroIdleRange> zeroIdleRanges = null,
            IEnumerable<MagicalTransitionRecord> transitions = null)
        {
            if (!OrdinaryMagicProfile.IsPredecessor(predecessor) || nextOrdinal < 1)
                throw new ArgumentException("Invalid ordinary-magic declaration.");
            PredecessorFingerprint = predecessor; NextOrdinal = nextOrdinal; Current = current;
            Segments = Rows(segments); Activities = Rows(activities); Settlements = Rows(settlements);
            ZeroIdleRanges = Rows(zeroIdleRanges); Transitions = Rows(transitions);
        }
        private static IReadOnlyList<T> Rows<T>(IEnumerable<T> source) where T : class
        {
            var rows = (source ?? Array.Empty<T>()).Take(MaxRows + 1).ToArray();
            if (rows.Length > MaxRows || rows.Any(x => x == null)) throw new ArgumentException("Magical accounting history capacity exceeded.");
            return Array.AsReadOnly(rows);
        }
        public MagicalActivityCalendarRecord With(long nextOrdinal, MagicalAllowanceRecord current,
            IEnumerable<MagicalSegmentRecord> segments = null, IEnumerable<MagicalActivityContextRecord> activities = null,
            IEnumerable<MagicalSettlementRecord> settlements = null, IEnumerable<MagicalZeroIdleRange> ranges = null,
            IEnumerable<MagicalTransitionRecord> transitions = null)
            => new MagicalActivityCalendarRecord(PredecessorFingerprint, nextOrdinal, current, segments ?? Segments,
                activities ?? Activities, settlements ?? Settlements, ranges ?? ZeroIdleRanges, transitions ?? Transitions);
    }
}
