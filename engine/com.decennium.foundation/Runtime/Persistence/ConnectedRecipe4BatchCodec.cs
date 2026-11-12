using System.IO;

namespace Decennium.Foundation
{
    internal static class ConnectedRecipe4BatchCodec
    {
        internal static void Write(BinaryWriter writer, ConnectedRecipe4Batch record)
        {
            SnapshotCodec.WriteText(writer, record.ApparatusId);
            SnapshotCodec.WriteText(writer, record.FitId);
            SnapshotCodec.WriteText(writer, record.ReturnVesselId);
            SnapshotCodec.WriteText(writer, record.OrderId);
            writer.Write(record.ChargeRevision);
            writer.Write(record.SettlementRevision);
            writer.Write((byte)record.Disposition);
        }

        internal static ConnectedRecipe4Batch Read(BinaryReader reader)
            => new ConnectedRecipe4Batch(SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader), reader.ReadInt64(), reader.ReadInt64(),
                (ConnectedSpecimenDisposition)reader.ReadByte());
    }
}
