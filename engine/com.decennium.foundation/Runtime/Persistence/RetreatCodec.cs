using System.IO;

namespace Decennium.Foundation
{
    internal static class RetreatCodec
    {
        public static void Write(BinaryWriter writer, RetreatRecord value)
        {
            void Text(string x) => SnapshotCodec.WriteText(writer, x);
            void Time(RuleTime x) { writer.Write(x.Numerator); writer.Write(x.Denominator); }
            void Position(RetreatPosition x) { writer.Write(x.X); writer.Write(x.Y); }
            var d = value.Definition;
            foreach (string id in new[] { d.Id, d.EncounterId, d.LeadId, d.CompanionId, d.DefenderId, d.ClubId, d.ControllerId,
                d.LeadMandateId, d.CompanionConsentId, d.OperationId, d.RouteId, d.RouteAccessId, d.RouteFingerprint, d.CohortId, d.ExposureId })
                Text(id);
            writer.Write(value.DeclaredRevision);
            Text(value.DeclarationId);
            writer.Write(value.Rounds.Count);
            foreach (var row in value.Rounds) {
                writer.Write(row.Number);
                writer.Write(row.FirstTurn);
                writer.Write(row.StartRevision);
                Time(row.StartedAt);
                var task = row.Task;
                writer.Write(task != null);
                if (task != null) {
                    writer.Write(task.Revision);
                    Text(task.CommandId);
                    Time(task.At);
                    writer.Write(task.Turn);
                    writer.Write(task.Modifier);
                    writer.Write(task.First);
                    writer.Write(task.Second);
                    writer.Write(task.RandomBefore);
                    writer.Write(task.RandomAfter);
                    writer.Write(task.WordsConsumed);
                    writer.Write((int)task.Degree);
                }
                Text(row.ThreatId);
                var end = row.Settlement;
                writer.Write(end != null);
                if (end == null) continue;
                writer.Write((int)end.Outcome);
                writer.Write(end.Revision);
                Text(end.CommandId);
                Time(end.At);
                writer.Write(end.EndTurn);
                Position(end.Lead);
                Position(end.Companion);
                Position(end.Defender);
                Text(end.LeadCrossingId);
                Text(end.CompanionCrossingId);
            }
        }

        public static RetreatRecord Read(BinaryReader reader)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            RuleTime Time() => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
            RetreatPosition Position() => new RetreatPosition(reader.ReadInt32(), reader.ReadInt32());
            bool Flag() => SnapshotCodec.ReadBool(reader);
            var d = new RetreatDefinition(Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text(),
                Text(), Text(), Text(), Text(), Text());
            long revision = reader.ReadInt64();
            string declaration = Text();
            var rows = new RetreatRound[SnapshotCodec.ReadCount(reader, 5)];
            for (int i = 0; i < rows.Length; i++) {
                long number = reader.ReadInt64();
                int turn = reader.ReadInt32();
                long startRevision = reader.ReadInt64();
                RuleTime started = Time();
                var task = Flag() ? new RetreatTaskRecord(reader.ReadInt64(), Text(), Time(), reader.ReadInt32(),
                    reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadUInt32(), reader.ReadUInt32(),
                    reader.ReadInt64(), (RetreatTaskDegree)reader.ReadInt32()) : null;
                string threat = Text();
                var end = Flag() ? new RetreatSettlement((RetreatOutcome)reader.ReadInt32(), reader.ReadInt64(), Text(),
                    Time(), reader.ReadInt32(), Position(), Position(), Position(), Text(), Text()) : null;
                rows[i] = new RetreatRound(number, turn, startRevision, started, task, threat, end);
            }
            return new RetreatRecord(d, revision, declaration, rows);
        }
    }
}
