using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class WorldScheduleCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static void Text(BinaryWriter w, string value) { var b = Utf8.GetBytes(value); w.Write(b.Length); w.Write(b); }
        private static int Count(BinaryReader r, int max) { int n = r.ReadInt32(); if (n < 0 || n > max) throw new InvalidDataException("Invalid world count."); return n; }
        private static string Text(BinaryReader r) { int n = Count(r, 96); var b = r.ReadBytes(n); if (b.Length != n) throw new EndOfStreamException(); return Utf8.GetString(b); }
        private static bool Bool(BinaryReader r) { byte n = r.ReadByte(); if (n > 1) throw new InvalidDataException("Invalid world boolean."); return n == 1; }
        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.WorldSchedule != null); if (s.WorldSchedule == null) return;
            var calendar = s.WorldSchedule; Text(w, calendar.Id); w.Write(calendar.Origin.Numerator); w.Write(calendar.Origin.Denominator); w.Write(calendar.ProcessedSlot);
            w.Write(calendar.Order.Count); foreach (string actor in calendar.Order) Text(w, actor);
            w.Write(s.WorldIntervals.Length);
            foreach (var a in s.WorldIntervals.OrderBy(x => x.ActorId, StringComparer.Ordinal)) {
                Text(w, a.ActorId); w.Write(a.LastStart); w.Write(a.MovementSpent.Numerator); w.Write(a.MovementSpent.Denominator);
                w.Write(a.ActionSpent); w.Write(a.DashPaid); w.Write(a.ReactionAvailable); w.Write(a.Interactions);
            }
            w.Write(s.WorldTraversals.Length);
            foreach (var a in s.WorldTraversals.OrderBy(x => x.ActorId, StringComparer.Ordinal)) {
                Text(w, a.ActorId); w.Write(a.StartedRevision); w.Write(a.FromX); w.Write(a.FromY); w.Write(a.ToX); w.Write(a.ToY);
                w.Write(a.DistanceFeet.Numerator); w.Write(a.DistanceFeet.Denominator); w.Write(a.Running); w.Write((int)a.Status);
            }
        }
        public static void Read(BinaryReader r, Snapshot s)
        {
            if (!Bool(r)) return;
            string id = Text(r); var origin = new RuleTime(r.ReadInt64(), r.ReadInt64()); long slot = r.ReadInt64();
            var actors = new string[Count(r, 64)]; for (int i = 0; i < actors.Length; i++) actors[i] = Text(r);
            s.WorldSchedule = new WorldScheduleRecord(id, origin, actors, slot);
            s.WorldIntervals = new WorldIntervalRecord[Count(r, 64)];
            for (int i = 0; i < s.WorldIntervals.Length; i++) s.WorldIntervals[i] = new WorldIntervalRecord(Text(r), r.ReadInt64(), new RuleQuantity(r.ReadInt64(), r.ReadInt64()), Bool(r), Bool(r), Bool(r), r.ReadInt32());
            s.WorldTraversals = new WorldTraversalRecord[Count(r, 64)];
            for (int i = 0; i < s.WorldTraversals.Length; i++) s.WorldTraversals[i] = new WorldTraversalRecord(Text(r), r.ReadInt64(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(),
                new RuleQuantity(r.ReadInt64(), r.ReadInt64()), Bool(r), (WorldTraversalStatus)r.ReadInt32());
        }
    }
}
