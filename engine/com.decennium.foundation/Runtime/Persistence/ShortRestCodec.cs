using System.IO;

namespace Decennium.Foundation
{
    internal static class ShortRestCodec
    {
        internal static void Write(BinaryWriter writer, ShortRestRecord[] rests)
        {
            SnapshotCodec.WriteText(writer, ShortRestBerth.Actor);
            SnapshotCodec.WriteText(writer, ShortRestBerth.Id);
            writer.Write(ShortRestBerth.InitialBenefits);
            writer.Write(ShortRestBerth.InitialWarriorStrain);
            writer.Write(rests.Length);
            foreach (var rest in rests) {
                writer.Write(rest.Sequence);
                SnapshotCodec.WriteText(writer, rest.StartCommandId);
                writer.Write(rest.StartRevision);
                WriteTime(writer, rest.StartedAt);
                writer.Write((byte)rest.Outcome);
                writer.Write((byte)rest.Benefit);
                writer.Write((byte)rest.Interruption);
                if (!rest.EndedAt.HasValue) continue;
                SnapshotCodec.WriteText(writer, rest.EndCommandId);
                writer.Write(rest.EndRevision);
                WriteTime(writer, rest.EndedAt.Value);
            }
        }

        internal static ShortRestRecord[] Read(BinaryReader reader)
        {
            if (SnapshotCodec.ReadText(reader) != ShortRestBerth.Actor || SnapshotCodec.ReadText(reader) != ShortRestBerth.Id
                || reader.ReadInt32() != ShortRestBerth.InitialBenefits || reader.ReadInt32() != ShortRestBerth.InitialWarriorStrain)
                throw new InvalidDataException("Unsupported Short Rest actor, site or initial entitlement.");
            var rests = new ShortRestRecord[SnapshotCodec.ReadCount(reader, ShortRestBerth.MaxAttempts)];
            for (int index = 0; index < rests.Length; index++) {
                int sequence = reader.ReadInt32();
                string command = SnapshotCodec.ReadText(reader);
                long revision = reader.ReadInt64();
                var start = ReadTime(reader);
                var outcome = (ShortRestOutcome)reader.ReadByte();
                var benefit = (ShortRestBenefit)reader.ReadByte();
                var interruption = (ShortRestInterruption)reader.ReadByte();
                rests[index] = outcome == ShortRestOutcome.Active
                    ? new ShortRestRecord(sequence, command, revision, start, outcome, benefit, interruption)
                    : new ShortRestRecord(sequence, command, revision, start, outcome, benefit, interruption,
                        SnapshotCodec.ReadText(reader), reader.ReadInt64(), ReadTime(reader));
            }
            return rests;
        }

        private static void WriteTime(BinaryWriter writer, RuleTime value)
        {
            writer.Write(value.Numerator);
            writer.Write(value.Denominator);
        }
        private static RuleTime ReadTime(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
    }
}
