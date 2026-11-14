using System.IO;

namespace Decennium.Foundation
{
    internal static class ConsumeDecayCodec
    {
        internal static void Write(BinaryWriter writer, ConsumeDecayRecord grant)
        {
            writer.Write(grant != null);
            if (grant == null) return;
            SnapshotCodec.WriteText(writer, grant.CommandId);
            writer.Write(grant.Revision);
            WriteTime(writer, grant.StartedAt);
            writer.Write(grant.Offer);
            writer.Write(grant.Accepted);
            writer.Write((byte)grant.End);
            if (!grant.EndedAt.HasValue) return;
            WriteTime(writer, grant.EndedAt.Value);
            writer.Write(grant.EndRevision);
        }

        internal static ConsumeDecayRecord Read(BinaryReader reader)
        {
            if (!SnapshotCodec.ReadBool(reader)) return null;
            string command = SnapshotCodec.ReadText(reader);
            long revision = reader.ReadInt64();
            var start = ReadTime(reader);
            int offer = reader.ReadInt32();
            bool accepted = SnapshotCodec.ReadBool(reader);
            var end = (TemporaryHpEnd)reader.ReadByte();
            return end == TemporaryHpEnd.None
                ? new ConsumeDecayRecord(command, revision, start, offer, accepted)
                : new ConsumeDecayRecord(command, revision, start, offer, accepted, end, ReadTime(reader), reader.ReadInt64());
        }

        private static void WriteTime(BinaryWriter writer, RuleTime value)
        {
            writer.Write(value.Numerator);
            writer.Write(value.Denominator);
        }

        private static RuleTime ReadTime(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
    }
}
