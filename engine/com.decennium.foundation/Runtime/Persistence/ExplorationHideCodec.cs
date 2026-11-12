using System.IO;

namespace Decennium.Foundation
{
    internal static class ExplorationHideCodec
    {
        internal static void Write(BinaryWriter writer, ExplorationHideRecord record)
        {
            var d = record.Definition;
            foreach (string id in new[] { d.SourceRevision, d.DirectorId, d.HiderId, d.WitnessId })
                SnapshotCodec.WriteText(writer, id);
            WriteCell(writer, d.Recess);
            WriteCell(writer, d.Alternate);
            WriteRelocation(writer, record.LatestRelocation);
            writer.Write(record.Attempts.Count);
            foreach (var attempt in record.Attempts) {
                writer.Write(attempt.Revision);
                SnapshotCodec.WriteText(writer, attempt.CommandId);
                SnapshotCodec.WriteText(writer, attempt.CalendarId);
                writer.Write(attempt.PaidStart);
                WriteTime(writer, attempt.StartedAt);
                WriteTime(writer, attempt.DueAt);
                WriteCell(writer, attempt.Anchor);
                WriteRelocation(writer, attempt.Relocation);
                var end = attempt.End;
                writer.Write(end != null);
                if (end == null) continue;
                writer.Write((byte)end.Status);
                writer.Write((byte)end.Interruption);
                writer.Write(end.Revision);
                SnapshotCodec.WriteText(writer, end.CommandId);
                WriteTime(writer, end.At);
                SnapshotCodec.WriteText(writer, end.ObservationId);
                writer.Write((byte)end.NoRoll);
                SnapshotCodec.WriteText(writer, end.PriorFailureId);
                SnapshotCodec.WriteText(writer, end.PriorFailureObserverId);
                writer.Write((byte)end.EligibleObservers);
            }
        }

        internal static void Read(BinaryReader reader, Snapshot state)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            var d = new ExplorationHideDefinition(Text(), Text(), Text(), Text(), ReadCell(reader), ReadCell(reader));
            var latest = ReadRelocation(reader);
            var attempts = new ExplorationHideAttempt[SnapshotCodec.ReadCount(reader, ExplorationHideRecord.MaxAttempts)];
            for (int i = 0; i < attempts.Length; i++) {
                long revision = reader.ReadInt64();
                string command = Text();
                string calendar = Text();
                long paid = reader.ReadInt64();
                var start = ReadTime(reader);
                var due = ReadTime(reader);
                var anchor = ReadCell(reader);
                var relocation = ReadRelocation(reader);
                var end = SnapshotCodec.ReadBool(reader)
                    ? new ExplorationHideEnd((ExplorationHideStatus)reader.ReadByte(), (ExplorationHideInterruption)reader.ReadByte(),
                        reader.ReadInt64(), Text(), ReadTime(reader), Text(), (ExplorationHideNoRoll)reader.ReadByte(),
                        Text(), Text(), (ExplorationHideObservers)reader.ReadByte())
                    : null;
                attempts[i] = new ExplorationHideAttempt(revision, command, calendar, paid, start, due, anchor, relocation, end);
            }
            state.ExplorationHide = new ExplorationHideRecord(d, latest, attempts);
        }

        private static void WriteRelocation(BinaryWriter writer, ExplorationHideRelocation relocation)
        {
            writer.Write(relocation != null);
            if (relocation == null) return;
            WriteCell(writer, relocation.From);
            WriteCell(writer, relocation.To);
            writer.Write(relocation.StartedRevision);
            writer.Write(relocation.ArrivedRevision);
            SnapshotCodec.WriteText(writer, relocation.ArrivalCommandId);
            WriteTime(writer, relocation.At);
        }

        private static ExplorationHideRelocation ReadRelocation(BinaryReader reader) => SnapshotCodec.ReadBool(reader)
            ? new ExplorationHideRelocation(ReadCell(reader), ReadCell(reader), reader.ReadInt64(), reader.ReadInt64(),
                SnapshotCodec.ReadText(reader), ReadTime(reader))
            : null;

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
