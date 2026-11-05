using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class WorldActivityCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static void Text(BinaryWriter w, string value) { var bytes = Utf8.GetBytes(value); w.Write(bytes.Length); w.Write(bytes); }
        private static string Text(BinaryReader r)
        {
            int length = r.ReadInt32();
            if (length < 0 || length > 96) throw new InvalidDataException("Invalid activity identity length.");
            var bytes = r.ReadBytes(length);
            if (bytes.Length != length) throw new EndOfStreamException();
            return Utf8.GetString(bytes);
        }
        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.WorldActivityIntervals.Length);
            foreach (var activity in s.WorldActivityIntervals.OrderBy(x => x.ActorId, StringComparer.Ordinal))
            {
                Text(w, activity.CalendarId); Text(w, activity.ActorId); w.Write(activity.IntervalIndex);
                w.Write(activity.MovementSpent.Numerator); w.Write(activity.MovementSpent.Denominator);
                w.Write((int)activity.Action); Text(w, activity.ActionReference); w.Write(activity.ActionReferenceRevision);
            }
        }
        public static void Read(BinaryReader r, Snapshot s)
        {
            int count = r.ReadInt32();
            if (count < 0 || count > 64) throw new InvalidDataException("Invalid activity record count.");
            s.WorldActivityIntervals = new WorldActivityIntervalRecord[count];
            for (int i = 0; i < count; i++)
                s.WorldActivityIntervals[i] = new WorldActivityIntervalRecord(Text(r), Text(r), r.ReadInt64(),
                    new RuleQuantity(r.ReadInt64(), r.ReadInt64()), (WorldActionCommitment)r.ReadInt32(), Text(r), r.ReadInt64());
        }
    }
}
