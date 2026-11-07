using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Append-only schema59 persistence for real TEST_ONLY Map Route work/check history.</summary>
    internal static class ExpeditionRouteMappingWorkCodec
    {
        public static void Write(BinaryWriter writer, Snapshot snapshot)
        {
            var attempts = snapshot.RouteMappingWorkAttempts.OrderBy(x => x.StartedRevision).ToArray();
            writer.Write(attempts.Length);
            foreach (var attempt in attempts)
            {
                SnapshotCodec.WriteText(writer, attempt.Id);
                SnapshotCodec.WriteText(writer, attempt.RouteId);
                SnapshotCodec.WriteText(writer, attempt.LeadId);
                var assistants = attempt.AssistantIds;
                writer.Write(assistants.Length);
                foreach (string assistant in assistants) SnapshotCodec.WriteText(writer, assistant);
                writer.Write(attempt.StartedRevision);
                WriteTime(writer, attempt.StartedAt);
                WriteTime(writer, attempt.UpdatedAt);
                WriteTime(writer, attempt.WorkDone);
                WriteTime(writer, attempt.WorkRequired);
                writer.Write((int)attempt.Status);
                writer.Write(attempt.Check != null);
                if (attempt.Check != null) WriteCheck(writer, attempt.Check);
            }
        }

        public static void Read(BinaryReader reader, Snapshot snapshot)
        {
            int count = SnapshotCodec.ReadCount(reader, ExpeditionRouteMappingWorkValidation.MaxAttempts);
            var attempts = new ExpeditionRouteMappingWorkAttemptRecord[count];
            for (int i = 0; i < count; i++)
            {
                string id = SnapshotCodec.ReadText(reader);
                string route = SnapshotCodec.ReadText(reader);
                string lead = SnapshotCodec.ReadText(reader);
                int assistantCount = SnapshotCodec.ReadCount(reader, 3);
                var assistants = new string[assistantCount];
                for (int a = 0; a < assistantCount; a++) assistants[a] = SnapshotCodec.ReadText(reader);
                long startedRevision = reader.ReadInt64();
                RuleTime startedAt = ReadTime(reader), updatedAt = ReadTime(reader), workDone = ReadTime(reader), workRequired = ReadTime(reader);
                var status = (ExpeditionRouteMappingWorkStatus)reader.ReadInt32();
                var check = SnapshotCodec.ReadBool(reader) ? ReadCheck(reader) : null;
                attempts[i] = new ExpeditionRouteMappingWorkAttemptRecord(id, route, lead, assistants,
                    startedRevision, startedAt, updatedAt, workDone, workRequired, status, check);
            }
            snapshot.RouteMappingWorkAttempts = attempts;
        }

        private static void WriteCheck(BinaryWriter writer, ExpeditionRouteMappingWorkCheckRecord check)
        {
            SnapshotCodec.WriteText(writer, check.CommandId);
            writer.Write(check.AppliedRevision);
            WriteTime(writer, check.At);
            writer.Write(check.LeadModifier);
            writer.Write(check.ProficiencyRank);
            writer.Write(check.ProficiencyBonus);
            writer.Write(check.AssistantBonus);
            writer.Write(check.Dc);
            writer.Write(check.ConditionOperationCount);
            writer.Write(check.Disadvantage);
            writer.Write(check.FirstRoll);
            writer.Write(check.SecondRoll);
            writer.Write(check.Natural);
            writer.Write(check.Total);
            writer.Write((int)check.Degree);
            writer.Write(check.RandomBefore);
            writer.Write(check.RandomAfter);
            writer.Write(check.WordsConsumed);
            writer.Write((int)check.MappingBefore);
            writer.Write((int)check.MappingAfter);
            writer.Write(check.MarksBefore);
            writer.Write(check.MarksGranted);
            writer.Write(check.MarksAfter);
        }

        private static ExpeditionRouteMappingWorkCheckRecord ReadCheck(BinaryReader reader)
            => new ExpeditionRouteMappingWorkCheckRecord(SnapshotCodec.ReadText(reader), reader.ReadInt64(), ReadTime(reader),
                reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(),
                SnapshotCodec.ReadBool(reader), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt64(),
                (ExpeditionRouteMappingResultDegree)reader.ReadInt32(),
                reader.ReadUInt32(), reader.ReadUInt32(), reader.ReadInt64(), (ExpeditionRouteMapping)reader.ReadInt32(),
                (ExpeditionRouteMapping)reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32());

        private static void WriteTime(BinaryWriter writer, RuleTime value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }

        private static RuleTime ReadTime(BinaryReader reader)
            => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
    }
}
