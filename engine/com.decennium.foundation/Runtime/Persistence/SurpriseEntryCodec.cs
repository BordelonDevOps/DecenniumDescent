using System.IO;

namespace Decennium.Foundation
{
    internal static class SurpriseEntryCodec
    {
        internal static void Write(BinaryWriter writer, SurpriseEntryRecord record)
        {
            var binding = record.Binding;
            foreach (string id in new[] { binding.SourceRevision, binding.DirectorId, binding.EncounterId,
                binding.ParticipantId, binding.ThreatId, binding.EvidenceId })
                SnapshotCodec.WriteText(writer, id);
            writer.Write((byte)binding.Outcome);
            var decision = record.Decision;
            writer.Write(decision != null);
            if (decision != null) {
                writer.Write(decision.Revision);
                SnapshotCodec.WriteText(writer, decision.CommandId);
                Time(writer, decision.At);
            }
            var start = record.FirstStart;
            writer.Write(start != null);
            if (start != null) {
                writer.Write(start.Revision);
                writer.Write(start.Ordinal);
                Time(writer, start.At);
            }
            var end = record.FirstEnd;
            writer.Write(end != null);
            if (end != null) {
                writer.Write(end.EndRevision);
                SnapshotCodec.WriteText(writer, end.EndCommandId);
                writer.Write(end.CompletedRevision);
                Time(writer, end.At);
            }
        }

        internal static void Read(BinaryReader reader, Snapshot state)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            var binding = new SurpriseAwarenessBinding(Text(), Text(), Text(), Text(), Text(), Text(), (SurpriseAwareness)reader.ReadByte());
            var decision = reader.ReadBoolean() ? new SurpriseEntryDecision(reader.ReadInt64(), Text(), Time(reader)) : null;
            var start = reader.ReadBoolean() ? new SurpriseFirstStart(reader.ReadInt64(), reader.ReadInt32(), Time(reader)) : null;
            var end = reader.ReadBoolean() ? new SurpriseFirstEnd(reader.ReadInt64(), Text(), reader.ReadInt64(), Time(reader)) : null;
            state.SurpriseEntry = new SurpriseEntryRecord(binding, decision, start, end);
        }

        private static void Time(BinaryWriter writer, RuleTime time)
        {
            writer.Write(time.Numerator);
            writer.Write(time.Denominator);
        }

        private static RuleTime Time(BinaryReader reader) => new RuleTime(reader.ReadInt64(), reader.ReadInt64());
    }
}
