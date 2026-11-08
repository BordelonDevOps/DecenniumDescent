using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Append-only persistence for real TEST_ONLY Map Route work/check history.</summary>
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
                if (attempt.Check != null) WriteCheck(writer, attempt.Check,snapshot.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema);
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
                var check = SnapshotCodec.ReadBool(reader) ? ReadCheck(reader,snapshot.SchemaVersion>=Snapshot.SharedCharacterAdvancementSchema) : null;
                attempts[i] = new ExpeditionRouteMappingWorkAttemptRecord(id, route, lead, assistants,
                    startedRevision, startedAt, updatedAt, workDone, workRequired, status, check);
            }
            snapshot.RouteMappingWorkAttempts = attempts;
        }

        private static void WriteCheck(BinaryWriter writer, ExpeditionRouteMappingWorkCheckRecord check,bool includeCausalInjuries)
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
            if(includeCausalInjuries) {
                writer.Write(check.LinkedInjuriesAtCheck.Count);
                foreach(int injury in check.LinkedInjuriesAtCheck)writer.Write(injury);
            }
        }

        private static ExpeditionRouteMappingWorkCheckRecord ReadCheck(BinaryReader reader,bool includeCausalInjuries)
        {
            string command=SnapshotCodec.ReadText(reader);long revision=reader.ReadInt64();RuleTime at=ReadTime(reader);
            int lead=reader.ReadInt32(),rank=reader.ReadInt32(),proficiency=reader.ReadInt32(),assistant=reader.ReadInt32(),dc=reader.ReadInt32(),conditionCount=reader.ReadInt32();
            bool disadvantage=SnapshotCodec.ReadBool(reader);int first=reader.ReadInt32(),second=reader.ReadInt32(),natural=reader.ReadInt32();long total=reader.ReadInt64();
            var degree=(ExpeditionRouteMappingResultDegree)reader.ReadInt32();uint before=reader.ReadUInt32(),after=reader.ReadUInt32();long words=reader.ReadInt64();
            var mappingBefore=(ExpeditionRouteMapping)reader.ReadInt32();var mappingAfter=(ExpeditionRouteMapping)reader.ReadInt32();
            int marksBefore=reader.ReadInt32(),marksGranted=reader.ReadInt32(),marksAfter=reader.ReadInt32();
            int[] injuries=Array.Empty<int>();
            if(includeCausalInjuries) { injuries=new int[SnapshotCodec.ReadCount(reader,3)];for(int i=0;i<injuries.Length;i++)injuries[i]=reader.ReadInt32(); }
            return new ExpeditionRouteMappingWorkCheckRecord(command,revision,at,lead,rank,proficiency,assistant,dc,conditionCount,
                disadvantage,first,second,natural,total,degree,before,after,words,mappingBefore,mappingAfter,marksBefore,marksGranted,marksAfter,injuries);
        }

        private static void WriteTime(BinaryWriter writer, RuleTime value)
        { writer.Write(value.Numerator); writer.Write(value.Denominator); }

        private static RuleTime ReadTime(BinaryReader reader)
            => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
    }
}
