using System;
using System.IO;
using System.Linq;

namespace Decennium.Foundation
{
    /// <summary>Schema76 append-only TEST_ONLY causal links for controlled opening, in-vessel
    /// portions, and trusted exposure occurrences. Earlier schema layouts do not call this codec.</summary>
    internal static class HarvestPreservationEvidenceCodec
    {
        private static void Time(BinaryWriter w,RuleTime value){w.Write(value.Numerator);w.Write(value.Denominator);}
        private static RuleTime Time(BinaryReader r)=>new RuleTime(r.ReadInt64(),r.ReadInt64());

        public static void Write(BinaryWriter w,Snapshot s)
        {
            var records=s.HarvestPreservationEvidence.OrderBy(x=>x.AppliedRevision).ToArray();
            w.Write(records.Length);
            foreach(var x in records) {
                w.Write((int)x.Kind);SnapshotCodec.WriteText(w,x.Id);SnapshotCodec.WriteText(w,x.TreatmentAttemptId);
                SnapshotCodec.WriteText(w,x.VesselId);SnapshotCodec.WriteText(w,x.CommandId);w.Write(x.AppliedRevision);Time(w,x.At);
                SnapshotCodec.WriteText(w,x.PortableHandlingId);SnapshotCodec.WriteText(w,x.ToolId);
                SnapshotCodec.WriteText(w,x.CleanToolFactId);
                SnapshotCodec.WriteText(w,x.OpeningEvidenceId);SnapshotCodec.WriteText(w,x.ChildLotId);
                SnapshotCodec.WriteText(w,x.OccurrenceId);w.Write((int)x.Cause);
            }
        }

        public static void Read(BinaryReader r,Snapshot s)
        {
            int count=SnapshotCodec.ReadCount(r,HarvestPreservationEvidenceValidation.MaxRecords);
            var records=new HarvestPreservationEvidenceRecord[count];
            for(int i=0;i<count;i++) {
                var kind=(HarvestPreservationEvidenceKind)r.ReadInt32();string id=SnapshotCodec.ReadText(r);
                string treatment=SnapshotCodec.ReadText(r),vessel=SnapshotCodec.ReadText(r),command=SnapshotCodec.ReadText(r);
                long revision=r.ReadInt64();RuleTime at=Time(r);string handling=SnapshotCodec.ReadText(r),tool=SnapshotCodec.ReadText(r);
                string cleanToolFact=SnapshotCodec.ReadText(r);
                string opening=SnapshotCodec.ReadText(r),child=SnapshotCodec.ReadText(r),occurrence=SnapshotCodec.ReadText(r);
                var cause=(HarvestPreservationExposureCause)r.ReadInt32();
                records[i]=new HarvestPreservationEvidenceRecord(id,kind,treatment,vessel,command,revision,at,
                    handling,tool,cleanToolFact,opening,child,occurrence,cause);
            }
            s.HarvestPreservationEvidence=records;
        }
    }
}
