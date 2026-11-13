using System.IO;

namespace Decennium.Foundation
{
    internal static class CompanionStabilizationCodec
    {
        internal static void Write(BinaryWriter writer, CompanionStabilizationAttempt[] attempts)
        {
            writer.Write(attempts.Length);
            foreach (var attempt in attempts) {
                SnapshotCodec.WriteText(writer, attempt.CommandId);
                writer.Write(attempt.Revision);
                SnapshotCodec.WriteText(writer, attempt.ActorId);
                SnapshotCodec.WriteText(writer, attempt.PatientId);
                writer.Write(attempt.TurnOrdinal);
                writer.Write(attempt.At.Numerator);
                writer.Write(attempt.At.Denominator);
                writer.Write(attempt.First);
                writer.Write(attempt.Second);
                writer.Write(attempt.Natural);
                writer.Write(attempt.Modifier);
                writer.Write(attempt.RecoveryDie);
                writer.Write(attempt.RandomBefore);
                writer.Write(attempt.RandomAfter);
                writer.Write(attempt.WordsConsumed);
            }
        }

        internal static CompanionStabilizationAttempt[] Read(BinaryReader reader)
        {
            var attempts = new CompanionStabilizationAttempt[SnapshotCodec.ReadCount(reader, Validation.MaxReceipts)];
            for (int i = 0; i < attempts.Length; i++)
                attempts[i] = new CompanionStabilizationAttempt(SnapshotCodec.ReadText(reader), reader.ReadInt64(),
                    SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader), reader.ReadInt32(),
                    new RuleTime(reader.ReadInt64(), reader.ReadInt64()), reader.ReadInt32(), reader.ReadInt32(),
                    reader.ReadInt32(), reader.ReadInt32(), reader.ReadInt32(), reader.ReadUInt32(), reader.ReadUInt32(), reader.ReadInt64());
            return attempts;
        }
    }
}
