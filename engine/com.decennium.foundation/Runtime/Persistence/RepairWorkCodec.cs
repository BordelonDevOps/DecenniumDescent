using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class RepairWorkCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static void Text(BinaryWriter w, string value) { var b = Utf8.GetBytes(value); w.Write(b.Length); w.Write(b); }
        private static string Text(BinaryReader r) { int n = Count(r, 96); var b = r.ReadBytes(n); if (b.Length != n) throw new EndOfStreamException(); return Utf8.GetString(b); }
        private static int Count(BinaryReader r, int max) { int n = r.ReadInt32(); if (n < 0 || n > max) throw new InvalidDataException("Invalid repair collection length."); return n; }
        private static void Time(BinaryWriter w, RuleTime t) { w.Write(t.Numerator); w.Write(t.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.RepairWork.Length);
            foreach (var job in s.RepairWork.OrderBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, job.Id); Text(w, job.WorkerId); Text(w, job.TargetId); Text(w, job.ToolkitId); Text(w, job.MaterialsId); w.Write((int)job.Status); Time(w, job.StartedAt); Time(w, job.UpdatedAt);
                w.Write(job.Work.Phases.Count); foreach (var phase in job.Work.Phases) Time(w, phase); w.Write(job.Work.CompletedPhases); Time(w, job.Work.Partial); Time(w, job.Work.Labor);
                w.Write(job.First); w.Write(job.Second); w.Write(job.Natural);
            }
        }
        public static void Read(BinaryReader r, Snapshot s)
        {
            s.RepairWork = new RepairWorkRecord[Count(r, RepairWorkValidation.MaxRecords)];
            for (int i = 0; i < s.RepairWork.Length; i++) {
                string id = Text(r), worker = Text(r), target = Text(r), tool = Text(r), materials = Text(r); var status = (RepairWorkStatus)r.ReadInt32(); var start = Time(r); var updated = Time(r);
                var phases = new RuleTime[Count(r, ActiveWorkProgress.MaxPhases)]; for (int j = 0; j < phases.Length; j++) phases[j] = Time(r);
                var work = new ActiveWorkProgress(phases, r.ReadInt32(), Time(r), Time(r));
                s.RepairWork[i] = new RepairWorkRecord(id, worker, target, tool, materials, status, start, updated, work, r.ReadInt32(), r.ReadInt32(), r.ReadInt32());
            }
        }
    }
}
