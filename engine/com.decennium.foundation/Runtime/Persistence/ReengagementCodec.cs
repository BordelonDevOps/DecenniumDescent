using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    internal static class ReengagementCodec
    {
        public static void Write(BinaryWriter writer, ReengagementRecord record)
        {
            var d = record.Definition;
            foreach (var id in new[] { d.RootId, d.SegmentId, d.LeadId, d.CompanionId, d.DefenderId,
                d.ControllerId, d.ConsentId, d.DirectorMandateId })
                SnapshotCodec.WriteText(writer, id);
            writer.Write(record.Contacts.Count);
            foreach (var row in record.Contacts) {
                writer.Write(row.ApproachRevision);
                writer.Write(row.ArrivalRevision);
                SnapshotCodec.WriteText(writer, row.ArrivalCommandId);
                writer.Write(row.At.Numerator);
                writer.Write(row.At.Denominator);
                writer.Write(row.MarkerOrdinal);
                writer.Write(row.DistanceFeet.Numerator);
                writer.Write(row.DistanceFeet.Denominator);
                SnapshotCodec.WriteText(writer, row.Failure);
            }
        }

        public static void Read(BinaryReader reader, Snapshot state)
        {
            string Text() => SnapshotCodec.ReadText(reader);
            var definition = new ReengagementDefinition(Text(), Text(), Text(), Text(), Text(), Text(), Text(), Text());
            var rows = new ReengagementContact[SnapshotCodec.ReadCount(reader, ReengagementRecord.MaxContacts)];
            for (int i = 0; i < rows.Length; i++)
                rows[i] = new ReengagementContact(reader.ReadInt64(), reader.ReadInt64(), Text(),
                    new RuleTime(reader.ReadInt64(), reader.ReadInt64()), reader.ReadInt32(),
                    new RuleQuantity(reader.ReadInt64(), reader.ReadInt64()), Text());
            state.Reengagement = new ReengagementRecord(definition, rows);
            if (state.Reengagement.Entry == null) return;
            var phase = state.Reinforcement.Admission?.Phase ?? throw new InvalidDataException("Missing inherited re-engagement phase.");
            if (state.Encounter?.Id == definition.SegmentId) state.Encounter = state.Encounter.BindInheritedPhase(phase);
            state.ClosedEncounters = state.ClosedEncounters.Select(x => x.Encounter.Id == definition.SegmentId
                ? new ClosedEncounterRecord(x.Encounter.BindInheritedPhase(phase), x.ClosedRevision, x.ClosedAt, x.Reason)
                : x).ToArray();
        }
    }
}
