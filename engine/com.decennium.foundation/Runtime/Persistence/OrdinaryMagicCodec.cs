using System;
using System.Collections.Generic;
using System.IO;

namespace Decennium.Foundation
{
    internal static class OrdinaryMagicCodec
    {
        internal static void Write(BinaryWriter w, MagicalActivityCalendarRecord record)
        {
            Text(w, record.PredecessorFingerprint); Text(w, OrdinaryMagicProfile.Approval); Text(w, OrdinaryMagicProfile.ContractHash);
            Text(w, OrdinaryMagicProfile.RepresentationApproval);
            w.Write(record.NextOrdinal); w.Write(record.Current != null);
            if (record.Current != null) {
                var x = record.Current;
                Origin(w, x.Origin); Time(w, x.OriginAt); Time(w, x.Deadline); Text(w, x.ContextEpoch);
                w.Write(x.InInitiative); w.Write(x.Consumed); w.Write(x.SegmentOrdinal);
            }
            Rows(w, record.Segments, x => {
                w.Write(x.Ordinal); Origin(w, x.Origin); Text(w, x.ContextEpoch); w.Write(x.InInitiative); w.Write(x.ConsumedAtOpen);
                Text(w, x.CauseId); w.Write(x.Revision); Time(w, x.At); w.Write(x.Closed);
                Text(w, x.CloseCauseId); w.Write(x.CloseRevision); Time(w, x.CloseAt);
            });
            Rows(w, record.Activities, x => {
                w.Write(x.Ordinal); Text(w, x.CommandId); w.Write(x.Revision); Time(w, x.At); Origin(w, x.Origin);
                w.Write(x.SegmentOrdinal); Text(w, x.ContextEpoch); w.Write(x.InInitiative); w.Write(x.ConsumedAtUse); w.Write((int)x.Kind);
            });
            Rows(w, record.Settlements, x => {
                w.Write(x.Ordinal); Origin(w, x.Origin); w.Write(x.SegmentOrdinal); Text(w, x.ContextEpoch);
                Text(w, x.CauseId); w.Write(x.Revision); Time(w, x.At); w.Write((int)x.Reason);
                w.Write(x.IdleEligible); w.Write(x.MagicalActivity); w.Write(x.Grounding); w.Write(x.Proficiency); w.Write(x.Before); w.Write(x.After);
            });
            Rows(w, record.ZeroIdleRanges, x => {
                w.Write(x.Ordinal); Text(w, x.EpochId); w.Write(x.FirstLocalStart); w.Write(x.LastLocalStart); w.Write(x.Count);
                Text(w, x.CauseId); w.Write(x.Revision); Time(w, x.Through);
            });
            Rows(w, record.Transitions, x => {
                w.Write(x.Ordinal); Text(w, x.CauseId); w.Write(x.Revision); Time(w, x.At); Origin(w, x.Origin);
                Text(w, x.FromEpoch); Text(w, x.ToEpoch); w.Write(x.FromInitiative); w.Write(x.ToInitiative); w.Write(x.Consumed);
                w.Write(x.AdmissionCarry != null);
                if (x.AdmissionCarry != null) {
                    var c = x.AdmissionCarry.Interval;
                    Text(w, c.ActorId); w.Write(c.LastStart); Quantity(w, c.MovementSpent); w.Write(c.ActionSpent);
                    w.Write(c.DashPaid); w.Write(c.ReactionAvailable); w.Write(c.Interactions); w.Write(x.AdmissionCarry.BonusActionAvailable);
                }
            });
        }
        internal static MagicalActivityCalendarRecord Read(BinaryReader r)
        {
            string predecessor = Text(r);
            if (Text(r) != OrdinaryMagicProfile.Approval || Text(r) != OrdinaryMagicProfile.ContractHash
                || Text(r) != OrdinaryMagicProfile.RepresentationApproval)
                throw new InvalidDataException("Unknown ordinary-magic policy binding.");
            long next = r.ReadInt64();
            MagicalAllowanceRecord current = null;
            if (Bool(r)) current = new MagicalAllowanceRecord(Origin(r), Time(r), Time(r), Text(r), Bool(r), Bool(r), r.ReadInt64());
            var segments = Rows(r, () => new MagicalSegmentRecord(r.ReadInt64(), Origin(r), Text(r), Bool(r), Bool(r),
                Text(r), r.ReadInt64(), Time(r), Bool(r), Text(r), r.ReadInt64(), Time(r)));
            var activities = Rows(r, () => new MagicalActivityContextRecord(r.ReadInt64(), Text(r), r.ReadInt64(), Time(r), Origin(r),
                r.ReadInt64(), Text(r), Bool(r), Bool(r), (CastingActivityKind)r.ReadInt32()));
            var settlements = Rows(r, () => new MagicalSettlementRecord(r.ReadInt64(), Origin(r), r.ReadInt64(), Text(r),
                Text(r), r.ReadInt64(), Time(r), (MagicalSettlementReason)r.ReadInt32(), Bool(r), Bool(r), Bool(r),
                r.ReadInt32(), r.ReadInt32(), r.ReadInt32()));
            var ranges = Rows(r, () => new MagicalZeroIdleRange(r.ReadInt64(), Text(r), r.ReadInt64(), r.ReadInt64(), r.ReadInt64(),
                Text(r), r.ReadInt64(), Time(r)));
            var transitions = Rows(r, () => {
                long ordinal = r.ReadInt64(); string cause = Text(r); long revision = r.ReadInt64(); var at = Time(r); var origin = Origin(r);
                string from = Text(r), to = Text(r); bool fromInitiative = Bool(r), toInitiative = Bool(r), consumed = Bool(r);
                ReinforcementCarry carried = null;
                if (Bool(r)) carried = new ReinforcementCarry(
                    new WorldIntervalRecord(Text(r), r.ReadInt64(), Quantity(r), Bool(r), Bool(r), Bool(r), r.ReadInt32()), Bool(r));
                return new MagicalTransitionRecord(ordinal, cause, revision, at, origin, from, to, fromInitiative, toInitiative, consumed, carried);
            });
            return new MagicalActivityCalendarRecord(predecessor, next, current, segments, activities, settlements, ranges, transitions);
        }
        private static void Rows<T>(BinaryWriter w, IReadOnlyList<T> rows, Action<T> write)
        {
            w.Write(rows.Count); foreach (var row in rows) write(row);
        }
        private static T[] Rows<T>(BinaryReader r, Func<T> read)
        {
            var rows = new T[SnapshotCodec.ReadCount(r, MagicalActivityCalendarRecord.MaxRows)];
            for (int i = 0; i < rows.Length; i++) rows[i] = read();
            return rows;
        }
        private static void Origin(BinaryWriter w, SpellTurnIdentity origin)
        {
            w.Write(origin != null);
            if (origin == null) return;
            Text(w, origin.ActorId); Text(w, origin.EpochId); w.Write(origin.LocalStart); w.Write(origin.GlobalStart);
        }
        private static SpellTurnIdentity Origin(BinaryReader r) => Bool(r) ? new SpellTurnIdentity(Text(r), Text(r), r.ReadInt64(), r.ReadInt64()) : null;
        private static bool Bool(BinaryReader r) => SnapshotCodec.ReadBool(r);
        private static void Text(BinaryWriter w, string value) => SnapshotCodec.WriteText(w, value);
        private static string Text(BinaryReader r) => SnapshotCodec.ReadText(r);
        private static void Time(BinaryWriter w, RuleTime value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void Quantity(BinaryWriter w, RuleQuantity value) { w.Write(value.Numerator); w.Write(value.Denominator); }
        private static RuleQuantity Quantity(BinaryReader r) => new RuleQuantity(r.ReadInt64(), r.ReadInt64());
    }
}
