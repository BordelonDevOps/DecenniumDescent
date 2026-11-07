using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Append-only schema54 persistence for TEST_ONLY route-mapping result history.</summary>
    internal static class ExpeditionRouteMappingCodec
    {
        public static void Write(BinaryWriter writer, Snapshot snapshot)
        {
            var records = snapshot.RouteMappingResults.OrderBy(x => x.AppliedRevision).ToArray();
            writer.Write(records.Length);
            foreach (var value in records)
            {
                SnapshotCodec.WriteText(writer, value.RouteId);
                SnapshotCodec.WriteText(writer, value.ResultId);
                SnapshotCodec.WriteText(writer, value.ActorId);
                SnapshotCodec.WriteText(writer, value.CommandId);
                SnapshotCodec.WriteText(writer, value.OperationId);
                SnapshotCodec.WriteText(writer, value.EvidenceId);
                SnapshotCodec.WriteText(writer, value.ResultProfileFingerprint);
                writer.Write(value.AppliedRevision);
                writer.Write(value.CompletedAt.Numerator);
                writer.Write(value.CompletedAt.Denominator);
                writer.Write((int)value.Degree);
                writer.Write((int)value.MappingBefore);
                writer.Write((int)value.MappingAfter);
                writer.Write(value.MarksBefore);
                writer.Write(value.MarksGranted);
                writer.Write(value.MarksAfter);
                writer.Write(value.Synthetic);
            }
        }

        public static void Read(BinaryReader reader, Snapshot snapshot)
        {
            int count = SnapshotCodec.ReadCount(reader, ExpeditionRouteMappingRules.MaxResults);
            var records = new ExpeditionRouteMappingResultRecord[count];
            for (int i = 0; i < count; i++)
            {
                records[i] = new ExpeditionRouteMappingResultRecord(
                    SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                    SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                    SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                    SnapshotCodec.ReadText(reader), reader.ReadInt64(),
                    new RuleTime(reader.ReadInt64(), reader.ReadInt64()),
                    (ExpeditionRouteMappingResultDegree)reader.ReadInt32(),
                    (ExpeditionRouteMapping)reader.ReadInt32(), (ExpeditionRouteMapping)reader.ReadInt32(),
                    reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), SnapshotCodec.ReadBool(reader));
            }
            snapshot.RouteMappingResults = records;
        }
    }
}
