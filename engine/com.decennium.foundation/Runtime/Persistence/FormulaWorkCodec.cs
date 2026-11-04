using System;
using System.IO;
using System.Linq;
using System.Text;

namespace Decennium.Foundation
{
    internal static class FormulaWorkCodec
    {
        private static readonly UTF8Encoding Utf8 = new UTF8Encoding(false, true);
        private static void Text(BinaryWriter w, string value) { var bytes = Utf8.GetBytes(value); w.Write(bytes.Length); w.Write(bytes); }
        private static string Text(BinaryReader r)
        {
            int count = Count(r, 96); var bytes = r.ReadBytes(count);
            if (bytes.Length != count) throw new EndOfStreamException(); return Utf8.GetString(bytes);
        }
        private static int Count(BinaryReader r, int max) { int n = r.ReadInt32(); if (n < 0 || n > max) throw new InvalidDataException("Invalid formula collection length."); return n; }
        private static void Time(BinaryWriter w, RuleTime t) { w.Write(t.Numerator); w.Write(t.Denominator); }
        private static RuleTime Time(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        public static void Write(BinaryWriter w, Snapshot s)
        {
            w.Write(s.FormulaWork.Length);
            foreach (var job in s.FormulaWork.OrderBy(x => x.Id, StringComparer.Ordinal)) {
                Text(w, job.Id); Text(w, job.WorkerId); Text(w, job.RecipeId); Text(w, job.EvidenceId); Text(w, job.MethodId); Text(w, job.PreviousAttemptId);
                w.Write((int)job.Kind); w.Write((int)job.Status); Time(w, job.StartedAt); Time(w, job.UpdatedAt);
                w.Write(job.Work.Phases.Count); foreach (var phase in job.Work.Phases) Time(w, phase);
                w.Write(job.Work.CompletedPhases); Time(w, job.Work.Partial); Time(w, job.Work.Labor);
                w.Write(job.First); w.Write(job.Second); w.Write(job.Natural);
            }
        }
        public static void Read(BinaryReader r, Snapshot s)
        {
            s.FormulaWork = new FormulaWorkRecord[Count(r, FormulaWorkValidation.MaxRecords)];
            for (int i = 0; i < s.FormulaWork.Length; i++) {
                string id = Text(r), worker = Text(r), recipe = Text(r), evidence = Text(r), method = Text(r), prior = Text(r);
                var kind = (FormulaWorkKind)r.ReadInt32(); var status = (FormulaWorkStatus)r.ReadInt32(); var start = Time(r); var update = Time(r);
                var phases = new RuleTime[Count(r, ActiveWorkProgress.MaxPhases)]; for (int j = 0; j < phases.Length; j++) phases[j] = Time(r);
                var work = new ActiveWorkProgress(phases, r.ReadInt32(), Time(r), Time(r));
                s.FormulaWork[i] = new FormulaWorkRecord(id, worker, recipe, evidence, method, kind, status, start, update, work, r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), prior);
            }
        }
    }
}
