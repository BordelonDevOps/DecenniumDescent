using System.IO;

namespace Decennium.Foundation
{
    internal static class ConnectedBloodSpecimenCodec
    {
        internal static void Write(BinaryWriter writer, ConnectedBloodSpecimen record)
        {
            foreach (var value in new[] { record.AuthorityId, record.LotId, record.SourceOccurrence, record.RecipeOccurrence })
                SnapshotCodec.WriteText(writer, value);
            writer.Write(record.Origin.Numerator);
            writer.Write(record.Origin.Denominator);
            writer.Write(record.IntervalSeconds);
            writer.Write(record.UnitMass.Numerator);
            writer.Write(record.UnitMass.Denominator);
            foreach (var value in new[] { record.VesselId, record.FitId, record.SupplyLotId, record.ToolId, record.CleanToolFactId })
                SnapshotCodec.WriteText(writer, value);
        }

        internal static ConnectedBloodSpecimen Read(BinaryReader reader)
            => new ConnectedBloodSpecimen(SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                new RuleTime(reader.ReadInt64(), reader.ReadInt64()), reader.ReadInt32(),
                new RuleQuantity(reader.ReadInt64(), reader.ReadInt64()), SnapshotCodec.ReadText(reader),
                SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                SnapshotCodec.ReadText(reader));
    }
}
