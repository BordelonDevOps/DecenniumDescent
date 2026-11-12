using System.IO;

namespace Decennium.Foundation
{
    internal static class ExplorationSearchCodec
    {
        internal static void Write(BinaryWriter writer, ExplorationSearchRecord record)
        {
            var d = record.Definition;
            foreach (string id in new[] { d.SourceRevision, d.DirectorId, d.CueId, d.SearcherId, d.ConcealedActorId })
                SnapshotCodec.WriteText(writer, id);
            foreach (var cell in new[] { d.Anchor, d.CueCandidate, d.Sign, d.Occlusion })
                WriteCell(writer, cell);

            writer.Write(record.Attempts.Count);
            foreach (var attempt in record.Attempts) {
                writer.Write(attempt.Revision);
                SnapshotCodec.WriteText(writer, attempt.CommandId);
                writer.Write(attempt.IntervalIndex);
                WriteTime(writer, attempt.StartedAt);
                WriteTime(writer, attempt.DueAt);
                WriteCell(writer, attempt.Candidate);

                var end = attempt.End;
                writer.Write(end != null);
                if (end == null) continue;
                writer.Write((byte)end.Status);
                writer.Write((byte)end.Interruption);
                writer.Write(end.Revision);
                SnapshotCodec.WriteText(writer, end.CommandId);
                WriteTime(writer, end.At);
                SnapshotCodec.WriteText(writer, end.ObservationId);
                SnapshotCodec.WriteText(writer, end.CueId);
                SnapshotCodec.WriteText(writer, end.HideId);
            }
        }

        internal static void Read(BinaryReader reader, Snapshot state)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            var d = new ExplorationSearchDefinition(Text(), Text(), Text(), Text(), Text(),
                ReadCell(reader), ReadCell(reader), ReadCell(reader), ReadCell(reader));
            var attempts = new ExplorationSearchAttempt[SnapshotCodec.ReadCount(reader, ExplorationSearchRecord.MaxAttempts)];
            for (int i = 0; i < attempts.Length; i++) {
                long revision = reader.ReadInt64();
                string commandId = Text();
                long interval = reader.ReadInt64();
                var start = ReadTime(reader);
                var due = ReadTime(reader);
                var candidate = ReadCell(reader);
                var end = SnapshotCodec.ReadBool(reader)
                    ? new ExplorationSearchEnd((ExplorationSearchStatus)reader.ReadByte(), (ExplorationSearchInterruption)reader.ReadByte(),
                        reader.ReadInt64(), Text(), ReadTime(reader), Text(), Text(), Text())
                    : null;
                attempts[i] = new ExplorationSearchAttempt(revision, commandId, interval, start, due, candidate, end);
            }
            state.ExplorationSearch = new ExplorationSearchRecord(d, attempts);
        }

        private static void WriteCell(BinaryWriter writer, ExplorationSearchCell cell)
        {
            writer.Write(cell.X);
            writer.Write(cell.Y);
        }

        private static ExplorationSearchCell ReadCell(BinaryReader reader) => new ExplorationSearchCell(reader.ReadInt32(), reader.ReadInt32());

        private static void WriteTime(BinaryWriter writer, RuleTime time)
        {
            writer.Write(time.Numerator);
            writer.Write(time.Denominator);
        }

        private static RuleTime ReadTime(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
    }
}
