using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Append-only schema60 persistence for route-segment feasibility and reconnaissance work.</summary>
    internal static class ExpeditionRouteReconnaissanceCodec
    {
        public static void Write(BinaryWriter writer, Snapshot snapshot)
        {
            var segments = snapshot.RouteSegments.OrderBy(x => x.StartedRevision).ToArray();
            writer.Write(segments.Length);
            foreach (var x in segments)
            {
                SnapshotCodec.WriteText(writer, x.Id); SnapshotCodec.WriteText(writer, x.RouteId);
                SnapshotCodec.WriteText(writer, x.TravelerId); writer.Write(x.StartedRevision);
                WriteQuantity(writer, x.StartingProgress); writer.Write((int)x.StartingMapping);
                SnapshotCodec.WriteText(writer, x.LatestAttemptId); SnapshotCodec.WriteText(writer, x.FeasibilityAttemptId);
                WriteQuantity(writer, x.ProgressAward); writer.Write((int)x.Status);
                writer.Write(x.TravelStartedRevision); writer.Write(x.TravelCompletedRevision);
                writer.Write(x.PressureReductionBlockedAtFloor);
            }
            var attempts = snapshot.RouteReconnaissanceAttempts.OrderBy(x => x.StartedRevision).ToArray();
            writer.Write(attempts.Length);
            foreach (var x in attempts)
            {
                SnapshotCodec.WriteText(writer, x.Id); SnapshotCodec.WriteText(writer, x.SegmentId);
                SnapshotCodec.WriteText(writer, x.RouteId); SnapshotCodec.WriteText(writer, x.LeadId);
                SnapshotCodec.WriteText(writer, x.InspectionProfileId);
                SnapshotCodec.WriteText(writer, x.InspectionProfileFingerprint);
                writer.Write(x.StartedRevision); WriteTime(writer, x.StartedAt); WriteTime(writer, x.UpdatedAt);
                WriteTime(writer, x.WorkDone); WriteTime(writer, x.WorkRequired); writer.Write((int)x.Status);
                writer.Write(x.Check != null);
                if (x.Check != null) WriteCheck(writer, x.Check);
            }
        }

        public static void Read(BinaryReader reader, Snapshot snapshot)
        {
            int segmentCount = SnapshotCodec.ReadCount(reader, ExpeditionRouteReconnaissanceValidation.MaxSegments);
            var segments = new ExpeditionRouteSegmentRecord[segmentCount];
            for (int i = 0; i < segmentCount; i++)
                segments[i] = new ExpeditionRouteSegmentRecord(SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                    SnapshotCodec.ReadText(reader), reader.ReadInt64(), ReadQuantity(reader),
                    (ExpeditionRouteMapping)reader.ReadInt32(), SnapshotCodec.ReadText(reader), SnapshotCodec.ReadText(reader),
                    ReadQuantity(reader), (ExpeditionRouteSegmentStatus)reader.ReadInt32(), reader.ReadInt64(), reader.ReadInt64(),
                    SnapshotCodec.ReadBool(reader));
            int attemptCount = SnapshotCodec.ReadCount(reader, ExpeditionRouteReconnaissanceValidation.MaxAttempts);
            var attempts = new ExpeditionRouteReconnaissanceAttemptRecord[attemptCount];
            for (int i = 0; i < attemptCount; i++)
            {
                string id = SnapshotCodec.ReadText(reader), segmentId = SnapshotCodec.ReadText(reader);
                string routeId = SnapshotCodec.ReadText(reader), leadId = SnapshotCodec.ReadText(reader);
                string inspectionProfileId = SnapshotCodec.ReadText(reader);
                string inspectionProfileFingerprint = SnapshotCodec.ReadText(reader);
                long revision = reader.ReadInt64(); RuleTime started = ReadTime(reader), updated = ReadTime(reader);
                RuleTime done = ReadTime(reader), required = ReadTime(reader);
                var status = (ExpeditionRouteReconnaissanceStatus)reader.ReadInt32();
                var check = SnapshotCodec.ReadBool(reader) ? ReadCheck(reader) : null;
                attempts[i] = new ExpeditionRouteReconnaissanceAttemptRecord(id, segmentId, routeId, leadId,
                    inspectionProfileId, inspectionProfileFingerprint, revision, started, updated, done, required,
                    status, check);
            }
            snapshot.RouteSegments = segments; snapshot.RouteReconnaissanceAttempts = attempts;
        }

        private static void WriteCheck(BinaryWriter w, ExpeditionRouteReconnaissanceCheckRecord x)
        {
            SnapshotCodec.WriteText(w, x.CommandId); w.Write(x.AppliedRevision); WriteTime(w, x.At);
            w.Write(x.LeadModifier); w.Write(x.ProficiencyRank); w.Write(x.ProficiencyBonus); w.Write(x.Dc);
            w.Write(x.ConditionOperationCount); w.Write(x.Disadvantage); w.Write(x.FirstRoll); w.Write(x.SecondRoll);
            w.Write(x.Natural); w.Write(x.Total); w.Write((int)x.Degree); w.Write(x.RandomBefore); w.Write(x.RandomAfter);
            w.Write(x.WordsConsumed);
        }

        private static ExpeditionRouteReconnaissanceCheckRecord ReadCheck(BinaryReader r)
            => new ExpeditionRouteReconnaissanceCheckRecord(SnapshotCodec.ReadText(r), r.ReadInt64(), ReadTime(r),
                r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), SnapshotCodec.ReadBool(r),
                r.ReadInt32(), r.ReadInt32(), r.ReadInt32(), r.ReadInt64(),
                (ExpeditionRouteReconnaissanceDegree)r.ReadInt32(), r.ReadUInt32(), r.ReadUInt32(), r.ReadInt64());

        private static void WriteTime(BinaryWriter w, RuleTime x) { w.Write(x.Numerator); w.Write(x.Denominator); }
        private static RuleTime ReadTime(BinaryReader r) => new RuleTime(r.ReadInt64(), r.ReadInt64());
        private static void WriteQuantity(BinaryWriter w, RuleQuantity x) { w.Write(x.Numerator); w.Write(x.Denominator); }
        private static RuleQuantity ReadQuantity(BinaryReader r) => new RuleQuantity(r.ReadInt64(), r.ReadInt64());
    }
}
