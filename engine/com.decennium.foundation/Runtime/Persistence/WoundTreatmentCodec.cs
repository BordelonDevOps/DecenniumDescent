using System.IO;

namespace Decennium.Foundation
{
    internal static class WoundTreatmentCodec
    {
        internal static void Write(BinaryWriter writer, WoundTreatmentRecord[] jobs)
        {
            writer.Write(jobs.Length);
            foreach (var job in jobs) {
                writer.Write(job.Basket);
                SnapshotCodec.WriteText(writer, job.StartCommandId);
                writer.Write(job.StartRevision);
                WriteTime(writer, job.StartedAt);
                writer.Write(job.LinkedInjury);
                writer.Write((byte)job.Outcome);
                if (!job.EndedAt.HasValue) continue;
                SnapshotCodec.WriteText(writer, job.EndCommandId);
                writer.Write(job.EndRevision);
                WriteTime(writer, job.EndedAt.Value);
                if (job.Outcome == WoundTreatmentOutcome.Interrupted) continue;
                writer.Write(job.First);
                writer.Write(job.Second);
                writer.Write(job.Natural);
                writer.Write(job.Modifier);
                writer.Write(job.RandomBefore);
                writer.Write(job.RandomAfter);
                writer.Write(job.WordsConsumed);
            }
        }

        internal static WoundTreatmentRecord[] Read(BinaryReader reader)
        {
            var jobs = new WoundTreatmentRecord[SnapshotCodec.ReadCount(reader, WoundTreatmentStation.BasketCount)];
            for (int i = 0; i < jobs.Length; i++) {
                int basket = reader.ReadInt32();
                string startCommand = SnapshotCodec.ReadText(reader);
                long startRevision = reader.ReadInt64();
                var start = ReadTime(reader);
                int injury = reader.ReadInt32();
                var outcome = (WoundTreatmentOutcome)reader.ReadByte();
                if (outcome == WoundTreatmentOutcome.Active) {
                    jobs[i] = new WoundTreatmentRecord(basket, startCommand, startRevision, start, injury);
                    continue;
                }
                string endCommand = SnapshotCodec.ReadText(reader);
                long endRevision = reader.ReadInt64();
                var end = ReadTime(reader);
                jobs[i] = outcome == WoundTreatmentOutcome.Interrupted
                    ? new WoundTreatmentRecord(basket, startCommand, startRevision, start, injury, outcome, endCommand, endRevision, end)
                    : new WoundTreatmentRecord(basket, startCommand, startRevision, start, injury, outcome, endCommand, endRevision, end,
                        reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadUInt32(),
                        reader.ReadUInt32(), reader.ReadInt64());
            }
            return jobs;
        }

        private static void WriteTime(BinaryWriter writer, RuleTime value)
        {
            writer.Write(value.Numerator);
            writer.Write(value.Denominator);
        }

        private static RuleTime ReadTime(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
    }
}
